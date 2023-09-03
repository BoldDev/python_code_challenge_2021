import React, { useState } from 'react'
import Episodes from './episodes'

type Props = {}

function MainSection({}: Props) {
  return (
    <div>
      {/* <h1 className="text-orange-600 text-8xl">Episodes</h1> */}
      <Episodes />
    </div>
  )
}

export default MainSection
