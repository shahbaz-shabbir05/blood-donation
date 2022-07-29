FROM python:3.10

RUN mkdir /blood_donation_platform

WORKDIR /blood_donation_platform

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /blood_donation_platform

RUN pip install -r requirements.txt

RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000