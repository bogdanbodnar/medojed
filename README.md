# MEDOJED
Hypertext search web-application 

##Installation
Install `Medojed`: 
```
$ git clone git@github.com:bodya3d/medojed.git
$ cd medojed
```
Install and uprgade `virualenv`:
```
$ pyvenv ./env
$ source env/bin/activate
$ pip install --upgrade pip 
```
Check youre version of `pip` and `python` ( >= 3.5.1 ) :
```
$ pip --version
```
Istall dependensy from `requirements.txt` :
```
$ pip install -r ./requirements.txt
```
Declarate and create database from `db_dec.py`:
```
python db_dec.py 
```

##Run
Run Medojed from `run.py`:
```
python run.py
```
Go to http://localhost:8080/ and enjoy!
