from rest_framework import serializers
from .models import Title, Episode, Season, Comments


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model."""

    class Meta:
        model = Title
        fields = "__all__"


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for Season model."""

    class Meta:
        model = Season
        fields = ("season_number", "season_title")


class EpisodeSerializer(serializers.ModelSerializer):
    """Serializer for Episode model."""

    class Meta:
        model = Episode
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for Comments model."""

    comment_episode = serializers.SlugRelatedField(
        slug_field="title", queryset=Episode.objects.all()
    )

    class Meta:
        model = Comments
        fields = ("comment_episode", "author", "comment")

    def validate(self, data):
        author = data["author"]
        comment_episode = data["comment_episode"]

        # Check if the author has already commented on the episode
        existing_comment = Comments.objects.filter(
            author=author, comment_episode=comment_episode
        ).exists()

        if existing_comment:
            raise serializers.ValidationError(
                "You have already commented on this episode."
            )

        return data
