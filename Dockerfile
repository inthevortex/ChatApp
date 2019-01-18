FROM python:3-stretch

RUN mkdir /chat_app
WORKDIR /chat_app
ADD . /chat_app

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "/chat_app/manage.py", "runserver", "0.0.0.0:8000"]
