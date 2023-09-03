import { useRouter } from 'next/router'
import useSWR from 'swr'
import {
  REFRESH_INTERVAL,
  EPISODES_URL,
} from '@/app/tools/clients/got/constants'
import { listEpisodes } from '@/app/tools/clients/got'
import { Episode } from '@/app/tools/clients/got/interface'
import { retrieveEpisode } from '@/app/tools/clients/got'
import { useParams } from 'next/navigation'

export type UseEpisodeHook = {
  episode: Episode | any | null
  error: Error | null
  isValidating: boolean
}

function useEpisode(): UseEpisodeHook {
  const params = useParams()
  const episodeId = params.id

  const { data, error, isValidating } = useSWR(
    {
      url: EPISODES_URL,
      args: { episodeId },
    },
    retrieveEpisode,
    {
      refreshInterval: REFRESH_INTERVAL,
    },
  )

  let episode = data

  return {
    episode,
    error,
    isValidating,
  }
}

export default useEpisode
