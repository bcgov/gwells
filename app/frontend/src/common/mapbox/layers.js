import { defaultsDeep } from 'lodash'

const VECTOR_TILE_SERVER = `${window.location.protocol}//${window.location.host}${process.env.VUE_APP_VECTOR_TILE_BASE_URL}`

export const WELLS_SOURCE_ID = 'postgis_ftw.gwells_well_view'
export const WELLS_BASE_AND_ARTESIAN_LAYER_ID = 'wells-with-artesian'
export const WELLS_UNCORRELATED_LAYER_ID = 'wells-uncorrelated'
export const WELLS_EMS_LAYER_ID = 'wells-ems'
export const WELLS_OBSERVATION_LAYER_ID = 'wells-observation'

export const SEARCHED_WELLS_SOURCE_ID = 'searched-wells'
export const SEARCHED_WELLS_LAYER_ID = 'highlight-wells-with-artesian'

export const FOCUSED_WELLS_SOURCE_ID = 'focused-wells'
export const FOCUSED_WELLS_LAYER_ID = 'focused-wells'
export const FOCUSED_WELLS_ARTESIAN_LAYER_ID = 'focused-wells-artesian'
export const FOCUSED_WELL_IMAGE_ID = 'focused-well-image'
export const FOCUSED_WELL_ARTESIAN_IMAGE_ID = 'focused-artesian-well-image'

export const AQUIFERS_SOURCE_ID = 'postgis_ftw.gwells_aquifer_view'
export const AQUIFERS_LINE_LAYER_ID = 'aquifer-line'
export const AQUIFERS_FILL_LAYER_ID = 'aquifer-fill'

export const DATABC_ROADS_SOURCE_ID = 'DATABC-roads-source'
export const DATABC_ROADS_LAYER_ID = 'DATABC-roads-layer'

export const DATABC_CADASTREL_SOURCE_ID = 'DATABC-cadastrels-source'
export const DATABC_CADASTREL_LAYER_ID = 'DATABC-cadastrels-layer'

export const DATABC_ECOCAT_SOURCE_ID = 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW'
export const DATABC_ECOCAT_LAYER_ID = 'DATABC-ecocat-layer'

export const DATABC_WATER_LICENCES_SOURCE_ID = 'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV'
export const DATABC_SURFACE_WATER_LICENCES_LAYER_ID = 'DATABC-surface-water-licences-layer'
export const DATABC_GROUND_WATER_LICENCES_LAYER_ID = 'DATABC-ground-water-licences-layer'

export const ECOCAT_FW_FEATURE_CODE = 'WC00015300'

export function vectorTileServerUrl (sourceLayerName) {
  return `${VECTOR_TILE_SERVER}${sourceLayerName}/{z}/{x}/{y}.pbf`
}

export function vectorSourceConfig (sourceLayerName, options = {}) {
  return {
    type: 'vector',
    tiles: [ vectorTileServerUrl(sourceLayerName) ],
    minzoom: 4,
    maxzoom: 17,
    ...options
  }
}

export const DATABC_ROADS_SOURCE = {
  type: 'raster',
  tiles: [
    // NOTE: added ?env= param because of WATER-1183
    `https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/{z}/{y}/{x}?env=${window.location.hostname}`
  ],
  minzoom: 0,
  maxzoom: 17,
  tileSize: 256
}

export const DATABC_CADASTREL_SOURCE = {
  type: 'raster',
  tiles: [
    'https://openmaps.gov.bc.ca/geo/pub/ows?&service=WMS&request=GetMap&layers=pub%3AWHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW&format=image%2Fpng&transparent=true&version=1.1.1&width=256&height=256&srs=EPSG:3857&bbox={bbox-epsg-3857}'
  ],
  minzoom: 14,
  maxzoom: 24,
  tileSize: 256
}

export const DATABC_ECOCAT_SOURCE = {
  type: 'vector',
  tiles: [
    'https://openmaps.gov.bc.ca/geo/pub/ows?&service=WMS&request=GetMap&layers=pub%3AWHSE_FISH.ACAT_REPORT_POINT_PUB_SVW&format=application/x-protobuf;type=mapbox-vector&version=1.1.1&width=512&height=512&srs=EPSG:3857&bbox={bbox-epsg-3857}'
  ],
  minzoom: 7,
  maxzoom: 24,
  tileSize: 512,
  promoteId: 'REPORT_ID'
}

export const DATABC_WATER_LICENCES_SOURCE = {
  type: 'vector',
  tiles: [
    'https://openmaps.gov.bc.ca/geo/pub/ows?&service=WMS&request=GetMap&layers=pub%3AWHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV&format=application/x-protobuf;type=mapbox-vector&version=1.1.1&width=512&height=512&srs=EPSG:3857&bbox={bbox-epsg-3857}'
  ],
  minzoom: 7,
  maxzoom: 24,
  tileSize: 512,
  promoteId: 'LICENCE_NUMBER'
}

