from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import  os

class UserManager(BaseUserManager):
    def create_user(self, password,email):
        if not password:
            raise ValueError("ENTER A PASSWORD")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user= self.create_user(password,email)
        user.is_staff=True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(unique=True)
        date_joined = models.DateTimeField(null=True,default=timezone.now(),editable=False)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(editable=False,default=False)
        objects = UserManager()
        sexe_choix = (('F', 'Female'), ('M', 'Male'))
        sexe = models.CharField(max_length=1, choices=sexe_choix, null=True)
        poste = models.CharField(max_length=255, null=True)
        avatar = models.ImageField(upload_to='profile_pics', blank=True)
        phone = models.IntegerField(null=True)
        first_name = models.CharField(max_length=255, null=True)
        last_name = models.CharField(max_length=255, null=True)

        USERNAME_FIELD = "email"
        REQUIRED_FIELDS=[]

        def __str__(self):
            return "{0}".format(self.email)

        def get_short_name(self):
            return self.email

        def get_long_name(self):
            return "{0}".format(self.email)

        @property
        def isRapporteur(self):
            if hasattr(self, 'employe_rapporteur_related'):
                return True
            return False

        @property
        def isDirigeant(self):
            if hasattr(self, 'employe_dirigeant_related'):
                return True
            return False

        @property
        def isCollaborateur(self):
            if hasattr(self, 'employe_collaborateur_related'):
                return True
            return False
class Employe(models.Model):
    user = models.OneToOneField(User, null=True, related_name='%(app_label)s_%(class)s_related', on_delete=models.CASCADE)

    @property
    def email(self):
        return self.user.email

    @property
    def sexe(self):
        return self.user.sexe

    @property
    def avatar(self):
        return self.user.avatar

    @property
    def poste(self):
        return self.user.poste

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def phone(self):
        return self.user.phone

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    class Meta:
        abstract=True



class Collaborateur(Employe):

    collabore = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Collaborator {0} ".format( self.user.email)


    class Meta:
        verbose_name_plural="Collaborators"



class Rapporteur(Employe):

   rapport = models.IntegerField(null=True)

   def __str__(self):
       return "Protractor {0}  ".format(self.user.email)

   class Meta:
        verbose_name_plural="Protractors"


class Dirigeant(Employe):
    dirige = models.IntegerField(null=True)

    def __str__(self):
        return "Leader {0} ".format(self.user.email)

    class Meta:
        verbose_name_plural="Leaders"