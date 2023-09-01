from django.db import models
from django.db.models import DateTimeField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import serializers

class DateTimeWithoutTZField(DateTimeField):
    '''
    Override Datetime in postgres to save without timezone
    '''
    def db_type(self, connection):
        return 'timestamp'

class EventManager(models.Manager):
    def get_show(self):

        data = Show.objects.get(title='Game of Thrones')

        return {
            "id": data.id,
            "title": data.title,
            "genre": data.genre,
            "year": data.year
        }
    
    def get_episodes_by_season(self, season_num):
        
        season = Season.objects.filter(season_number=season_num)
        data = Episode.objects.filter(season=season)

        print(data)

        return data

class Show(models.Model):
    '''
    Shows model that saves general information about the serie
    '''

    title = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    genre = models.CharField(max_length=40)
    year = models.CharField(max_length=40)
    imdb_id = models.CharField(max_length=15)
    created_at = DateTimeWithoutTZField(auto_now_add=True)
    updated_at = DateTimeWithoutTZField(auto_now=True)
    objects = EventManager()

    class Meta:
        db_table = 'show'

class Season(models.Model):
    '''
    Seasons model that saves basic season information (including a FK for the show)
    '''

    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    season_number = models.IntegerField(validators=[
            MaxValueValidator(15),
            MinValueValidator(1)
        ], default='1')
    total_episodes = models.CharField(max_length=10)
    created_at = DateTimeWithoutTZField(auto_now_add=True)
    updated_at = DateTimeWithoutTZField(auto_now=True)
    objects = EventManager()

    class Meta:
        db_table = 'season'

class Episode(models.Model):
    '''
    Each episode of a show
    '''

    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    episode_number = models.IntegerField(validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ], default='1')
    title = models.CharField(max_length=40)
    imdb_rating = models.CharField(max_length=5)
    created_at = DateTimeWithoutTZField(auto_now_add=True)
    updated_at = DateTimeWithoutTZField(auto_now=True)
    objects = EventManager()

    class Meta:
        db_table = 'episode'

class Comments(models.Model):
    '''
    Comments for each episode
    '''

    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = DateTimeWithoutTZField(auto_now_add=True)
    updated_at = DateTimeWithoutTZField(auto_now=True)