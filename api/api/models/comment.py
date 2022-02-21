from django.db import models
from .episode import Episode


class Comment(models.Model):  # model name
    """
    A model for comment table
    """
    author = models.CharField(max_length=32,
                              blank=False,
                              primary_key=True,
                              help_text="This represents the comment's author.",
                              verbose_name="Author",
                              )
    comment = models.CharField(max_length=256,
                               blank=True,
                               null=True,
                               primary_key=False,
                               help_text="This represents the comment.",
                               verbose_name="Comment",
                               )

    comment_owner_episode = models.ForeignKey(Episode,
                                              on_delete=models.CASCADE,
                                              related_name="comments",
                                              help_text="This represents the comment owner episode.",
                                              verbose_name="Comment owner episode",
                                              )
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}'s comment on {self.comment_owner_episode}"
