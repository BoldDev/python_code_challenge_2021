'use client'

import EpisodeDetailScreen from '@/app/components/screens/EpisodeDetailScreen'
import { useParams, useRouter, useSearchParams } from 'next/navigation'
import { Fragment } from 'react'

export default function EpisodeDetail() {
  // const router = useRouter()
  // const searchParams = useSearchParams()

  // const commentId = searchParams.get('')

  return (
    <Fragment>
      <EpisodeDetailScreen />
    </Fragment>
  )
}
