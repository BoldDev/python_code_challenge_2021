from django.db import models
from .title import Title


class Season(models.Model):  # model name
    """
    A model for season table
    """
    season_number = models.PositiveSmallIntegerField(blank=False,
                                                     primary_key=False,
                                                     help_text="This represents the season number.",
                                                     verbose_name="Season number",
                                                     )
    season_owner_title = models.ForeignKey(Title,  # Foreign key class
                                           on_delete=models.CASCADE,  # What happens when deleted
                                           related_name="seasons",
                                           # The field name linked to related model (for nested only)
                                           help_text="This represents the season owner title.",
                                           verbose_name="Season owner",
                                           )  # Sets a foreign key

    def __str__(self):
        return f"{self.season_owner_title} season {str(self.season_number)}"
