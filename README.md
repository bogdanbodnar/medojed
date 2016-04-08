# MEDOJED
Hypertext search web-application 

##Installation
Install `Medojed`: 
```
$ git clone git@github.com:bodya3d/medojed.git
$ cd medojed
```
Install and uprgade `virtualenv`:
```
$ pyvenv ./env
$ source env/bin/activate
(env) $ pip install --upgrade pip 
```
Check youre version of `pip` and `python` ( >= 3.5 ) :
```
(env) $ pip --version
```
Istall dependency from `requirements.txt` :
```
(env) $ pip install -r ./requirements.txt
```
Declarate and create database from `db_dec.py`:
```
(env) $ python db_dec.py 
```

##Run
Run Medojed from `run.py`:
```
(env) $ python run.py
```
Go to http://localhost:8080/ and enjoy!
