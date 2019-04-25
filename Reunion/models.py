from __future__ import unicode_literals

from django.utils import timezone

from django.db import models

from Employe.models import Dirigeant, Collaborateur, Rapporteur
from audiofield.fields import AudioField
import os
from pfa2 import settings


class Reunion(models.Model):
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=100)
    soumise = models.BooleanField(default=False)
    dirigeant = models.ForeignKey(Dirigeant)
    rapporteur = models.ForeignKey(Rapporteur)

    @property
    def hasPV(self):
        if hasattr(self, 'pv'):
            return True
        return False

    @property
    def generatedResume(self):
        generaed=False
        if hasattr(self, 'points'):
            points=self.points.all()
            for p in points:
                if not p.text:
                    generaed=True
                    return generaed
        return False

    @property
    def submitted(self):
       return self.soumise

class PV(models.Model):

    reunion = models.OneToOneField(Reunion, on_delete=models.CASCADE, primary_key=True, related_name="pv")
    file= models.FileField(upload_to="pv",null=True)
    soumis = models.BooleanField(default=False)

class Point(models.Model):
    titre = models.CharField(max_length=255)
    explication = models.TextField()
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE, related_name="points")
    ordre = models.IntegerField()
    diarizationResultat = models.TextField(default=True,null=True)
    text = models.TextField(null=True)
    resume = models.TextField(null=True)
    hasChanged = models.BooleanField(default=False)

    def __str__(self):
        return " {0} ".format(self.ordre)

    @property
    def hasRecord(self):
        if hasattr(self,'enregistrement'):
            return True
        return False

    @property
    def hasResume(self):
        if self.resume!=None:
            return True
        return False




class Enregistrement(models.Model):


    point = models.OneToOneField(Point, on_delete=models.CASCADE, related_name='enregistrement')
    audio_file = models.FileField(upload_to='audio', blank=True, )



class Invitation(models.Model):
    date = models.DateField(null=False,default=timezone.now(),editable=False)
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.CASCADE, related_name="collaborateur_invitations",
                                      related_query_name="collaborateur_invitation")
    meeting = models.ForeignKey(Reunion, on_delete=models.CASCADE, related_name="meeting_invitations",
                                related_query_name="meeting_inviation")
    reponse = models.TextField(null=True)
    choix = (('A', 'Absent'), ('P', 'Present'),)
    confirmation = models.CharField(null=True, choices=choix, max_length=1)


