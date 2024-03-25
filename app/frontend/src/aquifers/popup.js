import { uniqBy, pick, isEqual } from 'lodash'

import {
  toggleAquiferHover,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  AQUIFERS_FILL_LAYER_ID,
  DATABC_ECOCAT_LAYER_ID,
  DATABC_GROUND_WATER_LICENCES_LAYER_ID,
  DATABC_SURFACE_WATER_LICENCES_LAYER_ID,
} from '../common/mapbox/layers'
import { popupItems, popupItem } from '../common/mapbox/popup'

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
    ems,
    observation_well_number: observationWellNumber,
    observation_well_status_code: observationWellStatusCode,
    is_published: isPublished
  } = feature.properties

  let correlatedAquiferItem = 'Uncorrelated well'
  if (aquiferId) {
    // Only link to the correlated aquifer if the user can interact with this popup content. Or if
    // the optional `currentAquiferId` is not the same as this aquiferId
    if (canInteract && aquiferId !== currentAquiferId) {
      correlatedAquiferItem = {
        prefix: 'Correlated to ',
        route: { name: 'aquifers-view', params: { id: aquiferId } },
        text: `aquifer ${aquiferId}`
      }
    } else {
      correlatedAquiferItem = `Correlated to aquifer ${aquiferId}`
    }
  }

  const observationWellUrl = `https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20${observationWellNumber}`
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
    ems ? {
      prefix: 'EMS ID: ',
      text: ems
    } : null,
    observationWellNumber ? {
      prefix: `${observationWellStatusCode} observation well number: `,
      url: observationWellUrl,
      text: observationWellNumber
    } : null,
    correlatedAquiferItem,
    {
      className: isPublished === false ? 'unpublished' : '',
      text: isPublished === false ? 'unpublished' : null
    }
  ]

  return popupItems(items, $router, { className: 'mapbox-popup-well', canInteract })
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

  uniqBy(onlyAquiferFeatures, 'id').map((feature) => {
    const {
      aquifer_id: aquiferId,
      is_retired: isRetired,
      is_published: isPublished,
      material_type: materialType,
      subtype: subType
    } = feature.properties
    const linkToAquifer = canInteract && currentAquiferId !== aquiferId

    const item = {
      className: `${isRetired ? 'retired' : ''} ${isPublished ? 'published' : ''}`,
      route: linkToAquifer ? { name: 'aquifers-view', params: { id: aquiferId } } : null,
      text: `Aquifer ${aquiferId} (${materialType}, ${subType})`,
      suffix: [
        isRetired ? 'retired' : null,
        !isPublished ? 'unpublished' : null
      ].filter(Boolean).join(' – ')
    }

    const li = popupItem(item, $router, { canInteract })

    if (canInteract) {
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

  const feature = features.filter((feature) => ecocatLayerIds.indexOf(feature.layer.id) !== -1)[0]

  const {
    REPORT_ID: reportId,
    TITLE: title,
    AUTHOR: author,
    DATE_PUBLISHED: datePublished
  } = feature.properties

  const ecocatReportUrl = `https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=${reportId}`

  const items = [
    {
      url: ecocatReportUrl,
      text: title
    },
    {
      prefix: 'Author: ',
      text: author
    },
    {
      prefix: 'Published: ',
      text: datePublished
    }
  ]

  return popupItems(items, null, { className: 'mapbox-popup-ecocat', canInteract })
}

// Creates a <div> for the water licence's popup content
export function createWaterLicencePopupElement (features, map, $router, options = {}) {
  const canInteract = Boolean(options.canInteract)
  // const isSurfaceWaterLicence = Boolean(options.surfaceWater)
  // const isGroundWaterLicence = Boolean(options.groundWater)
  const waterLicenceLayerIds = options.waterLicenceLayerIds || [ DATABC_SURFACE_WATER_LICENCES_LAYER_ID, DATABC_GROUND_WATER_LICENCES_LAYER_ID ]

  const container = document.createElement('div')
  container.className = 'mapbox-popup-water-licence'

  // Filter to only features in water licence layers
  const licenceFeatures = features.filter((feature) => waterLicenceLayerIds.indexOf(feature.layer.id) !== -1)
  // Find similar features that have the same licence number at the same lat/lng
  const sameLicenceFeatures = similarFeatures(licenceFeatures, ['LICENCE_NUMBER', 'LONGITUDE', 'LATITUDE'])

  const topFeature = sameLicenceFeatures[0]
  const {
    LICENCE_NUMBER: licenceNumber,
    LICENCE_STATUS: licenceStatus,
    SOURCE_NAME: sourceName,
    POD_SUBTYPE: podSubtype
  } = topFeature.properties

  const isGroundWaterLicence = podSubtype.indexOf('POD') === -1

  // Create a sub-list of items by licence purpose + quantity
  const purposeItems = sameLicenceFeatures.map((feature) => {
    const {
      PURPOSE_USE: purposeUse,
      QUANTITY: quantity,
      QUANTITY_UNITS: quantityUnits
    } = feature.properties

    const quantityByPurposeEl = document.createElement('div')
    const purposeEl = document.createElement('span')
    purposeEl.className = 'licence-purpose'
    purposeEl.textContent = purposeUse
    const quantityEl = document.createElement('span')
    quantityEl.className = 'licence-quantity'
    quantityEl.textContent = `${Number(quantity).toFixed(2)}\xa0${quantityUnits}`

    quantityByPurposeEl.appendChild(purposeEl)
    quantityByPurposeEl.appendChild(quantityEl)

    return {
      className: 'quantity-by-purpose',
      el: quantityByPurposeEl
    }
  })

  const purposeEl = popupItems(purposeItems, null, { nodeName: 'ul' })

  const licenceUrl = `https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&PosseObjectDef=o_ATIS_DocumentSearch&PosseMenuName=WS_Main&Criteria_LicenceNumber=${licenceNumber}`

  // If this is a groundwater licence then SOURCE_NAME should be the aquiferId
  const aquiferId = (isGroundWaterLicence && sourceName && Number(sourceName)) || null

  const items = [
    {
      prefix: 'Licence number: ',
      url: licenceUrl,
      text: licenceNumber
    },
    {
      prefix: 'Status: ',
      text: licenceStatus
    },
    {
      prefix: 'Quantity per purpose:',
      el: purposeEl
    },
    {
      prefix: 'Source: ',
      text: `${aquiferId ? 'aquifer ' : ''}${sourceName}`,
      route: aquiferId ? { name: 'aquifers-view', params: { id: aquiferId } } : null
    }
  ]

  return popupItems(items, $router, { className: 'mapbox-popup-water-licence', canInteract })
}

function similarFeatures (features, properties) {
  const paths = properties.map((p) => `properties.${p}`)
  const topFeatureProperties = pick(features[0], paths)

  return features.filter((feature) => {
    return isEqual(topFeatureProperties, pick(feature, paths))
  })
}
