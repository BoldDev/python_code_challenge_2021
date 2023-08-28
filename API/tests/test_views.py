from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from API.views import EpisodesViewSet, SeasonsViewSet, TitlesViewSet


class TestEpisodesViewSet(APITestCase):
    def test_get_episodes(self):
        factory = APIRequestFactory()
        view = EpisodesViewSet.as_view({"get": "list"})
        request = factory.get("/api/episodes/")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSeasonsViewSet(APITestCase):
    def test_get_seasons(self):
        factory = APIRequestFactory()
        view = SeasonsViewSet.as_view({"get": "list"})
        request = factory.get("/api/seasons/")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTitlesViewSet(APITestCase):
    def test_get_titles(self):
        factory = APIRequestFactory()
        view = TitlesViewSet.as_view({"get": "list"})
        request = factory.get("/api/titles/")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
