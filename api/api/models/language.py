from django.db import models
from .title import Title


class Language(models.Model):
    """
    A model for language table
    """
    name = models.CharField(max_length=32,
                            blank=False,
                            primary_key=False,
                            help_text="This represents the language presentation name.",
                            verbose_name="Language name",
                            )
    language_owner_title = models.ForeignKey(Title,
                                             on_delete=models.CASCADE,
                                             related_name='languages',
                                             help_text="This represents the language owner title.",
                                             verbose_name="Language owner",
                                             )

    def __str__(self):
        return self.name
