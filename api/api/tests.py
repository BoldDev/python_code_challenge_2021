import json
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status


class RequestTestCase(TestCase):
    # In order to reverse to DefaultRouter we need to specify {app_name}:{basename}-suffix
    # https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    titles_url = reverse('api:titles-list')
    seasons_url = reverse('api:seasons-list')
    episodes_url = reverse('api:episodes-list')
    titles_data = {
        "imdb_id": "test",
        "title": "Test",
        "plot": "This is a test case for titles.",
        "imdb_rating": 10.0,
        "poster": "http://www.google.com",
    }
    seasons_data = {
        "season_owner_title": "test",
        "season_number": 1,
    }
    episodes_data = {
        "imdb_id": "test",
        "title": "Test",
        "episode_number": 1,
        "runtime": 10,
        "plot": "This is a test case for episodes.",
        "imdb_rating": 10.0,
        "poster": "http://www.google.com.br",
        "episode_owner_title": "test",
        "episode_owner_season": 1
    }

    def setUp(self) -> None:
        """
        Creates title, season and episode
        """
        self.client.post(self.titles_url, self.titles_data)
        self.client.post(self.seasons_url, self.seasons_data)
        self.client.post(self.episodes_url, self.episodes_data)

        self.titles_response = self.client.get(self.titles_url)
        self.seasons_response = self.client.get(self.seasons_url)
        self.episodes_response = self.client.get(self.episodes_url)

    def test_status(self):
        """
        Tests models status
        """
        for response in [self.titles_response, self.seasons_response, self.episodes_response]:
            tests = response.status_code
            expects = status.HTTP_200_OK

            self.assertEqual(tests, expects)

    def test_titles_fields(self):
        """
        Tests if titles necessary fields exists
        """
        tests = list(json.loads(self.titles_response.content)[0])
        fields = ['imdb_id', 'title', 'genres', 'plot',
                  'languages', 'released', 'imdb_rating', 'poster',
                  'seasons', 'created', 'updated']

        self.assertTrue(set(tests) == set(fields))

    def test_seasons_fields(self):
        """
        Tests if seasons necessary fields exists
        """
        tests = list(json.loads(self.seasons_response.content)[0])
        fields = ['id', 'season_owner_title', 'season_number', 'episodes']

        self.assertTrue(set(tests) == set(fields))

    def test_episodes_fields(self):
        """
        Tests if episodes necessary fields exists
        """
        tests = list(json.loads(self.episodes_response.content)[0])
        fields = ['imdb_id', 'title', 'episode_number', 'plot',
                  'runtime', 'released', 'imdb_rating', 'poster',
                  'episode_owner_title', 'episode_owner_season']

        self.assertTrue(set(tests) == set(fields))

    def test_title_nesting(self):
        """
        Tests if titles nesting has related fields
        """
        tests = list(json.loads(self.titles_response.content)[0]["seasons"][0])
        fields = ['id', 'season_owner_title', 'season_number', 'episodes']

        self.assertTrue(set(tests) == set(fields))

        tests = list(json.loads(self.titles_response.content)[0]["seasons"][0]["episodes"][0])
        fields = ['imdb_id', 'title', 'episode_number', 'plot',
                  'runtime', 'released', 'imdb_rating', 'poster',
                  'episode_owner_title', 'episode_owner_season']

        self.assertTrue(set(tests) == set(fields))
