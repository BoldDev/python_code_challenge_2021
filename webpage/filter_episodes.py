def filter_episodes(response, search_episodes):
    filtered_episodes = response

    if search_episodes:
        filtered_episodes = [
            episode
            for episode in filtered_episodes
            if search_episodes.lower() in episode.get("imdb_id", "").lower()
        ]

    return filtered_episodes


def filter_episodes_imdb_rating(response, greater_than_88):
    filtered_episodes = response

    if greater_than_88:
        filtered_episodes = [
            episode
            for episode in filtered_episodes
            if episode.get("imdb_rating", "0.0") > "8.8"
            and episode.get("imdb_rating") != "N/A"
        ]

    return filtered_episodes


def filter_episodes_comments(response, search_episodes_comments):
    filtered_episodes = response

    if search_episodes_comments:
        filtered_episodes = [
            episode
            for episode in filtered_episodes
            if search_episodes_comments.lower()
            in episode.get("comment_episode", "").lower()
        ]

    return filtered_episodes
