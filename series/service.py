import requests
import os
from .models import Show, Season, Episode
from django.conf import settings

def import_show(show_name):
    '''
    Function that makes an API request to retrieves show information. 
    For the purpose of this coding exercise, only game of thrones 
    is being fetched and saved on database
    '''

    # If we imported data, no need to do it again
    if settings.OMDB_IMPORTED:
        return "Data is already imported. No need to do it again"

    api_url = f'http://www.omdbapi.com/?t={show_name}&apikey={os.environ.get("OMDB_KEY")}'

    # Send a GET request to the API
    message = "Show imported with success!"

    try:
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
            message = f"API request to import show failed with status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        message = f"API request to import show failed: {e}"
        return message
    
    settings.OMDB_IMPORTED = True
    return message

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
            message = f"API request to import show seasons failed with status code {response.status_code}"

    return True
