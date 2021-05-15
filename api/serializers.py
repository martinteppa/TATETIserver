from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Partida, JugadorX, JugadorO, Persona


class CreatePartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = (JugadorX, )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            "username",
            "password",
        )


class PartidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = "__all__"


class JugadorXSerializer(serializers.ModelSerializer):
    class Meta:
        model = JugadorX
        fields = "__all__"


class JugadorOSerializer(serializers.ModelSerializer):
    class Meta:
        model = JugadorO
        fields = "__all__"
