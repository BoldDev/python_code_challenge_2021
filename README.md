# Desafio Bold
A web page/API capable of gathering omdbapi data and delivery via REST/HTTP.<br>

![Solution structure](https://github.com/BrunoLanconi/desafioBold/blob/main/imgs/solution_structure.png)

# Dependencies
Docker<br>
docker-compose

# Variables
`TITLES`: used within bold_services container to determine what titles to gather information.<br>
`API_KEY`: used within bold_services container to access third-party API.<br>
`WEBSITE_NAME`: used within bold_main_site* containers to determine website name.<br>
`hint`: All variables may be found within `docker-compose.yml`.

# Installation
After pulling, navigate to your cloned folder then run `docker-compose up`.<br>
On the first time, Docker may take a while to prepare the environment.

# Configuration
The default configuration is sufficient to validate tasks, but you may also
want to stress it. The default configuration opens testing ports on host -> load balancers:<br>
`main_site` can be accessed through `localhost` default port `80`.<br>
`api` can be accessed through `localhost:3030`.<br>
`api docs` can be accessed through `localhost:3030/swagger/` or `localhost:3030/redoc/`.<br>
<br>
For further history acknowledgment view commit comments [clicking here](https://github.com/BrunoLanconi/desafioBold/commits/main) :)


# More information
Author(s): Bruno Lançoni<br>
version: 1.0.0
