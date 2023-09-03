import { useRouter } from 'next/router'
import useSWR from 'swr'
import {
  REFRESH_INTERVAL,
  EPISODES_URL,
} from '@/app/tools/clients/got/constants'
import { listEpisodes } from '@/app/tools/clients/got'
import { Episode } from '@/app/tools/clients/got/interface'

export type UseEpisodesHook = {
  episodes: Episode[] | any | null
  error: Error | null
  isValidating: boolean
}

function useEpisodes(awesome: boolean, season: number): UseEpisodesHook {
  const { data, error, isValidating } = useSWR(
    {
      url: EPISODES_URL,
      args: { awesome, season },
    },
    listEpisodes,
    {
      refreshInterval: REFRESH_INTERVAL,
    },
  )

  let episodes = data

  // if (episodes) {
  //   episodes = data?.filter((warning) => {
  //     return (
  //       warning.idAreaAviso === 'FAR' && warning.awarenessLevelID !== 'green'
  //     )
  //   })
  // }

  return {
    episodes,
    error,
    isValidating,
  }
}

export default useEpisodes
