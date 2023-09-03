'use client'

import React, { Fragment, useEffect } from 'react'
import Base from '../parts/Base'
import Layout from '../parts/Layout'
import HeaderSection from '../parts/HeaderSection'
import MainSection from '../parts/MainSection'
import FooterSection from '../parts/FooterSection'

type Props = {}

function HomeScreen({}: Props) {
  console.log('Rendering HomeScreen')

  return (
    <Base>
      <Layout
        headerSection={<HeaderSection />}
        mainSection={<MainSection />}
        footerSection={<FooterSection />}
      />
    </Base>
  )
}

export default HomeScreen
