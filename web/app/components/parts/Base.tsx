import Head from 'next/head'
import React, { Fragment, ReactNode, useEffect } from 'react'

type Props = {
  title?: string
  children: ReactNode
}

function Base({ title = 'GOT-Challenge', children }: Props) {
  useEffect(() => {
    document.title = title
  })

  return <Fragment>{children}</Fragment>
}

export default Base
