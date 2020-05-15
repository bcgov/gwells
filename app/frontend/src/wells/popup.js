import mapboxgl from 'mapbox-gl'

import { getLngLatOfPointFeature } from '../common/mapbox/geometry'
import { WELLS_BASE_AND_ARTESIAN_LAYER_ID, SEARCHED_WELLS_LAYER_ID, FOCUSED_WELLS_LAYER_ID } from '../common/mapbox/layers'
import { wireUpAnchors } from '../common/mapbox/popup'

export const WELL_FEATURE_PROPERTIES_FOR_POPUP = [
  'well_tag_number',
  'identification_plate_number',
  'street_address'
]

export function createWellTooltipElement (wellFeatureProperties) {
  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress
  } = wellFeatureProperties

  const container = document.createElement('div')
  container.className = 'mapbox-tooltip-well'
  container.innerHTML = `
    Well Tag Number: ${wellTagNumber}<br>
    Identification Plate Number: ${identificationPlateNumber || '—'}<br>
    Address: ${streetAddress || '—'}
  `
  return container
}

export function createWellPopupElement ($router, wellFeatureProperties) {
  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress
  } = wellFeatureProperties

  const routes = {
    wellDetail: { name: 'wells-detail', params: { id: wellTagNumber } }
  }

  const url = $router.resolve(routes.wellDetail)

  const container = document.createElement('div')
  container.className = 'mapbox-popup-well'
  container.innerHTML = `
    Well Tag Number: <a href="${url.href}" data-route-name="wellDetail">${wellTagNumber}</a><br>
    Identification Plate Number: ${identificationPlateNumber || '—'}<br>
    Address: ${streetAddress || '—'}
  `
  return wireUpAnchors(container, $router, routes)
}

// Adds mouse event listeners to the map which will show the tooltip on hover and popup for the clicked wells
export function setupMapPopups (map, $router, options = {}) {
  const wellsLayerIds = options.wellsLayerIds || [ WELLS_BASE_AND_ARTESIAN_LAYER_ID, SEARCHED_WELLS_LAYER_ID, FOCUSED_WELLS_LAYER_ID ]

  const tooltip = new mapboxgl.Popup()
  const popup = new mapboxgl.Popup()

  wellsLayerIds.forEach((wellsLayerId) => {
    map.on('mouseenter', wellsLayerId, (e) => {
      if (popup.isOpen()) { return } // don't show tooltip when popup is open

      map.getCanvas().style.cursor = 'pointer'

      const feature = e.features[0]
      const contentDiv = createWellTooltipElement(feature.properties)
      tooltip
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
        .addTo(map)
    })

    map.on('mousemove', wellsLayerId, (e) => {
      if (popup.isOpen()) { return } // don't show tooltip when popup is open

      const feature = e.features[0]
      const contentDiv = createWellTooltipElement(feature.properties)
      tooltip
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
    })

    map.on('mouseleave', wellsLayerId, () => {
      map.getCanvas().style.cursor = ''
      tooltip.remove()
    })

    map.on('click', wellsLayerId, (e) => {
      const feature = e.features[0]
      const contentDiv = createWellPopupElement($router, feature.properties)
      popup
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
        .addTo(map)
    })
  })
}
