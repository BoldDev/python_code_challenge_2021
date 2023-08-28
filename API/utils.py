import requests
from datetime import datetime
from django.conf import settings
from django.db.models import Q
from API.models import Title, Season, Episode


def convert_date_format(input_date):
    date_object = datetime.strptime(input_date, "%d %b %Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date


def get_episodes(total_seasons):
    url = settings.URL["url"]
    api_key = settings.API_KEY["api_key"]
    imdb_id = settings.IMDB_ID["imdb_id"]
    for season in range(1, int(total_seasons) + 1):
        title = Title.objects.get(imdb_id=imdb_id)
        if not Season.objects.filter(
            Q(season_title=title) and Q(season_number=season)
        ).exists():
            Season.objects.create(season_title=title, season_number=season)

        response = requests.get(
            url + "i=" + imdb_id + "&Season=" + str(season) + "&apikey=" + api_key
        ).json()

        for episode in response["Episodes"]:
            if not Episode.objects.filter(imdb_id=episode["imdbID"]).exists():
                Episode.objects.create(
                    episode_season=Season.objects.get(
                        Q(season_title=title) and Q(season_number=season)
                    ),
                    imdb_id=episode["imdbID"],
                    title=episode["Title"],
                    episode_number=episode["Episode"],
                    imdb_rating=episode["imdbRating"],
                    released=episode["Released"],
                )
