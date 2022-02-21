FROM ubuntu
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Update apt-get, installing cron, python3 and pip3
RUN apt-get update
RUN apt-get -y install cron python3 python3-pip
# Creating links to python3 and pip3
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
# Defining working directory and coping content
WORKDIR /app
COPY ./services .
# Coping utils
COPY ./utils/ .
# Update PIP and install requirements
RUN python -m pip install --upgrade pip &&\
    python -m pip install -r requirements.txt
# Changing permissions so crontab can execute it
RUN chmod 0744 day.sh
# Installing crontab for continuous movies update
RUN (crontab -l ; echo "0 0 * * * /bin/sh /app/day.sh >> /var/log/services.log") | crontab
