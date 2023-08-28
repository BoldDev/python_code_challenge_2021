from django.db import models


class Title(models.Model):
    """
    Model for title.
    """

    imdb_id = models.CharField(max_length=20, blank=False, primary_key=True)
    title = models.CharField(
        max_length=120,
        blank=False,
    )
    imdb_rating = models.FloatField(blank=True, null=True)
    released = models.DateField(null=True)
    runtime = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    director = models.CharField(max_length=256, blank=True, null=True)
    plot = models.CharField(
        max_length=256,
    )
    language = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Season(models.Model):
    """
    Model for season.
    """

    season_number = models.PositiveSmallIntegerField(blank=False)
    season_title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="seasons",
    )


class Episode(models.Model):
    """
    Model for episode.
    """

    imdb_id = models.CharField(
        max_length=20,
        blank=False,
        primary_key=True,
    )
    title = models.CharField(
        max_length=96,
        blank=False,
    )
    episode_season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="episodes",
    )
    episode_number = models.PositiveSmallIntegerField(
        blank=False,
        help_text="This represents the episode number.",
        verbose_name="Episode number",
    )
    imdb_rating = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    released = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Comments(models.Model):
    """
    Model for comments.
    """

    author = models.CharField(
        max_length=32,
        blank=False,
        null=False,
    )
    comment = models.CharField(
        max_length=256,
    )

    comment_episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created = models.DateTimeField(auto_now=True)
