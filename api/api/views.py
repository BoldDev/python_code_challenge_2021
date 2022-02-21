from datetime import datetime
from django.http import Http404
from rest_framework import viewsets, generics
from .models.comment import Comment
from .models.episode import Episode
from .models.genre import Genre
from .models.language import Language
from .models.season import Season
from .models.title import Title
from .serializer import CommentsSerializer, EpisodesSerializer, GenresSerializer, LanguagesSerializer,\
    SeasonsSerializer, TitlesSerializer
from django.core.exceptions import ValidationError, FieldError


# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenticated


class CommentsViewSet(viewsets.ModelViewSet):  # all-in-one request method treatment (GET, POST, PUT, UPDATE)
    """
    Shows all comments
    """
    queryset = Comment.objects.all()  # what will be returned
    serializer_class = CommentsSerializer  # who will serialize returned content
    # authentication_classes = [BasicAuthentication]  # authentication method
    # permission_classes = [IsAuthenticated]  # authentication verification method


class EpisodesViewSet(viewsets.ModelViewSet):
    """
    Shows all episodes
    """
    queryset = Episode.objects.all()
    serializer_class = EpisodesSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class GenresViewSet(viewsets.ModelViewSet):
    """
    Shows all genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class LanguagesViewSet(viewsets.ModelViewSet):
    """
    Shows all languages
    """
    queryset = Language.objects.all()
    serializer_class = LanguagesSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class SeasonsViewSet(viewsets.ModelViewSet):
    """
    Shows all seasons
    """
    queryset = Season.objects.all()
    serializer_class = SeasonsSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Shows all titles
    """
    queryset = Title.objects.order_by('-imdb_rating')

    serializer_class = TitlesSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


# Filters


class FilterCommentsList(generics.ListAPIView):
    """
    Shows all comments based on key and value
    """
    def get_queryset(self):
        try:
            if self.kwargs["key"] in ["author", "comment"]:
                query = {self.kwargs["key"] + "__icontains": self.kwargs["value"]}
                queryset = Comment.objects.filter(**query)

            elif self.kwargs["key"] in ["created"]:
                datetime_timestamp = datetime.timestamp(self.kwargs["value"])
                query = {self.kwargs["key"] + "__date_gte": datetime_timestamp}
                queryset = Comment.objects.filter(**query)

            else:
                queryset = Comment.objects.filter(**{self.kwargs["key"]: self.kwargs["value"]})

        except (ValidationError, FieldError, TypeError):
            raise Http404
        return queryset

    serializer_class = CommentsSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class FilterEpisodesList(generics.ListAPIView):
    """
    Shows all episodes based on key and value
    """
    def get_queryset(self):
        try:
            if self.kwargs["key"] in ["imdb_rating", "runtime"]:
                query = {self.kwargs["key"] + "__gte": self.kwargs["value"]}
                queryset = Episode.objects.filter(**query)

            elif self.kwargs["key"] in ["plot", "poster", "title"]:
                query = {self.kwargs["key"] + "__icontains": self.kwargs["value"]}
                queryset = Episode.objects.filter(**query)

            elif self.kwargs["key"] in ["released"]:
                datetime_timestamp = datetime.timestamp(self.kwargs["value"])
                query = {self.kwargs["key"] + "__date_gte": datetime_timestamp}
                queryset = Episode.objects.filter(**query)

            else:
                queryset = Episode.objects.filter(**{self.kwargs["key"]: self.kwargs["value"]})

        except (ValidationError, FieldError, TypeError):
            raise Http404
        return queryset

    serializer_class = EpisodesSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class FilterSeasonsList(generics.ListAPIView):
    """
    Shows all seasons based on key and value
    """

    def get_queryset(self):
        try:
            queryset = Season.objects.filter(**{self.kwargs["key"]: self.kwargs["value"]})

        except (ValidationError, FieldError, TypeError):
            raise Http404
        return queryset

    serializer_class = SeasonsSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class FilterTitlesList(generics.ListAPIView):
    """
    Shows all titles based on key and value
    """
    def get_queryset(self):
        try:
            if self.kwargs["key"] in ["genres", "languages"]:
                query = {self.kwargs["key"] + "__name": self.kwargs["value"].capitalize()}
                queryset = Title.objects.filter(**query).order_by('-imdb_rating')

            elif self.kwargs["key"] in ["imdb_rating"]:
                query = {self.kwargs["key"] + "__gte": self.kwargs["value"]}
                queryset = Title.objects.filter(**query).order_by('-imdb_rating')

            elif self.kwargs["key"] in ["plot", "poster", "title"]:
                query = {self.kwargs["key"] + "__icontains": self.kwargs["value"]}
                queryset = Title.objects.filter(**query).order_by('-imdb_rating')

            elif self.kwargs["key"] in ["released", "created", "updated"]:
                datetime_timestamp = datetime.timestamp(self.kwargs["value"])
                query = {self.kwargs["key"] + "__date_gte": datetime_timestamp}
                queryset = Title.objects.filter(**query).order_by('-imdb_rating')

            else:
                queryset = Title.objects.filter(**{self.kwargs["key"]: self.kwargs["value"]}).order_by('-imdb_rating')

        except (ValidationError, FieldError, TypeError):
            raise Http404
        return queryset

    serializer_class = TitlesSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
