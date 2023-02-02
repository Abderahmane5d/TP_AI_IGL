from django.contrib import admin

# Register your models here.
from .models import Message, Utilisateur, Location, AI, Favories, UserModel


admin.site.register(Message)
admin.site.register(Utilisateur)
admin.site.register(Location)
admin.site.register(AI)
admin.site.register(Favories)
admin.site.register(UserModel)
