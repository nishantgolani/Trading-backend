FROM python:3.8

WORKDIR /app

<<<<<<< HEAD
COPY ./requirements.txt .
=======
COPY requirements.txt /app/
>>>>>>> 9760532483ae95be0ec254447b44854be07497bf
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver