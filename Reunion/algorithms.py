from audiofield.fields import AudioField
import speech_recognition as sr
import os
from pfa2.settings import BASE_DIR, STATIC_DIR
import requests
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.summarization import summarize, keywords
import networkx
import numpy as np
import re
import nltk
import string
from nltk.stem import WordNetLemmatizer
from html.parser import HTMLParser
import unicodedata
from pattern.en import tag
from scipy.sparse.linalg import svds
from nltk.corpus import wordnet as wn
import argparse
import os
import subprocess
import threading



CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

from pfa2.settings import MEDIA_DIR



stopword_list = nltk.corpus.stopwords.words('english')
wnl = WordNetLemmatizer()
html_parser = HTMLParser()


def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


def expand_contractions(text, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

# Annotate text tokens with POS tags
def pos_tag_text(text):
    def penn_to_wn_tags(pos_tag):
        if pos_tag.startswith('J'):
            return wn.ADJ
        elif pos_tag.startswith('V'):
            return wn.VERB
        elif pos_tag.startswith('N'):
            return wn.NOUN
        elif pos_tag.startswith('R'):
            return wn.ADV
        else:
            return None

    tagged_text = tag(text)
    tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag))
                         for word, pos_tag in
                         tagged_text]
    return tagged_lower_text


# lemmatize text based on POS tags
def lemmatize_text(text):
    pos_tagged_text = pos_tag_text(text)
    lemmatized_tokens = [wnl.lemmatize(word, pos_tag) if pos_tag
                         else word
                         for word, pos_tag in pos_tagged_text]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text


def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def unescape_html(parser, text):
    return parser.unescape(text)


def normalize_corpus(corpus, lemmatize=True, tokenize=False):
    normalized_corpus = []
    for text in corpus:
        text = html_parser.unescape(text)
        text = expand_contractions(text, CONTRACTION_MAP)
        if lemmatize:
            text = lemmatize_text(text)
        else:
            text = text.lower()
        text = remove_special_characters(text)
        text = remove_stopwords(text)
        if tokenize:
            text = tokenize_text(text)
            normalized_corpus.append(text)
        else:
            normalized_corpus.append(text)

    return normalized_corpus


def parse_document(document):
    document = re.sub('\n', ' ', document)
    if isinstance(document, str):
        document = document
    elif isinstance(document, unicode):
        return unicodedata.normalize('NFKD', document).encode('ascii', 'ignore')
    else:
        raise ValueError('Document is not string or unicode!')
    document = document.strip()
    sentences = nltk.sent_tokenize(document)
    sentences = [sentence.strip() for sentence in sentences]
    return sentences


def speechtotext(fileURL):
    url=BASE_DIR+fileURL
    # Utiliser le fichier audio comme source
    r = sr.Recognizer()
    with sr.AudioFile(url) as source:
        audio = r.record(source)  # Lecture

    # Sphinx Offline API
    title = ""
    try:
        text = r.recognize_sphinx(audio)
        return (text)


    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

def punctuator(inputs):
    data = {
      'text': inputs
    }

    response = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
    return response.text


def build_feature_matrix(documents, feature_type='frequency'):
    feature_type = feature_type.lower().strip()

    if feature_type == 'binary':
        vectorizer = CountVectorizer(binary=True, min_df=1,
                                     ngram_range=(1, 1))
    elif feature_type == 'frequency':
        vectorizer = CountVectorizer(binary=False, min_df=1,
                                     ngram_range=(1, 1))
    elif feature_type == 'tfidf':
        vectorizer = TfidfVectorizer(min_df=1,
                                     ngram_range=(1, 1))
    else:
        raise Exception("Wrong feature type entered. Possible values: 'binary', 'frequency', 'tfidf'")

    feature_matrix = vectorizer.fit_transform(documents).astype(float)

    return vectorizer, feature_matrix

def low_rank_svd(matrix, singular_count=2):
    u, s, vt = svds(matrix, k=singular_count)
    return u, s, vt


