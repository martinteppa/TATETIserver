from .models import Partida, JugadorX, JugadorO, Persona, generate_token
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import PartidasSerializer, RegisterSerializer, CreatePartidaSerializer
from rest_framework.decorators import api_view
from .tateti import encriptarTablero, desencriptarTateti, resolveTateti


@api_view(["POST"])
def register(request):
    username = request.data["username"]
    password = request.data["password"]
    user = Persona.objects.filter(username=username).first()
    if not user and password != "":
        user = Persona.objects.create(password=password, username=username)
        dic = {}
        dic["username"] = username
        dic["token"] = user.token
        return Response(dic, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Usuario ya existente"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]
    user = Persona.objects.filter(username=username).first()
    if not user:
        return Response({"error": "usuario inexistente"},
                        status=status.HTTP_400_BAD_REQUEST)
    elif not user.validatePassword(password):
        return Response({"error": "contraseña incorrecta"},
                        status=status.HTTP_401_UNAUTHORIZED)
    else:
        if not user.token:
            newtoken = generate_token()
            user.token = newtoken
            user.save()
        return Response({"token": user.token}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def logout(request):

    user = Persona.objects.get(token=request.data["token"])
     
    if user.validateUsername(username=request.data["username"]):
        user.token = ""
        user.save()
        return Response({"message": "sesion cerrada"},
                        status=status.HTTP_200_OK)
    else:
        return Response({"message": "data invalida"},
                        status=status.HTTP_403_FORBIDDEN)


class Partidas(generics.ListAPIView):
    queryset = Partida.objects.filter(finished=False).filter(jugadorO=None)

    def get(self, request):

        queryset = self.get_queryset()
        serializer = PartidasSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def createPartida(request):
    user = Persona.objects.get(username=request.data["username"])
    if user:
        if user.enPartida:
            return Response({"message": "Estas En Una Partida"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if user.validateToken(request.data["token"]):
            jugador = JugadorX.objects.create(jugador=user)
            user.enPartida = True
            user.save()
            partida = Partida.objects.create(jugadorX=jugador)
            partida.save()
            serializer = PartidasSerializer(partida)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Token incorrecto"},
                            status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Usuario incorrecto"},
                        status=status.HTTP_400_BAD_REQUEST)


class unirsePartida(generics.RetrieveAPIView):
    serializer_class = PartidasSerializer

    def get(self, request, **kwargs):
        #codigo
        codigo = kwargs.get('codigo')
        partida = Partida.objects.get(codigo=codigo)
        if partida:
            return Response(PartidasSerializer(partida).data,
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bad Request"},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        #codigo username token
        user2 = Persona.objects.get(username=request.data["username"])
        if user2 and user2.validateToken(request.data["token"]):
            if user2.enPartida:
                return Response(
                    {"message": "Usted esta en una partida already"},
                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                codigo = kwargs.get('codigo')
                partida = Partida.objects.get(codigo=codigo)
                if partida.jugadorO and partida.finished:
                    return Response({"message": "Partida Completa already"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    jugador2 = JugadorO.objects.create(jugador=user2)
                    user2.enPartida = True
                    user2.save()
                    partida.jugadorO = jugador2
                    partida.save()
                    return Response(PartidasSerializer(partida).data)
        else:
            return Response({"message": "Usted no ha sido autenticado"})

    def put(self, request, *args, **kwargs):
        #codigo #token #username #lastMovement
        user = Persona.objects.get(username=request.data["username"])
        if user and user.validateToken(request.data["token"]):
            codigo = kwargs.get('codigo')
            partida = Partida.objects.get(codigo=codigo)

            if not partida.finished and partida.jugadorO:

                if user == partida.jugadorX.jugador and partida.turno:
                    jugador = JugadorX.objects.get(id=partida.jugadorX.id)

                elif user == partida.jugadorO.jugador and not partida.turno:
                    jugador = JugadorO.objects.get(id=partida.jugadorX.id)
                else:

                    return Response({"message": "No es su turno, espere"},
                                    status=status.HTTP_400_BAD_REQUEST)

                jugador.lastMovement = request.data["lastMovement"]
                jugador.save()
                try:
                    nuevoTablero = desencriptarTateti(partida.tablero,
                                                      jugador.lastMovement,
                                                      jugador.tipoMovimiento)
                except:
                    return Response({"message": "cuadrado ya utilizado"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if resolveTateti(
                        nuevoTablero,
                        jugador.tipoMovimiento) or partida.cantidad == 9:
                    if partida.cantidad == 9:
                        partida.message = "Empataron "
                    else:
                        partida.message = "Gano el jugador " + jugador.tipoMovimiento
                    partida.finished = True
                    user1 = Persona.objects.get(
                        username=partida.jugadorX.jugador.username)
                    user2 = Persona.objects.get(
                        username=partida.jugadorO.jugador.username)
                    user1.enPartida = False
                    user2.enPartida = False
                    user1.save()
                    user2.save()
                else:
                    partida.message = "Turno del otro jugador "
                nuevoTablero = encriptarTablero(nuevoTablero)
                partida.tablero = nuevoTablero
                partida.cantidad += 1
                partida.turno = not partida.turno
                partida.save()
                return Response(PartidasSerializer(partida).data)

            else:
                return Response(
                    {"message": "esta partida ya habia finalizado"},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Usted no ha sido autenticado"},
                            status=status.HTTP_401_UNAUTHORIZED)
