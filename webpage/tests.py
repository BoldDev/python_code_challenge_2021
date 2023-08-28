from django.test import TestCase, RequestFactory
from unittest.mock import patch
from webpage.views import home, season_and_episodes_view, comments_view, episodes_imdb_rating


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("webpage.views.requests.get")
    def test_home_view(self, mock_get):
        mock_get.return_value.json.return_value = []
        request = self.factory.get("/")
        response = home(request)
        self.assertEqual(
            response.status_code, 200
        ) 

    @patch("webpage.views.requests.get")  
    def test_season_and_episodes_view(self, mock_get):
        mock_get.return_value.json.return_value = []
        request = self.factory.get("/seasons_and_episodes/")
        response = season_and_episodes_view(request)
        self.assertEqual(
            response.status_code, 200
        ) 

    @patch("webpage.views.requests.get")  
    def test_comments_view(self, mock_get):
        mock_get.return_value.json.return_value = []
        request = self.factory.get("/comments/")
        response = comments_view(request)
        self.assertEqual(
            response.status_code, 200
        ) 
    
    @patch("webpage.views.requests.get")  
    def test_imdb_rating_view(self, mock_get):
        mock_get.return_value.json.return_value = []
        request = self.factory.get("/imdb_rating/")
        response = episodes_imdb_rating(request)
        self.assertEqual(
            response.status_code, 200
        ) 