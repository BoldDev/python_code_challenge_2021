import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from API.models import Title
from API.utils import get_episodes, convert_date_format


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Fetch data from OMDB and save it on the models."""

        url = settings.URL["url"]
        api_key = settings.API_KEY["api_key"]
        imdb_id = settings.IMDB_ID["imdb_id"]
        response = requests.get(url + "i=" + imdb_id + "&apikey=" + api_key)
        response_json = response.json()
        if response.status_code == 200:
            if not Title.objects.filter(imdb_id=response_json["imdbID"]).exists():
                Title.objects.create(
                    imdb_id=response_json["imdbID"],
                    title=response_json["Title"],
                    imdb_rating=response_json["imdbRating"],
                    released=convert_date_format(response_json["Released"]),
                    runtime=response_json["Runtime"],
                    director=response_json["Director"],
                    plot=response_json["Plot"],
                    language=response_json["Language"],
                    country=response_json["Country"],
                    poster=response_json["Poster"],
                )
            get_episodes(response_json["totalSeasons"])
