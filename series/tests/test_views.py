from django.test import TestCase, Client, override_settings
from django.urls import reverse
from series.models import Show

class TestViews(TestCase):

    def setUp(self):
        # Create a test client
        self.client = Client()

        # Get endpoints
        self.fetch_data_url = reverse('fetch')
        self.seasons_url = reverse('seasons')

    def test_fetch_data_without_ajax(self):
        '''
        Test save_episodes view without being sent by ajax
        Should assert a 404 page
        '''
        
        response = self.client.get(self.fetch_data_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'errors/page-404.html')

    def test_get_seasons_error(self):
        '''
        Test get seasons with empty database
        Should assert an error message
        '''

        message= {'error': f'No data found in database. Please import it first.'}
        
        response = self.client.get(self.seasons_url)
        response_message = response.json()

        self.assertEquals(response.status_code, 422)
        self.assertEquals(message, response_message)

    @override_settings(OMDB_IMPORTED=True)
    def test_get_seasons(self):
        '''
        Test get seasons with success
        '''
        # Create a show
        Show.objects.create(
            title= 'Game of Thrones',
            description= 'very bloody',
            genre= 'drama',
            year= '2018-2023',
            imdb_id= 'some_id',
            created_at = '2023-09-04 10:39:46',
            updated_at = '2023-09-04 10:39:46'
        )

        response = self.client.get(self.seasons_url)
        response_message = response.json()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_message['show'], 'Game of Thrones')
        self.assertEquals(response_message['description'], 'very bloody')
        self.assertEquals(response_message['genre'], 'drama')
        self.assertEquals(response_message['year'], '2018-2023')
        self.assertEquals(response_message['imdb_id'], 'some_id')
        self.assertEquals(len(response_message['Seasons']), 0)

    