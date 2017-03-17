# MEDOJED / HONEY BADGER
Crawler and search engine based on PageRank algorithm

## Requirements
* Python 3.6 or newer
* pip 9.0.1 or newer
* *may work with previous versions as well*

## Installation
Install `Medojed`:
```
$ git clone git@github.com:bogdanbodnar/medojed.git
$ cd medojed
```

Create virtual environment:
```
python3 -m venv env
```
Activate env:
```
$ source env/bin/activate
```
Check your version of `pip` and `python` :
```
(env) $ pip --version
```
Install dependencies from `requirements.txt` :
```
(env) $ pip install -r ./requirements.txt
```
Create and declare the database:

1. Create PostgreSQL database `medojed`:
This step depends on your system. Project was tested with `PostgreSQL` version `9.6.2`.
   * Ubuntu:
```
$ sudo -u postgres createdb medojed
$ sudo -u postgres psql medojed
>>>psql (9.6.2)
>>>Type "help" for help.
medojed=# ALTER USER postgres with encrypted password 'some_password';
>>> ALTER ROLE
medojed=# \quit
```
Done, go to step 2.

   * Mac:
```
psql postgres
```
   * Check if user `postgres` exists
```
postgres=# \du
```
   * If yes, set his password (same as in `config.py`)
```
postgres=# \password postgres
```
   * If not, create the user and give him necessary permissions
```
postgres=# CREATE ROLE postgres WITH LOGIN PASSWORD 'some_password'
postgres=# ALTER ROLE postgres CREATEDB;
```
   * Confirm with `\du` and exit `\q`

   * Now it's time to create the database
```
psql postgres -U postgres
postgres=> CREATE DATABASE medojed;
```

2. You may also need to change variables in `config.py` accordingly.
3. Run `model.py` (don't forget about the environment `source env/bin/activate`)
```
(env) $ python model.py
```

## Run
Run Medojed from `run.py`:
```
(env) $ python medojed.py
```
Go to http://localhost:8080/ and enjoy!

## Tasks

- [ ] Fix minor bugs
