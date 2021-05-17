from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_code():
    length = 8

    while True:
        code = ''.join(random.choices(string.ascii_lowercase, k=length))
        if Partida.objects.filter(codigo=code).count() == 0:
            break

    return code


def generate_token():
    length = 30
    choicesrandom = string.ascii_letters + string.digits
    code = ''.join(random.choices(choicesrandom, k=length))
    return code


class Persona(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    token = models.CharField(default=generate_token, max_length=30)
    enPartida = models.BooleanField(default=False)

    def validateUsername(self, username):

        if self.username == username:
            return False
        else:
            return True

    def validatePassword(self, password):

        if self.password == password:
            return True
        else:
            return False

    def validateToken(self, token):
        if self.token == token:
            return True
        else:
            return False


class JugadorX(models.Model):
    jugador = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipoMovimiento = models.CharField(max_length=1, default="X")
    lastMovement = models.IntegerField(null=True, default=None)


class JugadorO(models.Model):
    jugador = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipoMovimiento = models.CharField(max_length=1, default="O")
    lastMovement = models.IntegerField(null=True, default=None)


class Partida(models.Model):
    codigo = models.CharField(max_length=8, default=generate_code, unique=True)
    finished = models.BooleanField(default=False)
    message = models.CharField(max_length=30, default="")
    turno = models.BooleanField(default=True)
    jugadorX = models.ForeignKey(JugadorX,
                                 on_delete=models.CASCADE,
                                 default=None)
    jugadorO = models.ForeignKey(JugadorO, on_delete=models.CASCADE, null=True)
    tablero = models.CharField(default="[s,s,s,s,s,s,s,s,s]", max_length=50)
    cantidad = models.IntegerField(default=0)