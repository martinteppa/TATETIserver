from django.urls import path
from .views import Partidas, createPartida, register, login, logout, unirsePartida

urlpatterns = [
    path('', Partidas.as_view()),
    path('crearpartida/', createPartida),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('<str:codigo>/', unirsePartida.as_view()),
]
