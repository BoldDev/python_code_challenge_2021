from django.db import models


class Title(models.Model):  # model name
    """
    A model for title table
    """
    imdb_id = models.CharField(max_length=10,  # field max length
                               blank=False,  # required
                               primary_key=True,  # is a primary key
                               help_text="This represents the title ID.",  # field guide
                               verbose_name="Title ID",  # human readable field definition
                               )  # field definition
    title = models.CharField(max_length=96,
                             blank=False,
                             primary_key=False,
                             help_text="This represents the title presentation name.",
                             verbose_name="Title name",
                             )
    plot = models.CharField(max_length=256,
                            blank=True,
                            null=True,
                            primary_key=False,
                            help_text="This represents the title plot.",
                            verbose_name="Plot",
                            )
    poster = models.URLField(blank=False,
                             primary_key=False,
                             help_text="This represents the title image URL.",
                             verbose_name="Poster URL",
                             )
    imdb_rating = models.FloatField(blank=True,
                                    null=True,
                                    primary_key=False,
                                    help_text="This represents the title rating.",
                                    verbose_name="Rating",
                                    )
    released = models.DateField(blank=True,
                                null=True,
                                primary_key=False,
                                help_text="This represents the title released date.",
                                verbose_name="Title released date",
                                )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
