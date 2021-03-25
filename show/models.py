from django.db import models
from django.db.models import CASCADE


class Show(models.Model):
    title = models.CharField(max_length=250)
    release_date = models.CharField(max_length=50)
    imdb_rating = models.FloatField()
    imdb_id = models.CharField(max_length=50, unique=True, editable=False)

    def __str__(self):
        return self.title


class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return self.show.title + "-" + str(self.number)


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=250)
    rating = models.FloatField()
    imdb_id = models.CharField(max_length=50, unique=True, editable=False)

    def __str__(self):
        return self.season.show.title + '- Season ' + str(self.season.number) + 'Episode ' + str(self.number)


class Comment(models.Model):
    episode = models.ForeignKey(Episode, on_delete=CASCADE)
    comment = models.TextField()

