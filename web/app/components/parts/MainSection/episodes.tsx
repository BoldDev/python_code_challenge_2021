import { Episode } from '@/app/tools/clients/got/interface'
import React, { Fragment, useState } from 'react'
import useEpisodes from '../../hooks/useEpisodes'
import { useRouter } from 'next/navigation'

type Props = {}

const Episodes = (props: Props) => {
  const router = useRouter()
  const [awesome, setAwesome] = useState(false)
  const [season, setSeason] = useState(0)
  const { episodes, error, isValidating } = useEpisodes(awesome, season)

  return (
    <Fragment>
      <button
        className="btn"
        onClick={() => {
          setAwesome(false)
          setSeason(0)
        }}
      >
        All episodes
      </button>
      <button className="m-2 btn" onClick={() => setAwesome(!awesome)}>
        Episodes &gt; 8.8
      </button>
      <div className="dropdown dropdown-end">
        <label tabIndex={0} className="m-1 btn">
          season
        </label>
        <ul
          tabIndex={0}
          className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52"
        >
          <li
            onClick={() => {
              setSeason(0)
            }}
          >
            <a>all seasons</a>
          </li>
          <li
            onClick={() => {
              setSeason(1)
            }}
          >
            <a>season 1</a>
          </li>
          <li
            onClick={() => {
              setSeason(2)
            }}
          >
            <a>season 2</a>
          </li>
          <li
            onClick={() => {
              setSeason(3)
            }}
          >
            <a>season 3</a>
          </li>
          <li
            onClick={() => {
              setSeason(4)
            }}
          >
            <a>season 4</a>
          </li>
          <li
            onClick={() => {
              setSeason(5)
            }}
          >
            <a>season 5</a>
          </li>
          <li
            onClick={() => {
              setSeason(6)
            }}
          >
            <a>season 6</a>
          </li>
          <li
            onClick={() => {
              setSeason(7)
            }}
          >
            <a>season 7</a>
          </li>
          <li
            onClick={() => {
              setSeason(8)
            }}
          >
            <a>season 8</a>
          </li>
        </ul>
      </div>
      {episodes && (
        <div className="overflow-x-auto">
          <table className="table">
            {/* head */}
            <thead>
              <tr>
                <th>id</th>
                <th>title</th>
                <th>season</th>
                <th>rating</th>
              </tr>
            </thead>
            <tbody>
              {/* row 1 */}
              {episodes.map((episode: Episode, index: any) => {
                return (
                  <tr
                    key={index}
                    onClick={() => {
                      router.push(`/episodes/${episode.id}`)
                    }}
                  >
                    <th>{episode.id}</th>
                    <td>{episode.title}</td>
                    <td>{episode.season_no}</td>
                    <td>{episode.rating}</td>
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

export default Episodes
