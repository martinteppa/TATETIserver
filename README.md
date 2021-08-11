# Server Tateti con Django Rest Framework

Lamentablemente he tenido que realizar este practico Gabriel con Django, primero porque tuve problema con un metodo de instalacion de ruby, ya que hay varios. Al final usé un sudo apt-get install ruby pero lo terminé haciendo con Django, ya que estoy mas familiarizado con python(en su version rest) y asi acortar un poco mas el tiempo de codeo. 
Otro problema que tuve fue que no supe como usar el sistema de autenticacion a la hora de debuggear, es por eso que en vez de pasar los tokens por el header, lo hice a traves del body. 


## Instalacion entorno

Hay que tener instalado Python3 3.8.5, Django, Sqlite3 para python(ya viene instalado con el modulo de python) , pip3, y DjangoRestFramework: 
```bash 
pip3 install django
```

```bash 
pip3 install djangorestframework
```
Tambien hay que instalar la aplicacion que permite la coneccion CORS:
```bash 
pip3 install django-cors-headers
```

Se puede crear un entorno virtual con venv e instalar la version de python utilizada. No he testeado si puede funcionar con una version anterior de python, pero creo que pueeeeede funcionar, ya que me he mantenido en lo simple de python en el codigo.

## Migraciones:
dentro de la carpeta donde se encuentre manage.py
```bash 
python3 manage.py makemigrations
```
```bash 
python3 manage.py migrate
```
para arrancar el server:
```bash 
python3 manage.py runserver
```

## EndPoints
Dentro de la carpeta api, el archivo views.py contiene los metodos de los endpoints.


### Register
Hay que registrar dos usuarios para jugar

```bash 
http://127.0.0.1:8000/tateti/register/
method: POST
body: 
{
    "username": "exampleUsername", 
    "password":"examplePassword"
}
```
devolverá un token. 

```bash 
{
    "token": "K6V7D93QSCK0QvNU0U7etwBlcorrCO",
    "username": "exampleUsername"
}
```
Si el nnombre de usuario ya existe dará un 400 bad request:
```bash 
{
    "message": "Usuario ya existente"
}
```
### Login
```bash 
http://127.0.0.1:8000/tateti/login/
method: POST
body:
{
    "username": "exampleUsername",
    "password": "examplePassword",
}
```
devolverá un nuevo token si no tiene
```bash 
202: Acepted
body:
{
    "token": "OcdQVHMsKmNbg1pdQEMW4Dgj5v80g2" 
}
```

Si no existe el usuario, dara un 400, y si la contraseña es incorrecta, un 401

### Logout
```bash 
http://127.0.0.1:8000/tateti/logout/
method: POST
body:
{
    "username": "exampleUsername",
    "token": "exampleToken" 
}
```
Esto eliminará el token del usuario. En caso de tener algun dato invalido, devolverá un 403 forbiden

### Ver partidas EN CURSO 
```bash 
http://127.0.0.1:8000/tateti/
method: GET
```
Esto nos da un listado de todas las partidas que no han sido finalizadas y que no se les ha asignado un segundo usuario

### Crear partida  
```bash 
http://127.0.0.1:8000/tateti/crearpartida/
method: POST
body:
{
    "username": "exampleUsername",
    "token": "exampleToken"
}
```
Crea una partida si: *El usuario no está en una partida actualmente, *Si su token enviado es valido. En caso de que no cumpla alguna de las dos, se responde con un 400 o 401

### Partida 
```bash 
http://127.0.0.1:8000/tateti/<codigoPartida>/
```
Este endpoint tiene tres metodos distintos: GET, POST, PUT. Dependiendo de lo que se quiera hacer

#### GET

En este metodo se retorna la data de la partida especificada en la url

#### POST
```bash 
{
    "username": "exampleUsername",
    "token": "exampleToken"
}
```
El objetivo es asignar el segundo jugador a una partida ya creada. Se valida si: *el usuario no debe estar en una partida, *debe ser autenticado, *que en la partida no esté el segundo jugador , *y que la partida no esté finalizada.

#### PUT
```bash 
{
    "username": "exampleUsername",
    "token": "exampleToken",
    "lastMovement", INTEGER
}
```
Se establece el movimiento del jugador: el que crea la partida es el primero en empezar siempre. Se valida de quien es el turno, si están los jugadores asignados a dicha partida, si estan autenticados. al final de los tres metodos lo que se devuelve siempre es la info de la partida.
Cuando se crea una partida al inicio, lo que se crea es un array con nueve elementos, con valores "s" indicando sin valor.
```bash 
[s,s,s,s,s,s,s,s,s]
```
Este array hay que leerlo en el tateti de izquiera a derecha, de arriba a abajo. A medida que se van realizando puts, se cambian esos valores por X o por O. Tambien se va alternando el booleano "turno", y si termina la partida, el booleano "finished" pasa a true

