
# python_code_challenge_2021
## Solution A

Below are the requirements of the solution presented by the challenge.
For each requirement, there's a brief explanation of what was developed.

Required:

 - **Ability to import all episodes of all seasons of Game of Thrones from OMDb API.** The database loading through OMDb API is being executed before the application is loaded. The information gets stored in a SQL database for future sessions.
 - **Design the data model to store this data.** Only essential information is being stored: Season, Episode, Ratings, Comments, Title.
 - **Create GET API endpoints.**
	 - `/api/v1.0/season/<int:season_index>/episodes` requests all episodes of a specific season
	 - `/api/v1.0/season/<int:season_index>/episode/<int:episode_index>` requests a specific episode of a specific season
	 - `/api/v1.0/season/<int:season_index>/episode/<int:episode_index>/comments` requests comments for an episode
	 - `/api/v1.0/season/<int:season_index>/episode/<int:episode_index>/comments/add` adds a comment for an episode
	 - `/api/v1.0/best-ratings/season/<int:season_index>` gets the best episodes of a season
	 - `/api/v1.0/best-ratings` gets the best episodes of the show overall
	 - `/api/v1.0/search?q=<search term>&max=<maximum number of results>` search engine for episode names

~~In case you have frontend knowledge:~~

~~- Provide a frontend landing page consuming the endpoints you've created and show it as beautifully as you'd like (you~~
  ~~can use Any Frontend library you like, Vanilla JS is also welcomed)~~

Nice to have:

- **Design a data model to store basic text comments to be associated with a specific episode, along with a GET API to   retrieve all of the comments for an episode** 	 
	- `/api/v1.0/season/<int:season_index>/episode/<int:episode_index>/comments` 
	- `/api/v1.0/season/<int:season_index>/episode/<int:episode_index>/comments/add?c=<Comment text, URL-encoded>`
~~- Design and implement a separate CRUD API for these text comments.~~
- **Ability to filter episodes where imdbRating is greater than 8.8 for a season or for all seasons.**
	 - `/api/v1.0/best-ratings/season/<int:season_index>`
	 - `/api/v1.0/best-ratings`
~~- Write some unit tests~~
- **Docker implementation with a custom `Dockerfile` and a `docker-compose.yml` file.** A `docker-compose.yml` file was added. There was no need for a `Dockerfile`.

Bonus (Completely optional):

- **Create a cache layer (any engine you like) to store the data and return it from any endpoint.** A simple cache layer was added. It is possible to extend this cache using many techniques, such as: file system, Redis server, etc. For now, a memory cache is sufficient.
~~- Automated scripts (via Makefile) to make our life easier to test~~
~~- Swagger implementation to expose an documented API~~

