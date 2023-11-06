FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver