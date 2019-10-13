FROM python:3.6.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --assume-yes gettext postgresql unzip

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh && bash nodesource_setup.sh
RUN apt-get install --assume-yes nodejs

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

# Install frontend dependencies
ENV FRONTEND_INSTALL_DIR='/frontend'
RUN mkdir $FRONTEND_INSTALL_DIR
COPY package.json $FRONTEND_INSTALL_DIR
RUN npm install yarn -g
RUN cd $FRONTEND_INSTALL_DIR && yarn

ENV C_FORCE_ROOT 1

CMD python manage.py runserver 0.0.0.0:8080
