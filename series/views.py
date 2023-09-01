from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import template
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from . import service
from .models import Show, Season, Episode, Comments
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
def index(request):
    '''
    Basic html page that allows to: 
        - Import all game of thrones episodes
        - List and filter them
    '''

    return render(request, "index.html", {
        "segment": "series",
    })

def save_episodes(request):
    '''
    Imports all show episodes and save them into database.
    I decided to make this request 'private' by only allowing button click on main page.
    Trying to do /fetch will result in a 404 error page. The reason behind it was to prevent
    multiple requests.
    '''

    # Check if this request comes from button click in the frontend
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax and request.method == "GET":

        # Fetch show data and save it on database
        response = service.import_show("Game of Thrones")

        data = {"message": response}
        return JsonResponse(data)
    else:
        html_template = loader.get_template('errors/page-404.html')
        return HttpResponse(html_template.render({}, request))

@api_view(['GET'])
@swagger_auto_schema(
    responses={
        200: 'OK',
        422: 'Unprocessable Entity: Import episodes and seasons first',
        500: 'Sever error, probably database related',
    },
    tags=['seasons_all'],
)
def get_seasons(request):
    '''
    Retrieves all seasons for a specific show, in this code challenge for 'Game of Thrones'.
    Some of this logic can also be placed in the model file, in my opinion both ways work
    '''

    # Make sure that data from OMDB is imported
    if not settings.OMDB_IMPORTED:
        return JsonResponse({'error': f'No data found in database. Please import it first.'}, status=422)

    try:
        show = Show.objects.get(title='Game of Thrones')
        seasons = Season.objects.filter(show_id=show.id)

        seasons_data = []
        for season in seasons:
            episodes = Episode.objects.filter(season=season)
            episodes_data = [
                {
                    'episode_number': episode.episode_number,
                    'title': episode.title,
                    'imdb_rating': episode.imdb_rating
                }
                for episode in episodes
            ]

            season_data = {
                'season_number': season.season_number,
                'total_episodes': season.total_episodes,
                'Episodes': episodes_data
            }

            seasons_data.append(season_data)

        data = {
            "show": show.title,
            "genre": show.genre,
            "year": show.year,
            'Seasons': seasons_data
        }

        return JsonResponse(data, status=200)

    except Exception as error:
        return JsonResponse({'error': f'An unnexpected error appeared! Details: {error}'}, status=500)

@api_view(['GET'])
@swagger_auto_schema(
    responses={
        200: 'OK',
        422: 'Unprocessable Entity: Import episodes and seasons first',
        500: 'Sever error, probably database related',
    },
    tags=['seasons_all'],
)
def get_season_by_id(request, season_id):
    '''
    Retrieves all episodes by a specific season.
    Some of this logic can also be placed in the model file, in my opinion both ways work
    '''

    # Make sure that data from OMDB is imported
    if not settings.OMDB_IMPORTED:
        return JsonResponse({'error': f'No data found in database. Please import it first.'}, status=422)
    
    try:
        season = Season.objects.get(id=season_id)

        episodes = Episode.objects.filter(season=season)

        # Serialize the season data
        season_data = {
            "show": season.show.title,
            'season_number': season.season_number,
            'total_episodes': season.total_episodes,
            'Episodes': [
                {
                    'episode_number': episode.episode_number,
                    'title': episode.title,
                    'imdb_rating': episode.imdb_rating
                }
                for episode in episodes
            ]
        }

        return JsonResponse(season_data, status=200)

    except Exception as error:
        return JsonResponse({'error': f'An unnexpected error appeared! Details: {error}'}, status=500)

@api_view(['GET'])
@swagger_auto_schema(
    responses={
        200: 'OK',
        422: 'Unprocessable Entity: Import episodes and seasons first',
        500: 'Sever error, probably database related',
    },
    tags=['seasons_all'],
)  
def get_season_by_id_by_episode(request, season_id, episode_id):
    '''
    Retrieves a specific episode for a specific season.
    Some of this logic can also be placed in the model file, in my opinion both ways work
    '''

    # Make sure that data from OMDB is imported
    if not settings.OMDB_IMPORTED:
        return JsonResponse({'error': f'No data found in database. Please import it first.'}, status=422)
    
    try:
        season = Season.objects.get(id=season_id)
        episode = Episode.objects.get(season=season, episode_number=episode_id)

        # Serialize the season data
        season_data = {
            "show": season.show.title,
            'season_number': season.season_number,
            'total_episodes': season.total_episodes,
            'Episodes': [
                {
                    'episode_number': episode.episode_number,
                    'title': episode.title,
                    'imdb_rating': episode.imdb_rating
                }
            ]
        }

        return JsonResponse(season_data, status=200)

    except Exception as error:
        return JsonResponse({'error': f'An unnexpected error appeared! Details: {error}'}, status=500)

@api_view(['GET'])
@swagger_auto_schema(
    responses={
        200: 'OK',
        422: 'Unprocessable Entity: Import episodes and seasons first',
        500: 'Sever error, probably database related',
    },
    tags=['seasons_all'],
) 
def get_comments_by_id(request, season_id, episode_id):
    '''
    Get all comments of a specific episode by it's ID and also by season ID.
    So, for example, if we want comments from episode 3 of season 5: /comments/5/3
    '''

    # Make sure that data from OMDB is imported
    if not settings.OMDB_IMPORTED:
        return JsonResponse({'error': f'No data found in database. Please import it first.'}, status=422)

    try:
        season = Season.objects.get(id=season_id)
        episode = Episode.objects.get(season=season, episode_number=episode_id)

        comments = Comments.objects.filter(season=season, episode=episode)

        comment_data = {
            'show': season.show.title,
            'season_number': season.season_number,
            'episode_number': episode.episode_number,
            'title': episode.title,
            'Comments': [
                {
                    'id': comment.id,
                    'text': comment.comment,
                    'date': comment.created_at
                }
                for comment in comments
            ]
        }

        return JsonResponse(comment_data, status=200)

    except Exception as error:
        return JsonResponse({'error': f'An unnexpected error appeared! Details: {error}'}, status=500)

def pages(request):
    '''
    Redirect pages for invalid urls
    '''
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        # context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render({}, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('errors/page-404.html')
        return HttpResponse(html_template.render({}, request))
    except:
        html_template = loader.get_template('errors/page-500.html')
        return HttpResponse(html_template.render({}, request))