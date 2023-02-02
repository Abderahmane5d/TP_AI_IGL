from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
# from django.utils.translation import gettext_lazy as _ # other languages

# Create your models here.

# class Contact(models.Model): # a integrer dans user
#     nom = models.CharField(max_length=50)
#     prenom = models.CharField(max_length=100)
#     adresse = models.TextField(null=False) # the db can't have an instance of this model without this attribute
#     email = models.CharField(max_length=100) # email field
#     telephone = models.CharField(max_length=30)

#     def __str__(self) -> str:
#         return self.nom


# class Type(models.Model): # a integrer
#     pass
# class Category(models.Model): # a integrer
#     pass


class UserModel(models.Model):
    nom = models.CharField(max_length=50, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    # the db can't have an instance of this model without this attribute
    adresse = models.TextField(null=False, blank=True)
    email = models.EmailField(('email address'), unique=True)
    telephone = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return self.email


class Location(models.Model):
    wilaya = models.CharField(max_length=50)
    commune = models.CharField(max_length=50)
    adresse = models.TextField(null=False)  # null = False (default)
    coordonnees = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.wilaya


# class Acteur(models.Model): # enlever (user)
#     pass
#     # compteGoogle = models.CharField(max_length=50) # à revoir
#     # contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
# class CustomAccountManager(BaseUserManager):

#     def create_superuser(self, email, nom, prenom, adresse, telephone, password, **otherfields):
#         otherfields.setdefault('is_staff', True)
#         otherfields.setdefault('is_active', True)
#         otherfields.setdefault('is_superuser', True)

#         if otherfields.get('is_staff') == False:
#             raise ValueError('superuser must have is_staff=True')
#         if otherfields.get('is_active') == False:
#             raise ValueError('superuser must have is_active=True')
#         if otherfields.get('is_superuser') == False:
#             raise ValueError('superuser must have is_superuser=True')

#         return self.create_user(email, nom, prenom, adresse, telephone, password, **otherfields)

#     def create_user(self, email, nom, prenom, adresse, telephone, password, **otherfields):
#         if not email:
#             raise ValueError('tu doit introduire un email')
#         email = self.normalize_email(email)
#         # otherfilds.setdefault('username', email)
#         user = self.model(email=email, nom=nom, prenom=prenom,
#                           adresse=adresse, telephone=telephone, **otherfields)
#         user.set_password(password)
#         user.save()
#         return user


# # ajouter le nom et prenom ou bien le username
# class Utilisateur(AbstractBaseUser, PermissionsMixin):
#     nom = models.CharField(max_length=50, blank=True)
#     prenom = models.CharField(max_length=100, blank=True)
#     # the db can't have an instance of this model without this attribute
#     adresse = models.TextField(null=False, blank=True)
#     email = models.EmailField(('email address'), unique=True)  # email field
#     telephone = models.CharField(max_length=30, blank=True)
#     is_staff = models.BooleanField(default=False)
#     # for a secondary check (email sent to user they click and that activate the user and they can login)
#     is_active = models.BooleanField(default=False)

#     object = CustomAccountManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['nom', 'prenom', 'adresse', 'telephone']
#     # AI_Favories = models.ManyToManyField(AI) # à revoir
#     # messages = models.ForeignKey(Message, on_delete=models.CASCADE)
#     # propre_AI = models.ForeignKey(AI, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.email


class Favories(models.Model):
    # related_name : bach ndiro l'accès mel jiha lokhra
    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name='Favories')
    annonce = models.ManyToManyField('AI')


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # contact = models.ForeignKey(Utilisateur, on_delete=models.CASCADE) # à revoir
    conetnt = models.TextField()  # null = False (default)
    utilisateur = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='messages')
    destination = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='notification')

    # def __str__(self) -> str:
    #     return self.conetnt

# class Administrateur(Acteur): # ajouter le nom et prenom ou bien le username
#     nom = models.CharField(max_length=50)
#     prenom = models.CharField(max_length=100)
#     adresse = models.TextField(null=False) # the db can't have an instance of this model without this attribute
#     email = models.CharField(max_length=100) # email field
#     telephone = models.CharField(max_length=30)
#     # AI_signale = models.ForeignKey(AI) # à revoir
#     pass


class AI(models.Model):
    # choices:
    class TypeChoices(models.TextChoices):
        VENTE = 'Vente'
        ECHANGE = 'Echange'
        LOCATION = 'Location'
        LOCATION_POUR_VACANCE = 'Location_pour_vacances'

    class CategoryChoices(models.TextChoices):
        TERRAIN = 'Terrain'
        TERRAIN_AGRICOLE = 'Terrain_agricole'
        APPARTEMENT = 'Appartement'
        MAISON = 'Maison'
        BUNGALOW = 'Bungalow'

    titre = models.CharField(max_length=100)
    description = models.TextField()  # null = False (default)
    surface = models.IntegerField()  # en mètre carré
    price = models.IntegerField()
    images = models.ImageField  # or Images = []
    # type = models.ForeignKey(Type, on_delete=models.CASCADE) # à revoir
    type = models.CharField(choices=TypeChoices.choices,
                            max_length=22)  # null = False (default)
    category = models.CharField(
        choices=CategoryChoices.choices, max_length=16)  # null = False (default)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE)  # à revoir
    owner = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='anonces')
    created = models.DateTimeField(auto_now_add=True)
    # AI_signalees = models.ForeignKey(Signal, on_delete= models.CASCADE, null=True) # admin
    Signal = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.titre
# fav use one one     fav ai many lany
