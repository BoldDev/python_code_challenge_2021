import { useRouter } from 'next/router'
import useSWR from 'swr'
import {
  REFRESH_INTERVAL,
  COMMENTS_URL,
} from '@/app/tools/clients/got/constants'
import { listComments, listEpisodes } from '@/app/tools/clients/got'
import { useParams } from 'next/navigation'

export type UseCommentsHook = {
  comments: Comment[] | any | null
  error: Error | null
  isValidating: boolean
}

function useComments(): UseCommentsHook {
  const params = useParams()
  const episodeId = params.id
  const { data, error, isValidating } = useSWR(
    {
      url: COMMENTS_URL,
      args: { episodeId },
    },
    listComments,
    {
      refreshInterval: REFRESH_INTERVAL,
    },
  )

  let comments = data

  return {
    comments,
    error,
    isValidating,
  }
}

export default useComments
