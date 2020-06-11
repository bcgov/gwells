import { uniqBy } from 'lodash'

import {
  toggleAquiferHover,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  AQUIFERS_FILL_LAYER_ID,
  DATABC_ECOCAT_LAYER_ID
} from '../common/mapbox/layers'
import { wireUpAnchors } from '../common/mapbox/popup'

// Creates a <div> for the well's popup content
export function createWellPopupElement (features, map, $router, options = {}) {
  const currentAquiferId = options.currentAquiferId || null
  const canInteract = Boolean(options.canInteract)
  const wellLayerIds = options.wellLayerIds || [ WELLS_BASE_AND_ARTESIAN_LAYER_ID ]

  // Filter the features to only the well layers we care about
  const feature = features.filter((feature) => wellLayerIds.indexOf(feature.layer.id) !== -1)[0]

  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress,
    aquifer_id: aquiferId,
    ems
  } = feature.properties

  const routes = {
    wellDetail: { name: 'wells-detail', params: { id: wellTagNumber } },
    aquiferDetail: { name: 'aquifers-view', params: { id: aquiferId } }
  }

  let correlatedAquiferItem = 'Uncorrelated well'
  if (aquiferId) {
    // Only link to the correlated aquifer if the user can interact with this popup content. Or if
    // the optional `currentAquiferId` is not the same as this aquiferId
    if (canInteract && aquiferId !== currentAquiferId) {
      const aquiferDetailsUrl = $router.resolve(routes.aquiferDetail)
      correlatedAquiferItem = `Correlated to <a href="${aquiferDetailsUrl.href}" data-route-name="aquiferDetail">aquifer ${aquiferId}</a>`
    } else {
      correlatedAquiferItem = `Correlated to aquifer ${aquiferId}`
    }
  }

  const url = $router.resolve(routes.wellDetail)

  const items = [
    canInteract
      ? `Well Tag Number: <a href="${url.href}" data-route-name="wellDetail">${wellTagNumber}</a>`
      : `Well Tag Number: ${wellTagNumber}`,
    `Identification Plate Number: ${identificationPlateNumber || '—'}`,
    `Address: ${streetAddress || '—'}`,
    correlatedAquiferItem,
    ems ? `EMS ID: ${ems}` : null
  ]

  const container = document.createElement('div')
  container.className = 'mapbox-popup-well'
  container.innerHTML = items.filter(Boolean).join('<br>')
  return canInteract ? wireUpAnchors(container, $router, routes) : container
}

// Creates a <div> for the aquifer's popup content
export function createAquiferPopupElement (features, map, $router, options = {}) {
  const currentAquiferId = options.currentAquiferId || null
  const canInteract = Boolean(options.canInteract)
  const aquiferLayerIds = options.aquiferLayerIds || [ AQUIFERS_FILL_LAYER_ID ]

  const container = document.createElement('div')
  container.className = 'mapbox-popup-aquifer'
  const ul = document.createElement('ul')
  ul.className = `m-0 p-0 text-center mapbox-${canInteract ? 'popup' : 'tooltip'}`
  ul.style.listStyle = 'none'
  container.appendChild(ul)

  // Filter the features to only the aquifer layers we care about
  const onlyAquiferFeatures = features.filter((feature) => aquiferLayerIds.indexOf(feature.layer.id) !== -1)

  uniqBy(onlyAquiferFeatures, 'id').forEach((feature) => {
    const {
      aquifer_id: aquiferId,
      is_retired: isRetired,
      is_published: isPublished
    } = feature.properties
    const routes = {
      aquiferDetail: { name: 'aquifers-view', params: { id: aquiferId } }
    }
    const url = $router.resolve(routes.aquiferDetail)
    const aquiferTitle = `Aquifer ${aquiferId}`
    const linkToAquifer = canInteract && currentAquiferId !== aquiferId
    const items = [
      linkToAquifer ? `<a href="${url.href}" data-route-name="aquiferDetail">${aquiferTitle}</a>` : aquiferTitle,
      isRetired ? '<b>retired</b>' : null,
      !isPublished ? '<b>unpublished</b>' : null
    ]
    const li = document.createElement('li')
    li.className = 'm-0 p-0'
    li.innerHTML = items.filter(Boolean).join('<br>')
    if (canInteract) {
      wireUpAnchors(li, $router, routes)
      // highlight this aquifer on mouseover of the aquifer ID in the popup
      li.onmouseenter = () => {
        toggleAquiferHover(map, aquiferId, true)
      }
      li.onmouseleave = () => {
        toggleAquiferHover(map, aquiferId, false)
      }
    }
    ul.appendChild(li)
  })

  return container
}

// Creates a <div> for the ecocat's popup content
export function createEcocatPopupElement (features, map, options = {}) {
  const canInteract = Boolean(options.canInteract)
  const ecocatLayerIds = options.ecocatLayerIds || [ DATABC_ECOCAT_LAYER_ID ]

  const container = document.createElement('div')
  container.className = 'mapbox-popup-ecocat'

  const feature = features.filter((feature) => ecocatLayerIds.indexOf(feature.layer.id) !== -1)[0]

  const {
    REPORT_ID: reportId,
    TITLE: title,
    AUTHOR: author,
    DATE_PUBLISHED: datePublished
  } = feature.properties

  const ecocatReportLink = `<a href="https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=${reportId}" target="_blank">${title}</a>`

  container.innerHTML = [
    canInteract ? ecocatReportLink : title,
    author ? `Author: ${author}` : null,
    datePublished ? `Published: ${datePublished}` : null
  ].filter(Boolean).join('<br>')

  return container
}
