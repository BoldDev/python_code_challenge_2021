from typing import Optional

import httpx
from httpx import AsyncClient, Response
from pydantic import parse_obj_as

from .schemas import Season

BASE_URL = "http://www.omdbapi.com/"


# async def get_user(
#     token: Token,
# ) -> Optional[User]:
#     async with AsyncClient(base_url="https://api.github.com") as ac:
#         response: Response = await ac.get(
#             "/user",
#             headers={
#                 "Accept": "application/vnd.github+json",
#                 "Authorization": f"{token.token_type.capitalize()} {token.access_token}",
#                 "X-GitHub-Api-Version": "2022-11-28",
#             },
#         )

#     if response.status_code != httpx.codes.OK:
#         return None

#     response_payload = response.json()
#     user: User = User.parse_obj(response_payload)

#     return user


# http://www.omdbapi.com/?t=Game of Thrones&Season=1&apikey=f45c07f2


async def get_season(
    api_key: str,
    season_no: str,
    movie_title: str = "Game of Thrones",
) -> Season:
    async with AsyncClient(base_url=BASE_URL) as ac:
        response: Response = await ac.get(
            "",
            params={
                "t": movie_title,
                "Season": season_no,
                "apikey": api_key,
            },
        )

    if response.status_code != httpx.codes.OK:
        return None

    response_payload = response.json()
    season: Season = parse_obj_as(Season, response_payload)

    return season