export const DATABC_ROADS_LAYER = {
  type: 'raster',
  id: DATABC_ROADS_LAYER_ID,
  source: DATABC_ROADS_SOURCE_ID
}

export const DATABC_CADASTREL_LAYER = {
  type: 'raster',
  id: DATABC_CADASTREL_LAYER_ID,
  source: DATABC_CADASTREL_SOURCE_ID
}

export const WELLS_SOURCE = vectorSourceConfig(WELLS_SOURCE_ID, { promoteId: 'well_tag_number' })
export const AQUIFERS_SOURCE = vectorSourceConfig(AQUIFERS_SOURCE_ID, { promoteId: 'aquifer_id' })

function vectorLayerConfig (id, source, painttype, paint = {}, layout = {}, filter = null) {
  const cfg = {
    id,
    source,
    'source-layer': source,
    type: painttype,
    paint,
    layout
  }

  if (filter) {
    cfg.filter = filter
  }

  return cfg
}

function layerConfig (id, source, painttype, paint = {}, layout = {}) {
  return {
    id,
    source,
    type: painttype,
    paint,
    layout
  }
}

// Adds mouse event listeners to the map to highlight the hovered aquifer
export function setupAquiferHover (map, aquifersFillLayerId) {
  map.hoveredStateId = null

  map.on('mousemove', aquifersFillLayerId, (e) => {
    if (e.features.length > 0) {
      const newHoveredStateId = e.features[0].id
      if (newHoveredStateId !== map.hoveredStateId) {
        if (map.hoveredStateId) { // un-set hover state on previously hovered asquifer
          toggleAquiferHover(map, map.hoveredStateId, false)
        }

        toggleAquiferHover(map, newHoveredStateId, true)
        map.hoveredStateId = newHoveredStateId
      }
    }
  })

  // When the mouse leaves the state-fill layer, update the un-set the hover state of the
  // previously hovered aquifer.
  map.on('mouseleave', aquifersFillLayerId, () => {
    if (map.hoveredStateId) {
      toggleAquiferHover(map, map.hoveredStateId, false)
    }
    map.hoveredStateId = null
  })
}

export function toggleAquiferHover (map, aquiferId, hoveredState) {
  map.setFeatureState(
    { source: AQUIFERS_SOURCE_ID, id: aquiferId, sourceLayer: AQUIFERS_SOURCE_ID },
    { hover: hoveredState }
  )
}

export function ecoCatLayer (options = {}) {
  const layerId = options.id || DATABC_ECOCAT_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': [
      'case',
      ['==', ['get', 'FEATURE_CODE'], ECOCAT_FW_FEATURE_CODE], '#000',
      '#999'
    ],
    'circle-radius': 5
  })

  return vectorLayerConfig(layerId, options.source || DATABC_ECOCAT_SOURCE_ID, options.layerType || 'circle', styles, options.layout)
}

export function surfaceWaterLicencesLayer (options = {}) {
  const layerId = options.id || DATABC_SURFACE_WATER_LICENCES_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': '#5ED900',
    'circle-radius': 4,
    'circle-stroke-color': '#000',
    'circle-stroke-width': 0.75
  })

  const filter = [
    'all', ['in', ['get', 'POD_SUBTYPE'], 'POD'], ['==', ['get', 'POD_STATUS'], 'Active']
  ]

  return vectorLayerConfig(layerId, options.source || DATABC_WATER_LICENCES_SOURCE_ID, options.layerType || 'circle', styles, options.layout, filter)
}

export function groundWaterLicencesLayer (options = {}) {
  const layerId = options.id || DATABC_GROUND_WATER_LICENCES_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': 'yellow',
    'circle-radius': 4,
    'circle-stroke-color': '#000',
    'circle-stroke-width': 0.75
  })

  const filter = [
    'all', ['!', ['in', ['get', 'POD_SUBTYPE'], 'POD']], ['==', ['get', 'POD_STATUS'], 'Active']
  ]

  return vectorLayerConfig(layerId, options.source || DATABC_WATER_LICENCES_SOURCE_ID, options.layerType || 'circle', styles, options.layout, filter)
}

// Builds MapBox layer config object for wells with artesian ones with a fuchsia outline
export function wellsBaseAndArtesianLayer (options = {}) {
  const layerId = options.id || WELLS_BASE_AND_ARTESIAN_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': [
      'case',
      ['to-boolean', ['get', 'artesian']], '#1099FE',
      '#0162FE'
    ],
    'circle-radius': 3,
    'circle-stroke-color': [
      'case',
      ['to-boolean', ['get', 'artesian']], '#EE14CA',
      'transparent'
    ],
    'circle-stroke-width': 1
  })

  const filter = options.filter || wellLayerFilter(false)

  return vectorLayerConfig(layerId, options.source || WELLS_SOURCE_ID, options.layerType || 'circle', styles, options.layout, filter)
}

