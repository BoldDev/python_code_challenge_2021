# GOT - Game of thrones (challenge)

This is source code is an implementation of a solution to the `python_code_challenge_2021`.

## Quick start

### Dependencies

- docker
- [direnv](ttps://direnv.net/docs/installation.html)
- make
- python3.9
- pyenv (or alternative) to be able to install all python dependencies locally. To allow running the Typer CLI on the host

### Config

Set the `OMDB_API_KEY=''` env variable with your OMDb API key in both config files:

- `.envs/.local/.api`
- `.envrc`

### direnv

Change directory to the main project folder and run direnv allow to set the environment variables on your host to be able to execute the typer CLI commands:

```bash
direnv allow
```

### Build images and run

```bash
make build
make restart
```

### Apply migrations

```bash
make alembic-upgrade-head
```

### Fetch episodes from OMDb

```bash
make fetch
```

### Clean up the cache/database

```bash
make prune-cache
make prune-database
```

### Frontend

[http://localhost:3000/episodes](http://localhost:3000/episodes)

### Swagger documentation

[http://localhost:9000/api/docs](http://localhost:9000/api/docs)

## Features

- A Makefile serving as the entrypoint for all operations
- A Typer CLI (accessible through the Makefile) to performed the following operations:
  - fetch all episodes from OMDb API and store them into a postgres database and store them into a redis cache db.
  - delete the database containing the stored episodes and comments
  - delete the redis cache containing the episodes and comments
- Redis cache
- Ability to perform the following combination of HTTP methods/resources:

Episodes:

- `GET /episodes`
- `GET /episodes?season=1&awesome=false **`
- `GET /episodes/{episode_id}`

\*\* `awesome=true` episodes are those with an imdb rating > 8.8

Comments:

- `POST /comments`:

```bash
    body: {
        episode_id: <UUID>
    }
```

- `GET /comments?episode_id=<UUID>`
- `GET /comments/{comment_id}`
- `PUT /comments/{comment_id}`

```bash
    body: {
        episode_id: <UUID>
    }
```

- `DELETE /comments/{comment_id}`
