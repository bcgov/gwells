import mapboxgl from 'mapbox-gl'
import { uniqBy } from 'lodash'

import { getLngLatOfPointFeature } from '../common/mapbox/geometry'
import {
  toggleAquiferHover,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  AQUIFERS_FILL_LAYER_ID,
  WELLS_EMS_LAYER_ID,
  WELLS_UNCORRELATED_LAYER_ID
} from '../common/mapbox/layers'
import { wireUpAnchors } from '../common/mapbox/popup'

// Creates a <div> for the well's popup content
export function createWellPopupElement ($router, wellFeatureProperties, options = {}) {
  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress,
    aquifer_id: aquiferId,
    ems
  } = wellFeatureProperties

  const routes = {
    wellDetail: { name: 'wells-detail', params: { id: wellTagNumber } },
    aquiferDetail: { name: 'aquifers-view', params: { id: aquiferId } }
  }

  let correlatedAquiferItem = 'Uncorrelated well'
  if (aquiferId) {
    // well is correlated to diff aquifer = link it
    const aquiferDetailsUrl = $router.resolve(routes.aquiferDetail)
    correlatedAquiferItem = `Correlated to <a href="${aquiferDetailsUrl.href}" data-route-name="aquiferDetail">aquifer ${aquiferId}</a>`

    // If there is an optional `currentAquiferId` check to see if this well's aquifer_id is the same
    // as `currentAquiferId`. If it is then don't bother linking to the aquifer.
    if (options.currentAquiferId !== undefined && aquiferId === options.currentAquiferId) {
      correlatedAquiferItem = `Correlated to aquifer ${aquiferId}`
    }
  }

  const url = $router.resolve(routes.wellDetail)

  const items = [
    `Well Tag Number: <a href="${url.href}" data-route-name="wellDetail">${wellTagNumber}</a>`,
    `Identification Plate Number: ${identificationPlateNumber || '—'}`,
    `Address: ${streetAddress || '—'}`,
    correlatedAquiferItem,
    ems ? `EMS ID: ${ems}` : null
  ]

  const container = document.createElement('div')
  container.className = 'mapbox-popup-well'
  container.innerHTML = items.filter(Boolean).join('<br>')
  return wireUpAnchors(container, $router, routes)
}

// Creates a <div> for the well's tooltip content
export function createWellTooltipElement (wellFeatureProperties, options) {
  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress,
    aquifer_id: aquiferId,
    ems
  } = wellFeatureProperties

  let correlatedAquiferItem = 'Uncorrelated well'
  if (aquiferId) {
    correlatedAquiferItem = `Correlated to aquifer ${aquiferId}`
  }

  const items = [
    `Well Tag Number: ${wellTagNumber}`,
    `Identification Plate Number: ${identificationPlateNumber || '—'}`,
    `Address: ${streetAddress || '—'}`,
    correlatedAquiferItem,
    ems ? `EMS ID: ${ems}` : null
  ]

  const container = document.createElement('div')
  container.className = 'mapbox-tooltip-well'
  container.innerHTML = items.filter(Boolean).join('<br>')
  return container
}

function aquiferFeatures (map, point, aquiferLayerIds) {
  return uniqBy(map.queryRenderedFeatures(point, { layers: aquiferLayerIds }), 'id')
}

// Creates a <div> for the aquifer's popup content
export function createAquiferPopupElement (map, $router, point, aquiferLayerIds) {
  const container = document.createElement('div')
  container.className = 'mapbox-popup-aquifer'
  const ul = document.createElement('ul')
  ul.className = 'm-0 p-0 text-center'
  ul.style.listStyle = 'none'
  container.appendChild(ul)

  aquiferFeatures(map, point, aquiferLayerIds).forEach((feature) => {
    const {
      aquifer_id: aquiferId,
      is_retired: isRetired,
      is_published: isPublished
    } = feature.properties
    const route = { name: 'aquifers-view', params: { id: aquiferId } }
    const url = $router.resolve(route)
    const items = [
      `<a href="${url.href}">Aquifer ${aquiferId}</a>`,
      isRetired ? '<b>retired</b>' : null,
      !isPublished ? '<b>unpublished</b>' : null
    ]
    const li = document.createElement('li')
    li.className = 'm-0 p-0'
    li.innerHTML = items.filter(Boolean).join('<br>')
    const a = li.querySelector('a')
    a.onclick = (e) => {
      if (!e.ctrlKey) {
        e.preventDefault()
        $router.push(route)
      }
    }
    // highlight this aquifer on mouseover of the aquifer ID in the popup
    li.onmouseenter = () => {
      toggleAquiferHover(map, aquiferId, true)
    }
    li.onmouseleave = () => {
      toggleAquiferHover(map, aquiferId, false)
    }
    ul.appendChild(li)
  })
  return container
}

