from pydantic import BaseModel


class SeasonEpisode(BaseModel):
    Title: str
    Released: str
    Episode: str
    imdbRating: str
    imdbID: str


class Season(BaseModel):
    Title: str
    Season: str
    totalSeasons: str
    Episodes: list[SeasonEpisode]
    Response: str
