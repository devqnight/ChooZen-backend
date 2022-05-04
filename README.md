# ChooZen-backend

-run docker-compose build
-run docker-compose up db
-wait until db is ready
-stop the db with CTRL + C
-run docker-compose up

Backend part of the ChooZen project.

Django Python REST server, with a mysql db.

Database management :
DROP ALL TABLES : python manage.py migrate choozen zero
RECREATE ALL TABLES : python manage.py syncdb

Launch tests :
python manage.py test