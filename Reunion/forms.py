import datetime
from django import forms
from django.db.models.expressions import Date

from .models import *
from django.utils import timezone


def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value


class MeetingForm(forms.ModelForm):
    date = forms.DateField()
    time = forms.TimeField()
    place = forms.CharField(max_length=100)
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "Date"}),
        validators=[present_or_future_date],
    )
    time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Reunion
        fields = (
            "date",
            "time",
            "place",
            "rapporteur",
        )


class PointForm(forms.ModelForm):
    ordre = forms.IntegerField()
    explication = forms.TextInput()

    class Meta:
        model = Point
        fields = ("ordre", "titre", "explication")


class EditPoint(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPoint, self).__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["readonly"] = True

    text = forms.TextInput()
    resume = forms.TextInput()

    class Meta:
        model = Point
        fields = (
            "resume",
            "text",
        )


class RecordForm(forms.ModelForm):
    audio_file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control-file", "type": "file"})
    )

    class Meta:
        model = Enregistrement
        fields = ("audio_file",)
