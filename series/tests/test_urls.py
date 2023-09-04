from django.test import SimpleTestCase
from django.urls import reverse, resolve
import series.views as views

class TestUrls(SimpleTestCase):
    '''
    Test urls for series app
    '''
    def test_index_url_resolves(self):
        '''
        Test main url
        '''
        url = reverse('series')
        self.assertEquals(resolve(url).func, views.index)

    def test_fetch_url_resolves(self):
        '''
        Test import data url
        '''
        url = reverse('fetch')
        self.assertEquals(resolve(url).func, views.save_episodes)

    def test_seasons_url_resolves(self):
        '''
        Test get all seasons data url
        '''
        url = reverse('seasons')
        self.assertEquals(resolve(url).func.view_class, views.SeasonsData)

    def test_seasons_by_season_id_url_resolves(self):
        '''
        Test get all seasons by id data url
        '''
        url = reverse('get_season_by_id', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.SeasonsDataByID)

    def test_seasons_by_episode_id_url_resolves(self):
        '''
        Test get all seasons by season and episode id data url
        '''
        url = reverse('get_season_by_id_by_episode', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, views.SeasonsDataByEpisodeID)

    def test_fetch_comments_resolves(self):
        '''
        Test get/create comments for an episode
        '''
        url = reverse('comment_detail', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, views.CommentsData)

    def test_fetch_comments_resolves(self):
        '''
        Test patch/delete comments for an episode
        '''
        url = reverse('comment_handler', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.CommentsHandler)

    def test_pages_resolves(self):
        '''
        Test other pages url
        '''
        url = '/some/arbitrary/url/'
        self.assertEquals(resolve(url).func, views.pages)