# python_code_challenge_2021

## Installation

1. Change directory to `python_code_challenge_2021`
2. Make a copy of `.env.example` with the name `.env.`
    - Add a random string to `SECRET_KEY`
    - Add your OMDB key into `OMDB_KEY`. (I though of putting my key, but decided not to because of security reasons)

3. Make sure you have docker on your machine
4. Run

```
docker-compose up --build
```

Or '-d' for detachment

```
docker-compose up -d --build
```

5. Go to `localhost:8000/`. There you will have a few instructions.
6. Check the docs `localhost:8000/docs/` to see all endpoints.
7. Have fun! :)

## Considerations

- I decided to import all episodes by clicking the button on main page. I though of doing this during docker compose build but if an error occurred, you would never be able to test anything.

- When doing `/seasons` GET request, I decided to get all episodes divided into Seasons because I realized that OMDB always started at '1' when counting episodes. So, for instance, if I want the 1st episode I need to specify from which season we're talking about. That's why I created `/seasons/{season_id}{episode_id}`. Also, the naming convention can be a little better

- As requested, I added Celery/Redis with 1 worker running. It's only available when fetching all data from OMDB as an example of how it works.

- By adding celery, I have to create 2 new containers (Redis and Celery) to make sure everything works smoothly.

- Database resets everytime docker shuts down on purpose so you guys can check everything from scratch

- Error handling need a little work (more detailed and customizable)

- Django code also needs a bit work, by adding more Django Rest Framework stuff

- Created some tests but a lot more can be done. Sadly, I didn't have the time to run them automatically. So if you want to test, you can go inside docker `python_challenge` container and run:

```
python manage.py test
```