// Creates a <div> for the aquifer's tooltip content
export function createAquiferTooltipElement (map, point, aquiferLayerIds) {
  const container = document.createElement('div')
  container.className = 'mapbox-tooltip-aquifer'
  const ul = document.createElement('ul')
  ul.className = 'm-0 p-0 text-center'
  ul.style.listStyle = 'none'
  container.appendChild(ul)

  aquiferFeatures(map, point, aquiferLayerIds).forEach((feature) => {
    const {
      aquifer_id: aquiferId,
      is_retired: isRetired,
      is_published: isPublished
    } = feature.properties
    const items = [
      `Aquifer ${aquiferId}`,
      isRetired ? '<b>retired</b>' : null,
      !isPublished ? '<b>unpublished</b>' : null
    ]
    const li = document.createElement('li')
    li.className = 'm-0 p-0'
    li.innerHTML = items.filter(Boolean).join('<br>')
    ul.appendChild(li)
  })

  return container
}

const DEFAULT_WELL_LAYER_IDS = [
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  WELLS_EMS_LAYER_ID,
  WELLS_UNCORRELATED_LAYER_ID
]

// Adds mouse event listeners to the map which will show the tooltip for an aquifer or well
export function setupMapTooltips (map, $router, options = {}) {
  const wellsTooltip = new mapboxgl.Popup()
  const aquifersTooltip = new mapboxgl.Popup()

  const aquiferLayerIds = options.aquiferLayerIds || [ AQUIFERS_FILL_LAYER_ID ]
  const wellsLayerIds = options.wellsLayerIds || DEFAULT_WELL_LAYER_IDS

  let overAquifer = false
  wellsLayerIds.forEach((wellLayerId) => {
    map.on('mousemove', wellLayerId, (e) => {
      map.getCanvas().style.cursor = 'pointer'

      aquifersTooltip.remove()

      if (map.popup.isOpen()) { return }

      const feature = e.features[0]
      const contentDiv = createWellTooltipElement(feature.properties, options)
      wellsTooltip
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
        .addTo(map)
    })

    map.on('mouseleave', wellLayerId, () => {
      map.getCanvas().style.cursor = ''
      wellsTooltip.remove()
      if (overAquifer && !map.popup.isOpen()) {
        aquifersTooltip.addTo(map)
      }
    })
  })

  aquiferLayerIds.forEach((aquiferLayerId) => {
    map.on('mouseenter', aquiferLayerId, (e) => {
      overAquifer = true
      if (map.popup.isOpen() || wellsTooltip.isOpen()) { return }

      const contentDiv = createAquiferTooltipElement(map, e.point, aquiferLayerIds)
      aquifersTooltip
        .setDOMContent(contentDiv)
        .setLngLat(e.lngLat)
        .addTo(map)
    })

    map.on('mousemove', aquiferLayerId, (e) => {
      if (map.popup.isOpen() || wellsTooltip.isOpen()) { return }

      const contentDiv = createAquiferTooltipElement(map, e.point, aquiferLayerIds)
      aquifersTooltip
        .setDOMContent(contentDiv)
        .setLngLat(e.lngLat)
        .addTo(map)
    })

    map.on('mouseleave', aquiferLayerId, () => {
      aquifersTooltip.remove()
      overAquifer = false
    })
  })

  map.on('reset', () => {
    wellsTooltip.remove()
    aquifersTooltip.remove()
  })
}

// Adds mouse event listeners to the map which will show the popup for the clicked well or aquifer
export function setupMapPopups (map, $router, options = {}) {
  const wellsLayerIds = options.wellsLayerIds || DEFAULT_WELL_LAYER_IDS
  const aquiferLayerIds = options.aquiferLayerIds || [ AQUIFERS_FILL_LAYER_ID ]

  let clickedOnWell = false
  const popup = new mapboxgl.Popup()
  popup.on('close', () => {
    clickedOnWell = false
  })
  map.popup = popup

  wellsLayerIds.forEach((wellLayerId) => {
    map.on('click', wellLayerId, (e) => {
      // Check to see if we have already clicked on a well (could be an invisible EMS layer click)
      if (clickedOnWell) { return }
      clickedOnWell = true
      const feature = e.features[0]
      const contentDiv = createWellPopupElement($router, feature.properties, options)
      popup
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
        .addTo(map)
    })
  })

  aquiferLayerIds.forEach((aquiferLayerId) => {
    map.on('click', aquiferLayerId, (e) => {
      if (clickedOnWell) { return }
      if (map.hoveredAquiferId) {
        toggleAquiferHover(map, map.hoveredAquiferId, false)
      }

      const contentDiv = createAquiferPopupElement(map, $router, e.point, aquiferLayerIds)
      popup
        .setLngLat(e.lngLat)
        .setDOMContent(contentDiv)
        .addTo(map)
    })
  })

  map.on('reset', () => {
    popup.remove()
  })
}
