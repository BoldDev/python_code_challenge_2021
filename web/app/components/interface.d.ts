interface MeteoDataItem {
  precipitaProb: number // e.g '0.0'
  tMin: number // e.g '20.9'
  tMax: number // e.g '36.2'
  predWindDir: 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW'
  weatherType: string // e.g 2: Clear sky | 3: Partly cloudy | etc... | check: https://api.ipma.pt/open-data/weather-type-classe.json
  classWindSpeed: string // e.g -99: -- | 1: weak | 2: moderate | 3: strong | 4: very strong | check: https://api.ipma.pt/open-data/wind-speed-daily-classe.json
  // classWindSpeed: -99 | 1 | 2 | 3 | 4 // e.g -99: -- | 1: weak | 2: moderate | 3: strong | 4: very strong | check: https://api.ipma.pt/open-data/wind-speed-daily-classe.json
  longitude: number // e.g '-7.9331'
  latitude: number // e.g '37.0146'
  forecastDate: Date // e.g'2023-07-04'
}

interface Meteo {
  owner: 'IPMA'
  country: 'PT'
  data: MeteoDataItem[]
  globalIdLocal: FARO_GLOBAL_ID
  dateUpdate: Date
}

interface Uv {
  periodId: number // e.g 4
  hourInterval: string // e.g '12h-16h'
  date: Date // e.g '2023-07-06'
  globalIdLocal: number // e.g 3480200
  iUv: number // e.g '7.2'
}

export { Uv, Meteo, MeteoDataItem }