// Builds MapBox layer config object for searched wells with artesian ones with a fuchsia outline
export function searchedWellsLayer (options = {}) {
  const layerId = options.id || SEARCHED_WELLS_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': [
      'case',
      ['to-boolean', ['get', 'artesian_conditions']], '#1099FE',
      '#0162FE'
    ],
    'circle-radius': 5,
    'circle-stroke-color': [
      'case',
      ['to-boolean', ['get', 'artesian_conditions']], '#EE14CA',
      'black'
    ],
    'circle-stroke-width': 2
  })

  return layerConfig(layerId, options.source || SEARCHED_WELLS_SOURCE_ID, options.layerType || 'circle', styles, options.layout)
}

// Builds MapBox layer config object for focus wells (and artesian) images that pulse
export function focusedWellsLayer (options = {}) {
  const layerId = options.id || FOCUSED_WELLS_LAYER_ID
  const layout = defaultsDeep(options.layout, {
    'icon-image': [
      'case',
      ['to-boolean', ['get', 'artesian_conditions']], FOCUSED_WELL_ARTESIAN_IMAGE_ID,
      FOCUSED_WELL_IMAGE_ID
    ]
  })

  return layerConfig(layerId, options.source || FOCUSED_WELLS_SOURCE_ID, options.layerType || 'symbol', options.styles, layout)
}

// Builds MapBox layer config object for wells that are uncorrelated to any aquifer
export function wellsUncorrelatedLayer (options = {}) {
  const layerId = options.id || WELLS_UNCORRELATED_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': '#FFFFFF',
    'circle-radius': 3,
    'circle-stroke-color': '#000',
    'circle-stroke-width': 1
  })

  const filter = [
    '!', ['to-boolean', ['get', 'aquifer_id']]
  ]

  return vectorLayerConfig(layerId, options.source || WELLS_SOURCE_ID, options.layerType || 'circle', styles, options.layout, filter)
}

// Builds MapBox layer config object for wells that have EMS data
export function wellsEmsLayer (options = {}) {
  const layerId = options.id || WELLS_EMS_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': '#0CA287',
    'circle-radius': 3,
    'circle-stroke-color': '#000',
    'circle-stroke-width': 1
  })

  const filter = [
    'to-boolean', ['get', 'ems']
  ]

  return vectorLayerConfig(layerId, options.source || WELLS_SOURCE_ID, options.layerType || 'circle', styles, options.layout, filter)
}

export function observationWellsLayer (options = {}) {
  const layerId = options.id || WELLS_OBSERVATION_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': [
      'case',
      ['==', ['get', 'observation_well_status_code'], 'Active'], options.activeColour || '#8E1919',
      options.inactiveColour || '#DB6D6D'
    ],
    'circle-radius': 3,
    'circle-stroke-color': '#000',
    'circle-stroke-width': 1
  })

  const filter = [
    'to-boolean', ['get', 'observation_well_number']
  ]

  return vectorLayerConfig(layerId, options.source || WELLS_SOURCE_ID, options.layerType || 'circle', styles, options.layout, filter)
}

// Builds MapBox layer config object for aquifer line outlines
export function aquifersLineLayer (options = {}) {
  const layerId = options.id || AQUIFERS_LINE_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'line-color': [
      'case',
      ['boolean', ['feature-state', 'focused'], false], 'purple',
      ['boolean', ['feature-state', 'selected'], false], 'green',
      ['boolean', ['feature-state', 'searchResult'], false], 'purple',
      '#FF6500'
    ],
    'line-width': [
      'case',
      ['boolean', ['feature-state', 'selected'], false], 2,
      ['boolean', ['feature-state', 'selected'], false], 2,
      1
    ]
  })

  const filter = options.filter || aquiferLayerFilter(false, false)

  return vectorLayerConfig(layerId, options.source || AQUIFERS_SOURCE_ID, options.layerType || 'line', styles, options.layout, filter)
}

// Builds MapBox layer config object for aquifer fill
export function aquifersFillLayer (options = {}) {
  const layerId = options.id || AQUIFERS_FILL_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'fill-color': [
      'case',
      ['boolean', ['feature-state', 'focused'], false], 'purple',
      ['boolean', ['feature-state', 'selected'], false], 'green',
      ['boolean', ['feature-state', 'searchResult'], false], 'purple',
      '#FF6500'
    ],
    'fill-opacity': [
      'case',
      ['boolean', ['feature-state', 'hover'], false], 0.3,
      0.1
    ]
  })

  const filter = options.filter || aquiferLayerFilter(false, false)

  return vectorLayerConfig(layerId, options.source || AQUIFERS_SOURCE_ID, options.layerType || 'fill', styles, options.layout, filter)
}

export function wellLayerFilter (showUnpublishedWells) {
  return [
    'case',
    ['!', ['get', 'is_published']], showUnpublishedWells,
    true
  ]
}

export function aquiferLayerFilter (showUnpublishedAquifers, showRetiredAquifers) {
  return [
    'case',
    ['!', ['get', 'is_published']], showUnpublishedAquifers,
    ['get', 'is_retired'], !!showRetiredAquifers,
    true
  ]
}
