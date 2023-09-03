import Head from 'next/head'
import React, { Fragment, ReactNode } from 'react'
import HeaderSection from './HeaderSection'

type Props = {
  // children: ReactNode
  headerSection: any
  mainSection: any
  footerSection: any
}

function Layout(
  // { children }: Props
  { headerSection, mainSection, footerSection }: Props,
) {
  return (
    <div className="flex flex-col items-center">
      <div className="flex justify-center w-full">{headerSection}</div>
      <div className="flex justify-center w-full">{mainSection}</div>
      <div className="flex justify-center w-full">{footerSection}</div>
    </div>
  )
}

export default Layout
