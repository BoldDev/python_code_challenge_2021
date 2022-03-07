from flask.blueprints import Blueprint
import flask
from flask import json, request
from cache import cache

from app import db_connection

bp = Blueprint('bp_main', __name__, url_prefix='/api/v1.0')
ALLOWED_CHARS = list("-.+():|_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")

table_eps_cols = [
    'Title',
    'Released',
    'Episode',
    'imdbRating',
    'Season'
]

table_comm_cols = [
    'Episode',
    'Season',
    'Comment',
    'Id',
]


def response_gen(response: dict) -> object:
    return flask.Response(json.dumps(response, ensure_ascii=False, separators=(",", ":")),
                          mimetype='application/json')


@bp.route('/season/<int:season_index>/episodes', methods=['GET'])
def get_episodes(season_index: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select {",".join(table_eps_cols)} '
                   'from imdb_episodes '
                   'where Season = ?', (season_index,))
    data_selected = cursor.fetchall()
    cursor.close()
    conn.close()
    result = [
        {
            title: ii[index] for index, title in enumerate(table_eps_cols)
        } for ii in data_selected
    ]
    return response_gen({'Response': True, 'Episodes': result})


@bp.route('/season/<int:season_index>/episode/<int:episode_index>', methods=['GET'])
def get_episode_single(season_index: int, episode_index: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select {",".join(table_eps_cols)} '
                   'from imdb_episodes '
                   'where Season = ? and Episode = ?', (season_index, episode_index,))
    data_selected = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(data_selected):
        single_data = data_selected.pop()
        result = {
            title: single_data[index] for index, title in enumerate(table_eps_cols)
        }
    else:
        result = {}

    return response_gen({'Response': True, 'Episode': result})


@bp.route('/season/<int:season_index>/episode/<int:episode_index>/comments', methods=['GET'])
def get_comments_single(season_index: int, episode_index: int):
    conn = db_connection()
    cursor = conn.cursor()
    columns = [
        'Id',
        'Comment',
    ]
    cursor.execute(f'select {",".join(columns)} '
                   'from imdb_comments '
                   'where Season = ? and Episode = ?', (season_index, episode_index,))
    data_selected = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(data_selected):
        result = [
            {
                title: ii[index] for index, title in enumerate(columns)
            } for ii in data_selected
        ]
    else:
        result = {}

    return response_gen({'Response': True, 'Comments': result})


@bp.route('/season/<int:season_index>/episode/<int:episode_index>/comments/add', methods=['GET'])
def set_comments_single(season_index: int, episode_index: int):
    args = request.args.to_dict()
    comment_text = args.get('c', '')
    comment_text = _sanitize_sql_text(comment_text)

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'insert into imdb_comments({",".join(table_comm_cols)}) '
                   'values (?, ?, ?, (select IFNULL((max(Id)+1), 1) from imdb_comments))',
                   (episode_index, season_index, comment_text,))
    cursor.close()
    conn.commit()
    conn.close()

    return response_gen({'Response': True})


@bp.route('/best-ratings/season/<int:season_index>', methods=['GET'])
@cache.cached(timeout=300)
def get_best_ratings_season(season_index: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select {",".join(table_eps_cols)} from imdb_episodes '
                   f'where cast(imdbRating as float) > ? and '
                   f'Season = ?;',
                   (8.8, season_index))
    data_selected = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(data_selected):
        result = [
            {
                title: ii[index] for index, title in enumerate(table_eps_cols)
            } for ii in data_selected
        ]
    else:
        result = {}

    result = sorted(result, key=lambda d: d['imdbRating'], reverse=True)

    return response_gen({'Response': True, 'Comments': result})


@bp.route('/best-ratings', methods=['GET'])
@cache.cached(timeout=300)
def get_best_ratings():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select {",".join(table_eps_cols)} from imdb_episodes '
                   f'where cast(imdbRating as float) > ?',
                   (8.8,))
    data_selected = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(data_selected):
        result = [
            {
                title: ii[index] for index, title in enumerate(table_eps_cols)
            } for ii in data_selected
        ]
    else:
        result = {}

    result = sorted(result, key=lambda d: d['imdbRating'], reverse=True)

    return response_gen({'Response': True, 'Comments': result})


def _sanitize_sql_text(input_text: str):
    """
    Sanitize text inputs to prevent SQL injection
    :return:
    """
    return ''.join([dd if dd in ALLOWED_CHARS else '' for dd in input_text])


@cache.memoize(timeout=300)
def db_search_episode(search_term: str, max_results: int) -> list:
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select {",".join(table_eps_cols)} '
                   'from imdb_episodes '
                   'where Title like ?'
                   'limit ?', (search_term, max_results,))
    data_selected = cursor.fetchall()
    cursor.close()
    conn.close()
    return data_selected


@bp.route('/search', methods=['GET'])
def search_episode():
    args = request.args.to_dict()

    max_results = min(int(args.get('max', 8)), 8)
    query = args.get('q', '')

    search_term = _sanitize_sql_text(query)
    search_term = f'%{search_term}%'

    if not query:
        return flask.jsonify({'Response': False})

    data_selected = db_search_episode(search_term, max_results)

    result = [
        {
            title: ii[index] for index, title in enumerate(table_eps_cols)
        } for ii in data_selected
    ]

    return flask.jsonify({'Response': True, 'Count': len(data_selected), 'Results': result})
