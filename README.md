# Server Tateti con Django Rest Framework

Lamentablemente he tenido que realizar este practico Gabriel con Django, primero porque tuve problema con un metodo de instalacion de ruby, ya que hay varios. Al final usé un sudo apt-get install ruby pero lo terminé haciendo con Django, ya que estoy mas familiarizado con python y asi acortar un poco mas el tiempo.  

## Instalacion entorno

Hay que tener instalado Python3 3.8.5, o Python 2.7.18, Django, Sqlite3 para python , pip3, y DjangoRestFramework. Particularmente yo usé python3 y pip3
```bash 
pip3 install djangorestframework
```

```bash 
pip3 install django
```

## Migraciones:
```bash 
python3 manage.py makemigrations
```
```bash 
python3 manage.py migrate
```

## EndPoints

### Register
Hay que registrar dos usuarios para jugar

```bash 
http://127.0.0.1:8000/tateti/register
method: POST
body: {"username": "exampleUsername", "password":"examplePassword"}
```
devolverá un token. 

```bash 
{
"token": "K6V7D93QSCK0QvNU0U7etwBlcorrCO",
"username": "asdasd"
}
```
Si el nnombre de usuario ya existe dará un 400 bad request:
{
"message": "Usuario ya existente"
}

### Login
```bash 
http://127.0.0.1:8000/tateti/login
method: POST
body:
{
    "username": "asdasdadaca",
    "password": "asdasd",
  
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
