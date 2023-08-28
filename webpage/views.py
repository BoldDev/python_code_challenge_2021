import requests
from django.shortcuts import render
from .filter_episodes import (
    filter_episodes,
    filter_episodes_comments,
    filter_episodes_imdb_rating,
)


def home(request):
    api_url = "http://127.0.0.1:8000/titles"
    response = requests.get(api_url).json()
    context = {"response": response}
    return render(request, "home.html", context)


def season_and_episodes_view(request):
    api_url = "http://127.0.0.1:8000/episodes"
    response = requests.get(api_url).json()
    search_episodes = request.GET.get("search_episodes", "")

    filtered_response_by_id = filter_episodes(response, search_episodes)

    context = {
        "filtered_response_by_id": filtered_response_by_id,
        "search_episodes": search_episodes,
    }
    return render(request, "seasons_and_episodes.html", context)


def episodes_imdb_rating(request):
    api_url = "http://127.0.0.1:8000/episodes"
    response = requests.get(api_url).json()

    greater_than_88 = True

    selected_season_number = request.GET.get("season_number")
    all_seasons = selected_season_number is None or selected_season_number == ""

    selected_seasons = {
        "1": selected_season_number == "1",
        "2": selected_season_number == "2",
        "3": selected_season_number == "3",
        "4": selected_season_number == "4",
        "5": selected_season_number == "5",
        "6": selected_season_number == "6",
        "7": selected_season_number == "7",
        "8": selected_season_number == "8",
    }

    filtered_episodes = filter_episodes_imdb_rating(response, greater_than_88)

    if not all_seasons:
        filtered_episodes = [
            episode
            for episode in filtered_episodes
            if episode.get("episode_season") == int(selected_season_number)
        ]

    context = {
        "response": filtered_episodes,
        "season_number": selected_season_number,
        "selected_seasons": selected_seasons,
    }
    return render(request, "imdb_rating.html", context)


def comments_view(request):
    api_url = "http://127.0.0.1:8000/comments"
    response = requests.get(api_url).json()
    search_episodes_comments = request.GET.get("search_episodes_comments", "")

    filtered_response = filter_episodes_comments(response, search_episodes_comments)

    context = {
        "filtered_response": filtered_response,
        "search_episodes_comments": search_episodes_comments,
    }
    return render(request, "comments.html", context)
