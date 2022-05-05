# ChooZen-backend

## Getting started:


### Prerequisites:

- Install [Docker](https://docs.docker.com/get-docker/)

### How to launch the backend:

- Open a terminal in the root folder of the project and type:

```
docker-compose build
```

- Then type the following command to create the database :

```
docker-compose up db
```

- wait until database is ready and fully created

- To launch the backend, open a second terminal and type :

```
docker-compose up backend
```

- Once the following output appears, the backend is fully running:

```
choozen-backend-backend-1  | Django version 3.2.9, using settings 'choozenREST.settings'
choozen-backend-backend-1  | Starting development server at http://0.0.0.0:8000/
choozen-backend-backend-1  | Quit the server with CONTROL-C.
```

Django Python REST server, with a mysql db.

Database management :
DROP ALL TABLES : python manage.py migrate choozen zero
RECREATE ALL TABLES : python manage.py syncdb

Launch tests :
python manage.py test