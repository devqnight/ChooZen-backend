# ChooZen-backend

Django Python REST server, with a mysql db.

## Getting started:


### Prerequisites:

- Install [Docker](https://docs.docker.com/get-docker/)

### How to launch the backend:

1) Open a terminal in the root folder of the project and type:
```
docker-compose build
```
2) Then type the following command to create the database :
```
docker-compose up db
```
3) Wait until database is ready. The database is fully created when this console output is displayed:
```
Version: '5.7.36'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
```
4) To launch the backend, open a second terminal and type :
```
docker-compose up backend
```
5) Once the following output appears, the backend is fully running:
```
...
choozen-backend-backend-1  | Django version 3.2.9, using settings 'choozenREST.settings'
choozen-backend-backend-1  | Starting development server at http://0.0.0.0:8000/
choozen-backend-backend-1  | Quit the server with CONTROL-C.
...
```
### How to manage the backend:
1) Open a new terminal and execute the following command to access the Django CLI of the project :
```
docker exec -ti choozen-backend-backend-1 /bin/bash
```
2) Now type the following command to make migrations :
```	
python manage.py makemigrations
```
3) Then type the following command to apply the migrations and create all the tables on the database :
```
python manage.py migrate
```

### How to launch tests:
- On the Django CLI, type the following command to launch tests :
```
python manage.py test
```