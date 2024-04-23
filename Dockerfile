FROM python:latest

RUN mkdir /home/project

WORKDIR /home/project

COPY . .

RUN pip3 install -r requirements.txt

# RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

ENV PORT 8000
EXPOSE 8000

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

