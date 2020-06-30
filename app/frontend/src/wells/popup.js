import { WELLS_BASE_AND_ARTESIAN_LAYER_ID } from '../common/mapbox/layers'
import { popupItems } from '../common/mapbox/popup'

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

  const items = [
    {
      prefix: 'Well Tag Number: ',
      route: { name: 'wells-detail', params: { id: wellTagNumber } },
      text: wellTagNumber
    },
    {
      prefix: 'Identification Plate Number: ',
      text: identificationPlateNumber || '—'
    },
    {
      prefix: 'Address: ',
      text: streetAddress || '—'
    },
    {
      className: isPublished === false ? 'unpublished' : '',
      text: isPublished === false ? 'unpublished' : null
    }
  ]

  return popupItems(items, $router, { className: 'mapbox-popup-well', canInteract })
}
