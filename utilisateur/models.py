from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ManagerUtilisateur (BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire")
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user=self.create_user(email=email,password=password,**extra_fields)
        user.save()
        return user

class Utilisateur(AbstractBaseUser,PermissionsMixin):
    class Civilite (models.TextChoices):
        CHOIX="","-Choisir une civilité-"
        MONSIEUR="M","Monsieur"
        MADAME="Mme","Madame"
        ENTREPRISE="Entr","Entreprise"

    code=models.CharField(max_length=15,
                          unique=True,
                          editable=False,
                          blank=False,
                          verbose_name="Code utilisateur",
                          )

    slug=models.SlugField(max_length=20,
                          blank=False,
                          )

    email=models.EmailField(max_length=100,
                            unique=True,
                            blank=False,
                            verbose_name="Adresse e-mail",
                            )

    civilite=models.CharField(max_length=4,
                              choices=Civilite.choices,
                              default=Civilite.CHOIX,
                              blank=False,
                              verbose_name="Civilité",
                              )

    nom=models.CharField(max_length=30,
                            blank=False,
                            verbose_name="Nom",
                            )

    prenom=models.CharField(max_length=30,
                         blank=False,
                         verbose_name="Prénom",
                         )

    adresse=models.CharField(max_length=250,
                             blank=False,
                             verbose_name="Adresse",
                             )

    complement=models.CharField(max_length=250,
                                blank=True,
                                verbose_name="Complément d'adresse",
                                )

    cp=models.CharField(max_length=5,
                        blank=False,
                        validators=[RegexValidator(r'^\d{5}$',"Le code postal doit contenir 5 chiffres")],
                        verbose_name="Code postal",
                        )

    ville=models.CharField(max_length=50,
                           blank=False,
                           validators=[
                               RegexValidator(
                                   regex=r"^[a-zA-Zà-ÿÀ-ß\s\(\)'-]+$",
                                   message="Le nom de la ville contient des caractères non autorisés."
                               )
                           ],
                           verbose_name="Ville",
                           )

    tel=models.CharField(max_length=10,
                         blank=True,
                         validators=[RegexValidator(r'^\d{10}$',"Le numéro de téléphone doit contenir 10 chiffres")],
                         verbose_name="Téléphone",
                         )

    creation=models.DateTimeField(auto_now_add=True,
                                       blank=False,
                                       verbose_name="Date de creation",
                                       )

    tentative=models.IntegerField(default=0,
                                  blank=False,
                                  verbose_name="Nombre de tentatives",
                                  )
    blocage=models.DateTimeField(blank=True,
                                 null=True,
                                 verbose_name="Date et heure de blocage")

    is_active=models.BooleanField(default=True,)
    is_staff=models.BooleanField(default=False,)
    is_superuser=models.BooleanField(default=False,)

    USERNAME_FIELD="email"
    objects=ManagerUtilisateur()
    REQUIRED_FIELDS=["civilite","nom","prenom","adresse","cp","ville"]

    def save(self,*args,**kwargs):
        if not self.code:
            self.creation=timezone.now()
            annee=self.creation.year
            mois=f"{self.creation.month:02d}"
            compteur=Utilisateur.objects.filter(creation__year=annee).count()+1

            self.code=f"ID-{mois}{annee}-{compteur:04d}"
            self.slug=slugify(self.code)

        super().save(*args,**kwargs)

    def clean(self):
        super().clean()
        if self.email and isinstance(self.email, str):
            self.email = self.email.lower().strip()
        if self.nom and isinstance(self.nom, str):
            self.nom = self.nom.strip()
            if not self.nom:
                raise ValidationError({'nom': "Ce champ est obligatoire."})
        if self.prenom and isinstance(self.prenom, str):
            self.prenom = self.prenom.strip()
            if not self.prenom:
                raise ValidationError({'prenom': "Ce champ est obligatoire."})
        if self.ville and isinstance(self.ville, str):
            self.ville = self.ville.strip()
            if not self.ville:
                raise ValidationError({'ville': "Ce champ est obligatoire."})

    def __str__(self):
        return f"{self.civilite} {self.prenom.capitalize()} {self.nom.upper()}"