from django.db import models
from .title import Title


class Genre(models.Model):
    """
    A model for genre table
    """
    name = models.CharField(max_length=32,
                            blank=False,
                            primary_key=False,
                            help_text="This represents the genre presentation name.",
                            verbose_name="Genre name",
                            )
    genre_owner_title = models.ForeignKey(Title,
                                          on_delete=models.CASCADE,
                                          related_name="genres",
                                          help_text="This represents the genre owner title.",
                                          verbose_name="Genre owner",
                                          )

    def __str__(self):
        return self.name
