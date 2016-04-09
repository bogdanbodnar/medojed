# MEDOJED
Hypertext search web-application 

##Installation
Install `Medojed`: 
```
$ git clone git@github.com:bodya3d/medojed.git
$ cd medojed
```
Install and upgrade `virtualenv`:
```
$ pyvenv ./env
$ source env/bin/activate
(env) $ pip install --upgrade pip 
```
Check you're version of `pip` and `python` ( >= 3.5 ) :
```
(env) $ pip --version
```
Install dependency from `requirements.txt` :
```
(env) $ pip install -r ./requirements.txt
```
Create and declare database:

1. Create postgreSQL database `medojed`:
This step depends on your system. You must have installed `PostgreSQL` version `9.5` 
On Ubuntu 14.04 something like this:
```
$ sudo -u postgres createdb medojed
$ sudo -u postgres psql medojed
\>\>\>psql (9.5.2)
\>\>\>Type "help" for help.
medojed=# ALTER USER postgres with encrypted password 'some_password';
\>\>\> ALTER ROLE
medojed=# \quit
```
You also need to setup a `config.py`.

2. Run `model.py`
```
(env) $ python model.py 
```

##Run
Run Medojed from `run.py`:
```
(env) $ python medojed.py
```
Go to http://localhost:8080/ and enjoy!
