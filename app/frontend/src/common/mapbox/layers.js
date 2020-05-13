import { defaultsDeep } from 'lodash'

const VECTOR_TILE_SERVER = `${window.location.protocol}//${window.location.host}${process.env.VUE_APP_VECTOR_TILE_BASE_URL}`

export const WELLS_LAYER_SOURCE = 'postgis_ftw.gwells_well_view'
export const AQUIFERS_LAYER_SOURCE = 'postgis_ftw.gwells_aquifer_view'

export const DATABC_ROADS_SOURCE_ID = 'DATABC-roads-source'
export const DATABC_ROADS_LAYER_ID = 'DATABC-roads-layer'

export const DATABC_CADASTREL_SOURCE_ID = 'DATABC-cadastrels-source'
export const DATABC_CADASTREL_LAYER_ID = 'DATABC-cadastrels-layer'

export const DATABC_ECOCAT_SOURCE_ID = 'DATABC-ecocat-source'
export const DATABC_ECOCAT_LAYER_ID = 'DATABC-ecocat-layer'

export const DATABC_WATER_LICENCES_SOURCE_ID = 'DATABC-water-licences-source'
export const DATABC_WATER_LICENCES_LAYER_ID = 'DATABC-water-licences-layer'

export const DATABC_OBSERVATION_WELLS_SOURCE_ID = 'DATABC-obswells-source'
export const DATABC_OBSERVATION_WELLS_LAYER_ID = 'DATABC-obswells-layer'

export const DATABC_ROADS_SOURCE = {
  type: 'raster',
  tiles: [
    'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/{z}/{y}/{x}'
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
  type: 'raster',
  tiles: [
    'https://openmaps.gov.bc.ca/geo/pub/ows?&service=WMS&request=GetMap&layers=pub%3AWHSE_FISH.ACAT_REPORT_POINT_PUB_SVW&format=image%2Fpng&transparent=true&version=1.1.1&width=256&height=256&srs=EPSG:3857&bbox={bbox-epsg-3857}'
  ],
  minzoom: 7,
  maxzoom: 24,
  tileSize: 256
}

export const DATABC_WATER_LICENCES_SOURCE = {
  type: 'raster',
  tiles: [
    'https://openmaps.gov.bc.ca/geo/pub/ows?&service=WMS&request=GetMap&layers=pub%3AWHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV&format=image%2Fpng&transparent=true&version=1.1.1&width=256&height=256&srs=EPSG:3857&bbox={bbox-epsg-3857}'
  ],
  minzoom: 6,
  maxzoom: 24,
  tileSize: 256
}

export const DATABC_OBSERVATION_WELLS_SOURCE = {
  type: 'raster',
  tiles: [
    'https://openmaps.gov.bc.ca/geo/pub/ows?&service=WMS&request=GetMap&layers=pub%3AWHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW&format=image%2Fpng&transparent=true&version=1.1.1&width=256&height=256&srs=EPSG:3857&bbox={bbox-epsg-3857}&styles=7707'
  ],
  minzoom: 4,
  maxzoom: 24,
  tileSize: 256
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

export const DATABC_ECOCAT_LAYER = {
  type: 'raster',
  id: DATABC_ECOCAT_LAYER_ID,
  source: DATABC_ECOCAT_SOURCE_ID,
  layout: {
    visibility: 'none'
  }
}

export const DATABC_WATER_LICENCES_LAYER = {
  type: 'raster',
  id: DATABC_WATER_LICENCES_LAYER_ID,
  source: DATABC_WATER_LICENCES_SOURCE_ID,
  layout: {
    visibility: 'none'
  }
}

export const DATABC_OBSERVATION_WELLS_LAYER = {
  type: 'raster',
  id: DATABC_OBSERVATION_WELLS_LAYER_ID,
  source: DATABC_OBSERVATION_WELLS_SOURCE_ID,
  layout: {
    visibility: 'none'
  }
}

export const WELLS_BASE_AND_ARTESIAN_LAYER_ID = 'wells-with-artesian'
export const WELLS_UNCORRELATED_LAYER_ID = 'wells-uncorrelated'
export const WELLS_EMS_LAYER_ID = 'wells-ems'
export const AQUIFERS_LINE_LAYER_ID = 'aquifer-line'
export const AQUIFERS_FILL_LAYER_ID = 'aquifer-fill'

export function vectorTileServerUrl (sourceLayerName) {
  return `${VECTOR_TILE_SERVER}${sourceLayerName}/{z}/{x}/{y}.pbf`
}

export function vectorLayerConfig (sourceLayerName, options = {}) {
  return {
    type: 'vector',
    tiles: [ vectorTileServerUrl(sourceLayerName) ],
    minzoom: 4,
    maxzoom: 17,
    ...options
  }
}

export function layerConfig (id, source, painttype, paint = {}, layout = {}) {
  return {
    id: id,
    source: source,
    'source-layer': source,
    type: painttype,
    paint: paint,
    layout: layout
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
    { source: AQUIFERS_LAYER_SOURCE, id: aquiferId, sourceLayer: AQUIFERS_LAYER_SOURCE },
    { hover: hoveredState }
  )
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

  return layerConfig(layerId, options.source || WELLS_LAYER_SOURCE, options.layerType || 'circle', styles, options.layout)
}

// Builds MapBox layer config object for wells that are uncorrelated to any aquifer
export function wellsUncorrelatedLayer (options = {}) {
  const layerId = options.id || WELLS_UNCORRELATED_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': [
      'case',
      ['to-boolean', ['get', 'aquifer_id']], 'transparent',
      '#FFFFFF'
    ],
    'circle-radius': 3,
    'circle-stroke-color': '#000',
    'circle-stroke-width': [
      'case',
      ['to-boolean', ['get', 'aquifer_id']], 0,
      1
    ]
  })

  return layerConfig(layerId, options.source || WELLS_LAYER_SOURCE, options.layerType || 'circle', styles, options.layout)
}

// Builds MapBox layer config object for wells that have EMS data
export function wellsEmsLayer (options = {}) {
  const layerId = options.id || WELLS_EMS_LAYER_ID
  const styles = defaultsDeep(options.styles, {
    'circle-color': [
      'case',
      ['to-boolean', ['get', 'ems']], '#0CA287',
      'transparent'
    ],
    'circle-radius': 3,
    'circle-stroke-color': '#000',
    'circle-stroke-width': [
      'case',
      ['to-boolean', ['get', 'ems']], 1,
      0
    ]
  })

  return layerConfig(layerId, options.source || WELLS_LAYER_SOURCE, options.layerType || 'circle', styles, options.layout)
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

  return layerConfig(layerId, options.source || AQUIFERS_LAYER_SOURCE, options.layerType || 'line', styles, options.layout)
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

  return layerConfig(layerId, options.source || AQUIFERS_LAYER_SOURCE, options.layerType || 'fill', styles, options.layout)
}
