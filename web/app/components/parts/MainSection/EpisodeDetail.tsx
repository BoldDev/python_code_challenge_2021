import { Comment, Episode } from '@/app/tools/clients/got/interface'
import React, { Fragment, useState } from 'react'
import useEpisodes from '../../hooks/useEpisodes'
import { useParams, useRouter } from 'next/navigation'
import useEpisode from '../../hooks/useEpisode'
import useComments from '../../hooks/useComments'

type Props = {}

const EpisodeDetail = (props: Props) => {
  const router = useRouter()
  const {
    episode,
    error: errorEpisode,
    isValidating: isValidatingEpisode,
  } = useEpisode()
  const {
    comments,
    error: errorComments,
    isValidating: isValidatingComments,
  } = useComments()

  console.log(comments)

  return (
    <Fragment>
      {episode && (
        <div className="shadow-xl card card-compact w-96 bg-base-100">
          <div className="card-body">
            <h2 className="card-title">{episode.title}</h2>
            <p>id: {episode.id}</p>
            <p>season: {episode.season_no}</p>
            <p>episode: {episode.episode_no}</p>
            <p>rating: {episode.rating}</p>
            <p>imdb_id: {episode.imdb_id}</p>
            <div></div>
          </div>
        </div>
      )}

      {comments && (
        <div className="overflow-x-auto">
          <table className="table">
            {/* head */}
            <thead>
              <tr>
                <th>id</th>
                <th>text</th>
              </tr>
            </thead>
            <tbody>
              {/* row 1 */}
              {comments.map((comment: Comment, index: any) => {
                return (
                  <tr
                    key={index}
                    onClick={() => {
                      router.push(`/episodes/${episode.id}`)
                    }}
                  >
                    <td>{comment.id}</td>
                    <td>{comment.text}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </Fragment>
  )
}

export default EpisodeDetail
