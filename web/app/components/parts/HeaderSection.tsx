import React, { Fragment, ReactNode } from 'react'

type Props = {}

function HeaderSection({}: Props) {
  return (
    <header>
      <h1 className="text-2xl text-orange-400">
        Game of thrones challenge - UI
      </h1>
    </header>
  )
}

export default HeaderSection