def lsa_text_summarizer(DOCUMENT, documents, num_sentences=2,
                        num_topics=2, feature_type='frequency',
                        sv_threshold=0.5):
    vec, dt_matrix = build_feature_matrix(documents,
                                          feature_type=feature_type)
    sentences = parse_document(DOCUMENT)
    norm_sentences = normalize_corpus(sentences, lemmatize=True)
    td_matrix = dt_matrix.transpose()
    td_matrix = td_matrix.multiply(td_matrix > 0)

    u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)
    min_sigma_value = max(s) * sv_threshold
    s[s < min_sigma_value] = 0

    salience_scores = np.sqrt(np.dot(np.square(s), np.square(vt)))
    top_sentence_indices = salience_scores.argsort()[-num_sentences:][::-1]
    top_sentence_indices.sort()
    text=""
    for index in top_sentence_indices:
        text+=sentences[index]
    return text


def textrank_text_summarizer(DOCUMENT, num_sentences=2,
                             feature_type='frequency'):
    sentences = parse_document(DOCUMENT)
    norm_sentences = normalize_corpus(sentences, lemmatize=True)
    vec, dt_matrix = build_feature_matrix(norm_sentences,
                                          feature_type='tfidf')
    similarity_matrix = (dt_matrix * dt_matrix.T)

    similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)
    scores = networkx.pagerank(similarity_graph)

    ranked_sentences = sorted(((score, index)
                               for index, score
                               in scores.items()),
                              reverse=True)

    top_sentence_indices = [ranked_sentences[index][1]
                            for index in range(num_sentences)]
    top_sentence_indices.sort()
    text = ""
    for index in top_sentence_indices:
        text += sentences[index]
    return text


def text_summarization_gensim(text, summary_ratio=0.5):
    summary = summarize(text, split=True, ratio=summary_ratio)

    text=""
    for sentence in summary:
        text+=sentence
    return text




def summarizer(DOCUMENT):
    sentences = parse_document(DOCUMENT)
    norm_sentences = normalize_corpus(sentences, lemmatize=True)
    text = ' '.join(sentences)
    num_sentences = len(norm_sentences)
    #print("\ntext_summarization_gensim\n")
    #text_summarization_gensim(text, summary_ratio=((num_sentences * 0.4) / 13))
    #print("\nlsa_text_summarizer\n")
    #lsa_text_summarizer(DOCUMENT, norm_sentences, num_sentences // 4,
                     #   num_sentences // 2, feature_type='frequency',
                     #   sv_threshold=0.5)
    #print("\ntextrank_text_summarizer\n")
    return textrank_text_summarizer(DOCUMENT, num_sentences // 4,
                             feature_type='tfidf')


from fpdf import FPDF, HTMLMixin


class HTML2PDF(FPDF, HTMLMixin):
    pass


def html2pdf(meeting,invitations,points):
    html = '''<h1 align="center">Minutes of Meeting {0}</h1><hr>
    <p><b>Date: </b> {1}</p>
    <p><b>Time: </b> {2}</p>
    <p><b>Place: </b> {3}</p>
    <br><hr><p><b>Meeting Leader:</b> {4} {5}</p>
   <p><b>Meeting Protractor:</b> {6} {7}</p>
   <br><hr><p><b>Present Collaborators:</b> '''.format(meeting.id,meeting.date,meeting.time,meeting.place,meeting.dirigeant.first_name,meeting.dirigeant.last_name,meeting.rapporteur.first_name,
               meeting.rapporteur.last_name)
    for invitation in invitations:
        if invitation.confirmation=="P":
            html += '''{0} {1},'''.format(invitation.collaborateur.first_name,invitation.collaborateur.last_name)
    html += '''</p><p><b>Absent Collaborators:</b> '''
    for invitation in invitations:
        if invitation.confirmation!="P":
            html += '''{0} {1},'''.format(invitation.collaborateur.first_name,invitation.collaborateur.last_name)
    html += '''</p><br><hr><ul>'''
    for point in points:
            html += '''<li><b>Point {0}:</b> {1}</li><p>{2}</p><br>'''.format(point.ordre,point.titre,point.resume)
    html += '''</ul>'''
    file = HTML2PDF()
    file.add_page()
    file.write_html(html)
    print("sssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    return file.output(MEDIA_DIR+"/pv/meeting{0}.pdf".format(meeting.id))




class MonThread (threading.Thread):
    def __init__(self, url,texts,resumes,i):
        threading.Thread.__init__(self)
        self.url = url
        self.texts=texts
        self.resumes=resumes
        self.i=i

    def run(self):
        text = speechtotext(self.url)
        textP = punctuator(text)
        list = textP.split('.')
        resume = summarizer("""
            {}
            """.format(".\n".join(list[0:])))
        self.texts[self.i]=textP
        self.resumes[self.i] = resume

