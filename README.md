![https://github.com/Night4dead](https://img.shields.io/badge/Night4dead-2021-%23f514c0)

![https://img.shields.io/badge/IUT%20METZ-LP%202021--2022-%23f514c0](https://img.shields.io/badge/IUT%20METZ-LP%202021--2022-%23f514c0)

----
[Trello](https://trello.com/choozen/home)

[ChooZen-frontend](https://github.com/Night4dead/ChooZen-frontend)

----

# ChooZen-backend

## Realized by :

[Quentin KACZMAREK](https://github.com/Night4dead)

[Kevin BOUDINA](https://github.com/kevinBoudina)

[Martin JOSSIC](https://github.com/sibzou)

[Julien SIBILLE](https://github.com/tehjul)

## Description :

Frontend part of the ChooZen project.

This app allows users to create groups, where they can invite friends, family, etc... 
Then, every user of a group can propose a movie/tv series to watch which will be added to a list. 
The goal is for every member of the group to communicate how much they want to watch something. So users of a group can vote on how soon they want to watch a proposed media.

An average score is then calculated, and on the `"Next"` page, the list of movies that a user has voted is displayed, sorted by the highest average score.

The goal is to simplify the process of choosing what to watch with people you tend to watch movies / tv series with often. When you want to watch something, just go to the `"Next"` page and watch the highest rated movie/tv series.

In further iterations of the app, there will be multiple filters to make the list more precise, like filtering by genre, type (movie, tv series, shortfilm, etc...).

Written in Python with Django framework.

## Getting started:


### Dependencies:

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