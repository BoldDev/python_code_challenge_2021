import requests
from django.core.management import BaseCommand
import json

from django.db.models import Q

from show.models import Show, Season, Episode

URL = 'http://www.omdbapi.com/?'
IMDB_ID = 'tt0944947'
API_KEY = '&apikey=31d3cc7a'


def get_episodes(total_seasons):
    for season in range(1, int(total_seasons) + 1):

        # add Season if it doesn't exist
        show = Show.objects.get(imdb_id=IMDB_ID)
        if not Season.objects.filter(Q(show=show) and Q(number=season)).exists():
            Season.objects.create(
                show=show,
                number=season
            )

        r = requests.get(URL + 'i=' + IMDB_ID + '&Season=' + str(season) + API_KEY)
        content = json.loads(r.content)

        for ep in content["Episodes"]:

            # add Episode if it doesn't exist
            if not Episode.objects.filter(imdb_id=ep['imdbID']).exists():
                Episode.objects.create(
                    season=Season.objects.get(Q(show=show) and Q(number=season)),
                    number=ep["Episode"],
                    title=ep["Title"],
                    rating=ep["imdbRating"],
                    imdb_id=ep["imdbID"]
                )

class Command(BaseCommand):
    """
    Technically this can be used for any show, all you have to do is change the IMDB_ID value,
    this will also import updated data, by iterating through the number of total seasons and saving
    the episodes for each of them.
    """
    help = 'Imports GoT episode data from OMDb''s API.'

    def handle(self, *args, **options):
        r = requests.get(URL + 'i=' + IMDB_ID + API_KEY)
        content = json.loads(r.content)
        if r.status_code == 200:

            # add Show if it doesn't exist
            if not Show.objects.filter(imdb_id=content['imdbID']).exists():
                Show.objects.create(
                    title=content['Title'],
                    release_date=content['Released'],
                    imdb_rating=content['imdbRating'],
                    imdb_id=content['imdbID']
                )

            get_episodes(content['totalSeasons'])
        else:
            print(r.status_code, ':', content)


