# python_code_challenge_2021

The goal of this exercise is to test if you know your way around developing REST APIs in Python. You can use any rest
framework and database of your choice. Approach it the way you would an actual long-term project.

Tasks Your task is to build a JSON-based REST API for your frontend developers to consume. You have built a list of user
stories with your colleagues, but you get to decide how to design the API.

We do not need you to implement users or authentication, to reduce the amount of time this exercise will take to
complete. Ideally, you should not spend more than about 4 hours total working time on the exercise, but can be completed
over as long a period as is required.

**We provide you a `.gitignore` and a `.editorconfig` files to help you out creating your solution (you can discard them 
if you wish)**

> NOTE: You can either clone this repo and use it privately, or you can fork it and
> once you've finished you can create a Pull Request, so our team can evaluate your
> code and how well you could know `git` (Not required, but it will be considered
> as a bonus during our analysis)

Required:

- Ability to import all episodes of all seasons of Game of Thrones from OMDb API.

> (You will have to get an APIKey from http://www.omdbapi.com/apikey.aspx to use their API) The APIs that should probably be used are in the following format:
http://www.omdbapi.com/?t=Game of Thrones&Season=1&apikey= http://www.omdbapi.com/?i=&apikey=
(for an episode)

- Design the data model to store this data. You need not store all the attributes of an episode. Select the ones you
  think are important.
- Create GET API endpoints that can return episode information in a list format, as well as information for a specific
  episode, when retrieved by id

In case you have frontend knowledge:

- Provide a frontend landing page consuming the endpoints you've created and show it as beautifully as you'd like (you
  can use Any Frontend library you like, Vanilla JS is also welcomed)

Nice to have:

- Design a data model to store basic text comments to be associated with a specific episode, along with a GET API to
  retrieve all of the comments for an episode
- Design and implement a separate CRUD API for these text comments.
- Ability to filter episodes where imdbRating is greater than 8.8 for a season or for all seasons.
- Write some unit tests
- Docker implementation with a custom `Dockerfile` and a `docker-compose.yml`
  file

Bonus (Completely optional):

- Create a cache layer (any engine you like) to store the data and return it from any endpoint.
- Automated scripts (via Makefile) to make our life easier to test
- Swagger implementation to expose an documented API

![Good Luck](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmeme-generator.com%2Fwp-content%2Fuploads%2Fmememe%2F2019%2F11%2Fmememe_cb8e239ef97eb73a7d04ecf46ed4bf5c-1.jpg&f=1&nofb=1)



Considerações:

- Decidi fazer a separaçao de episodios por season em vez de os juntar todos e ir buscar o episodio nº94. Isto porque a API da OMDB começa sempre no episódio 1 para cada temporada
- Error codes mais especificos e criar customizaveis com error codes especificos (por exemplo, quando nao encontra a serie nº999)
