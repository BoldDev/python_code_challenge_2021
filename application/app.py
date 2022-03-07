from flask import Flask
import sqlite3
import os
import requests
from config import Config
from cache import cache

url_prefix = '/api/v1.0/'


def db_connection():
    return sqlite3.connect(os.path.join(Config().DB_SQLITE_DIR, 'local.db'))


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config())
    cache.init_app(flask_app)

    with flask_app.app_context():
        from endpoints import bp
        flask_app.register_blueprint(bp)

        return flask_app


def db_connect():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.executescript('''
    ;;
        ;
        create table if not exists imdb_episodes (
            Title varchar(256) not null,
            Released Date not null,
            Episode int not null,
            imdbRating varchar(8) default null, -- decimal default null,
            Season int not null,
            constraint PK_imdb_episodes PRIMARY KEY(Episode, Season),
            constraint UQ_imdb_episodes UNIQUE (Season, Title)
        )
        ;
        create table if not exists imdb_comments (
            Comment varchar(1024) not null,
            Episode int not null,
            Season int not null,
            Id int not null,
            constraint FK_imdb_comments FOREIGN KEY (Episode, Season)
                references imdb_episodes(Season, Title)
            constraint PK_imdb_comments PRIMARY KEY (Id, Episode, Season)
        )
    ;;
    ''')
    cursor.close()
    conn.commit()
    conn.close()


def data_available() -> bool:
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('select count(*) from imdb_episodes')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    count = result.pop()
    if count:
        if count[0]:
            return True
    return False


def import_data():
    params = {
        't': 'Game of Thrones',
        'apikey': Config().OMDBAPI_KEY,
    }
    url = 'http://www.omdbapi.com/'

    response = requests.get(url, params)
    seasons = response.json().get('totalSeasons', False)

    if isinstance(int(seasons), int):
        for ii in range(1, int(seasons), 1):
            print(f'Importing season {ii} from {params["t"]}...')
            params['Season'] = ii
            response = requests.get(url, params)

            episodes = response.json().get('Episodes', False)

            if not episodes:
                raise RuntimeError('Could not import data. Format unexpected.')

            insert = [
                (ep.get('Title'), ep.get('Released'), int(ep.get('Episode')), ep.get('imdbRating'), ii)
                for ep in episodes
            ]

            conn = db_connection()
            cursor = conn.cursor()
            cursor.executemany('insert into imdb_episodes(Title, Released, Episode, imdbRating, Season) '
                               'values (?, ?, ?, ?, ?)', insert)
            cursor.close()
            conn.commit()
            conn.close()

        return

    raise RuntimeError('Could not import data.')


if __name__ == '__main__':
    db_connect()
    if not data_available():
        import_data()

    create_app().run(host='0.0.0.0', port=Config().API_PORT, debug=True)
