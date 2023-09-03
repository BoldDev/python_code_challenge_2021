import {
  Episode,
  fetchArgsListComments,
  fetchArgsListEpisodes,
  fetchArgsRetrieveEpisode,
} from './interface'

async function listEpisodes(
  listEpisodesArgs: fetchArgsListEpisodes,
): Promise<Episode[]> {
  console.log('calling listEpisodes...')
  const { url, args } = listEpisodesArgs
  let url_with_args = url + '?'
  if (args.season > 0) {
    url_with_args = url_with_args + `season=${args.season.toString()}&`
  }
  url_with_args = url_with_args + `awesome=${args.awesome ? 'true' : 'false'}`
  console.log(url_with_args)
  const response = await fetch(url_with_args)
  const episodes: Episode[] = await response.json()
  return episodes
}

async function retrieveEpisode(
  retrieveEpisodeArgs: fetchArgsRetrieveEpisode,
): Promise<Episode> {
  console.log('calling retrieveEpisode...')
  const { url, args } = retrieveEpisodeArgs
  let url_with_args = url + `/${args.episodeId}`

  console.log(url_with_args)
  const response = await fetch(url_with_args)
  const episode: Episode = await response.json()
  return episode
}

async function listComments(
  listCommentsArgs: fetchArgsListComments,
): Promise<Comment[]> {
  console.log('calling listComments...')
  const { url, args } = listCommentsArgs
  let url_with_args = ''
  if (args.episodeId) {
    url_with_args = url + `?episode_id=${args.episodeId}`
  }

  console.log(url_with_args)
  const response = await fetch(url_with_args)
  const comments: Comment[] = await response.json()
  return comments
}

export { listEpisodes, retrieveEpisode, listComments }
