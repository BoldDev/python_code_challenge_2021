from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Show, Season, Episode

import requests
import os

@shared_task
def import_show(show_name):
    '''
    Function that makes an API request to retrieves show information. 
    For the purpose of this coding exercise, only game of thrones 
    is being fetched and saved on database
    '''

    try:
        result = {
            "message": "Show imported with success!",
            "code": 200
        }

        # Make sure we have a key
        if os.environ.get("OMDB_KEY") is None:
            raise requests.exceptions.RequestException("Make sure you have a valid OMDB_KEY on your .env file")

        # Create url to access OMDB API
        api_url = f'http://www.omdbapi.com/?t={show_name}&apikey={os.environ.get("OMDB_KEY")}'

        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response, assuming it's JSON data
            data = response.json()

            show = Show(
                title = data['Title'],
                description = data['Plot'],
                genre = data['Genre'],
                year = data['Year'],
                imdb_id = data['imdbID'],
            )

            # Save into database
            show.save()

            # Fetch and save all seasons for this show
            import_seasons(api_url, show, int(data['totalSeasons']))
        else:
            result['message'] = f"API request to import show failed with status code {response.status_code}"
            result['code'] = response.status_code
    except requests.exceptions.RequestException as e:
        result['message'] = f"API request to import show failed: {e}"
        result['code'] = 400
        return result
    return result

def import_seasons(api_url, show, number_seasons):
    '''
    Fetch all seasons for a specific show and save them into database
    - show(object): show object
    - number_seasons(int): number of seasons that a specific show has
    '''

    for s in range(1, number_seasons + 1):
        # Send a GET request to the API
        response = requests.get(api_url + f'&Season={s}')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response, assuming it's JSON data
            data = response.json()

            total_episodes = len(data['Episodes'])

            season = Season(
                show = show,
                season_number = s,
                total_episodes = str(total_episodes),
            )

            # Save season into database
            season.save()

            # Save each episode
            for e in range(total_episodes):
                episode = Episode(
                    season = season,
                    episode_number = data['Episodes'][e]['Episode'],
                    title = data['Episodes'][e]['Title'],
                    imdb_rating = data['Episodes'][e]['imdbRating'],
                )

                episode.save()
        else:
            raise requests.exceptions.RequestException(f"could not import seasons. Error code: {response.status_code}")
