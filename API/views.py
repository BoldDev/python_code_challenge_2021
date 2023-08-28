from rest_framework import viewsets, filters
from API.models import Title, Season, Episode, Comments
from API.serializers import (
    CommentsSerializer,
    EpisodeSerializer,
    SeasonSerializer,
    TitleSerializer,
)


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Shows all titles.
    """

    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class SeasonsViewSet(viewsets.ModelViewSet):
    """
    Shows all seasons.
    """

    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


class EpisodesViewSet(viewsets.ModelViewSet):
    """
    Shows all episodes.
    """

    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["imdb_id"]


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Shows all comments.
    """

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
