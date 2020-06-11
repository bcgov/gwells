import { WELLS_BASE_AND_ARTESIAN_LAYER_ID } from '../common/mapbox/layers'
import { wireUpAnchors } from '../common/mapbox/popup'

export function createWellPopupElement (features, map, $router, options = {}) {
  const canInteract = Boolean(options.canInteract)
  const wellLayerIds = options.wellLayerIds || [ WELLS_BASE_AND_ARTESIAN_LAYER_ID ]

  // Filter the features to only the well layers we care about
  const feature = features.filter((feature) => wellLayerIds.indexOf(feature.layer.id) !== -1)[0]

  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress,
    is_published: isPublished
  } = feature.properties

  const routes = {
    wellDetail: { name: 'wells-detail', params: { id: wellTagNumber } }
  }

  const url = $router.resolve(routes.wellDetail)

  const container = document.createElement('div')
  container.className = 'mapbox-popup-well'
  container.innerHTML = [
    canInteract
      ? `Well Tag Number: <a href="${url.href}" data-route-name="wellDetail">${wellTagNumber}</a>`
      : `Well Tag Number: ${wellTagNumber}`,
    `Identification Plate Number: ${identificationPlateNumber || '—'}`,
    `Address: ${streetAddress || '—'}`,
    isPublished === false ? '<b>unpublished</b>' : null
  ].filter(Boolean).join('<br>')
  return canInteract ? wireUpAnchors(container, $router, routes) : container
}
