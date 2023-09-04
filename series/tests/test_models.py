from django.test import TestCase
from series.models import Show, Season, Episode, Comments

class TestModels(TestCase):
    def setUp(self):
        '''
        Initial setup. Create a Show, Season, Episode and a comment
        '''

        # Create a show
        self.show = Show.objects.create(
            title= 'succession',
            description= 'rich people doing business stuff',
            genre= 'drama',
            year= '2018-2023',
            imdb_id= 'some_id',
            created_at = '2023-09-04 10:39:46',
            updated_at = '2023-09-04 10:39:46'
        )

        # Create a season
        self.season = Season.objects.create(
            show= self.show,
            season_number= '1',
            total_episodes= '1',
            created_at = '2023-09-04 10:40:46',
            updated_at = '2023-09-04 10:40:46'
        )

        # Create an episode
        self.episode = Episode.objects.create(
            season= self.season,
            episode_number= '1',
            title= 'Pilot',
            imdb_rating= '8.9',
            created_at = '2023-09-04 10:41:46',
            updated_at = '2023-09-04 10:41:46'
        )

        # Create a comment
        self.comment = Comments.objects.create(
            season= self.season,
            episode= self.episode,
            comment= 'it was good!',
            created_at = '2023-09-04 10:42:46',
            updated_at = '2023-09-04 10:42:46'
        )

    def test_models_ids(self):
        '''
        Assert that an episode belongs to a season and a season belongs to a show.
        And also that a comment belongs to an episode
        '''

        # Show -> Season
        self.assertEquals(self.show.id, self.season.show.id)

        # Season -> Episode
        self.assertEquals(self.season.id, self.episode.season.id)

        # Episode -> Comment
        self.assertEquals(self.episode.id, self.comment.episode.id)

        # Season -> Comment
        self.assertEquals(self.season.id, self.comment.season.id)