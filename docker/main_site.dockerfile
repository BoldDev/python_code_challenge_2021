FROM ubuntu
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Avoiding tzdata installation stuckness
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo
# Installing python3, pip3, venv3, apache and mod_wsgi
RUN apt-get update
RUN apt-get -y install python3 python3-pip python3.8-venv apache2 libapache2-mod-wsgi-py3
RUN apachectl -M
# Creating links to python3 and pip3
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
# Defining working directory, coping content, coping wait_for_django_parent.py and coping wait_for_database.py
WORKDIR /app
COPY ./main_site .
COPY ./utils/wait_for_database.py .
COPY ./utils/wait_for_django_parent.py .
# Coping utils/services
COPY ./utils/services/ ./pages/services/
# Installing mysqlclient dependencies
RUN apt-get -y install python3-dev default-libmysqlclient-dev build-essential
# Updating PIP and install requirements
RUN python -m pip install --upgrade pip &&\
    python -m pip install -r requirements.txt
# Creating virtual environment inheriting root packages
RUN python -m venv venv --system-site-packages
# Creating Django key
RUN key=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'); \echo "keys = {'SECRET_KEY': '$key', }" > /app/main_site/keys.py
