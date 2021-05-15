from .models import Partida, JugadorX, JugadorO, Persona, generate_token
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import PartidasSerializer, RegisterSerializer, CreatePartidaSerializer
from rest_framework.decorators import api_view
from .tateti import encriptarTablero, desencriptarTateti, resolveTateti


class Register(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = Persona.objects.create(password=password, username=username)
            dic = serializer.data
            dic["token"] = user.token
            return Response(dic, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario ya existente"})


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
    print(user)
    if user:
        user.token = ""
        user.save()
    return Response({"message": "sesion cerrada"}, status=status.HTTP_200_OK)


class Partidas(generics.ListAPIView):
    queryset = Partida.objects.filter(finished=False)  #.filter(jugadorO=None)

    def get(self, request):

        queryset = self.get_queryset()
        serializer = PartidasSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def createPartida(request):
    user = Persona.objects.get(username=request.data["username"])
    if user:
        if user.enPartida:
            return Response({"message": "Estas En Una Partida"})

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
        return Response({"message": "Usuario incorrecto"})


class unirsePartida(generics.RetrieveAPIView):
    serializer_class = PartidasSerializer

    def get(self, request, **kwargs):
        #codigo
        codigo = kwargs.get('codigo')
        partida = Partida.objects.get(codigo=codigo)

        return Response({"partida": partida.codigo})

    def post(self, request, **kwargs):
        #codigo username token
        user2 = Persona.objects.get(username=request.data["username"])
        if user2 and user2.validateToken(request.data["token"]):
            if user2.enPartida:
                return Response(
                    {"message": "Usted esta en una partida already"})
            else:
                codigo = kwargs.get('codigo')
                partida = Partida.objects.get(codigo=codigo)
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
                nuevoTablero = desencriptarTateti(partida.tablero,
                                                  jugador.lastMovement,
                                                  jugador.tipoMovimiento)
                if resolveTateti(nuevoTablero, jugador.tipoMovimiento):
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
                if partida.turno:
                    partida.turno = False
                else:
                    partida.turno = True
                partida.save()
                return Response(PartidasSerializer(partida).data)

            else:
                return Response(
                    {"message": "esta partida ya habia finalizado"},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Usted no ha sido autenticado"})
