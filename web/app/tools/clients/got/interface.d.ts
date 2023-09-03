interface Episode {
  title: string
  season_no: string
  episode_no: string
  rating: number
  imdb_id: string
  id: string
}

interface Comment {
  id: string
  text: string
  episode_id: string
}

interface fetchArgsListEpisodes {
  url: string
  args: { awesome: boolean; season: number }
}

interface fetchArgsRetrieveEpisode {
  url: string
  args: { episodeId: string }
}

interface fetchArgsListComments {
  url: string
  args: { episodeId: string }
}

export {
  Episode,
  Comment,
  fetchArgsListEpisodes,
  fetchArgsRetrieveEpisode,
  fetchArgsListComments,
}
