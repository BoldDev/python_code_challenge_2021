from django.urls import path, re_path
from . import views

urlpatterns = [
    # Main page
    path('', views.index, name="series"),

    # 'Private' url to import data from OMDB
    path('fetch/', views.save_episodes, name="fetch"),

    # Fetch all seasons with all episodes
    path('seasons', views.SeasonsData.as_view(), name='seasons'),

    # Fetch a specific season with all episodes
    path('seasons/<int:season_id>', views.SeasonsDataByID.as_view(), name='get_season_by_id'),

    # Fetch a specific season with a specific episode
    path('seasons/<int:season_id>/<int:episode_id>', views.SeasonsDataByEpisodeID.as_view(), name='get_season_by_id_by_episode'),

    # Get Comments by season id and episode id | Create a new comment
    path('comments/<int:season_id>/<int:episode_id>', views.CommentsData.as_view(), name='comment_detail'),

    # PATCH or DELETE comments
    path('comments/<int:comment_id>', views.CommentsHandler.as_view(), name='comment_handler'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]