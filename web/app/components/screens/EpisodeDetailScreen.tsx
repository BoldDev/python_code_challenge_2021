'use client'

import React, { Fragment, useEffect } from 'react'
import Base from '../parts/Base'
import Layout from '../parts/Layout'
import HeaderSection from '../parts/HeaderSection'
import MainSection from '../parts/MainSection'
import FooterSection from '../parts/FooterSection'
import EpisodeDetail from '../parts/MainSection/EpisodeDetail'

type Props = {}

function EpisodeDetailScreen({}: Props) {
  console.log('Rendering EpisodeDetailScreen')

  return (
    <Base>
      <Layout
        headerSection={<HeaderSection />}
        mainSection={<EpisodeDetail />}
        footerSection={<FooterSection />}
      />
    </Base>
  )
}

export default EpisodeDetailScreen
