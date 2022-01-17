FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /choozenREST
COPY requirements.txt /choozenREST/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /choozenREST

CMD python manage.py runserver 0.0.0.0:8000
