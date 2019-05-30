FROM python:3.6.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --assume-yes gettext postgresql unzip

# Override old pip with newer
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

# Install uwsgi
RUN pip install uWSGI
RUN pip install uwsgitop

RUN mkdir /src
COPY . /src
WORKDIR /src

# Install backend dependencies
RUN pip install -r requirements.txt

ENV C_FORCE_ROOT 1

CMD python manage.py runserver 0.0.0.0:8080
