from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class AiSreializer(serializers.ModelSerializer):
    class Meta:
        model = AI
        fields = '__all__'

class FavoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favories
        fields = '__all__'

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'
    
    def validate(self, attrs):
        email_exists = Utilisateur.object.all().filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError("Enter another email this one has been already used")
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user=super().create(validated_data)
        user.set_password(password)
        user.save()
        return user