import { Episode } from '@/app/tools/clients/got/interface'
import React, { Fragment, useState } from 'react'
import useEpisodes from '../../hooks/useEpisodes'
import { useRouter } from 'next/navigation'

type Props = {}

const CommentDetail = (props: Props) => {
  const router = useRouter()
  // const { episodes, error, isValidating } = useEpisodes(awesome, season)

  return <Fragment></Fragment>
}

export default CommentDetail
