FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /blood_donation_platform

WORKDIR /blood_donation_platform

COPY . /blood_donation_platform

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
