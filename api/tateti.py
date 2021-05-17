from .models import Partida, JugadorO, JugadorX, Persona
from rest_framework.response import Response
from rest_framework import status
from .serializers import PartidasSerializer


def desencriptarTateti(tablero, ultimoMovimiento, tipoMovimiento):
    tablero = tablero[1:-1].split(",")
    if tablero[ultimoMovimiento - 1] == "s":

        tablero[ultimoMovimiento - 1] = tipoMovimiento
        return tablero
    else:
        raise "nope"


def resolveTateti(tablero, tipoMovimiento):

    if tablero[0] == tipoMovimiento and tablero[1] == tipoMovimiento and tablero[
            2] == tipoMovimiento or tablero[3] == tipoMovimiento and tablero[
                4] == tipoMovimiento and tablero[5] == tipoMovimiento or tablero[
                    6] == tipoMovimiento and tablero[7] == tipoMovimiento and tablero[
                        8] == tipoMovimiento or tablero[0] == tipoMovimiento and tablero[
                            3] == tipoMovimiento and tablero[6] == tipoMovimiento or tablero[
                                1] == tipoMovimiento and tablero[4] == tipoMovimiento and tablero[
                                    7] == tipoMovimiento or tablero[2] == tipoMovimiento and tablero[
                                        5] == tipoMovimiento and tablero[
                                            8] == tipoMovimiento or tablero[
                                                0] == tipoMovimiento and tablero[
                                                    4] == tipoMovimiento and tablero[
                                                        8] == tipoMovimiento or tablero[
                                                            2] == tipoMovimiento and tablero[
                                                                4] == tipoMovimiento and tablero[
                                                                    6] == tipoMovimiento:
        return True

    else:

        return False


def encriptarTablero(tablero):
    newTablero = ','.join(tablero)
    newTablero = "[" + newTablero + "]"
    return newTablero