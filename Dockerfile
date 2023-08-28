FROM python:3.8

WORKDIR /devoteam
# Copy whole project to docker home directory.
COPY . /devoteam
ENV PYTHONUNBUFFERED=1
# Install dependencies
RUN pip install -U pip Pipenv && \
    pipenv lock && \
    pipenv install --dev --system
# Run migrations, django command and runserver
RUN ["python", "./manage.py", "migrate"]
RUN ["python", "./manage.py", "retrieve_omdb"]
EXPOSE 8000

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
