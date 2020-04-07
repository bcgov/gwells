import L from 'leaflet'

import cadastralLegendSrc from '../common/assets/images/cadastral.png'
import ecoCatWaterLegendSrc from '../common/assets/images/ecocat-water.svg'
import groundWaterLicenceActiveLegendSrc from '../common/assets/images/gwater-licence-active.svg'
import groundWaterLicenceInactiveLegendSrc from '../common/assets/images/gwater-licence-inactive.svg'
import observationWellInactiveLegendSrc from '../common/assets/images/owells-inactive.svg'
import observationWellActiveLegendSrc from '../common/assets/images/owells-active.svg'
import wellsAllLegendSrc from '../common/assets/images/wells-all.svg'
import wellsArtesianLegendSrc from '../common/assets/images/wells-artesian.svg'

const aquiferLayers = {
  'Cadastral': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
    transparent: true,
    name: 'Cadastral',
    legend: cadastralLegendSrc,
    overlay: true
  }),
  'EcoCat – water related reports': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
    transparent: true,
    name: 'EcoCat – water related reports',
    legend: ecoCatWaterLegendSrc,
    overlay: true
  }),
  'Water licences': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    // layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW', -- ask lindsay
    layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
    transparent: true,
    name: 'Water licences',
    legend: {
      active: {
        imageSrc: groundWaterLicenceActiveLegendSrc,
        name: 'active'
      },
      inactive: {
        imageSrc: groundWaterLicenceInactiveLegendSrc,
        name: 'inactive'
      }
    },
    overlay: true
  }),
  'Wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    transparent: true,
    name: 'Wells',
    legend: {
      all: {
        imageSrc: wellsAllLegendSrc,
        name: 'all'
      },
      artesian: {
        imageSrc: wellsArtesianLegendSrc,
        name: 'artesian'
      }
    },
    overlay: true
  }),
  'Observation wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: '7707',
    transparent: true,
    name: 'Observation wells',
    legend: {
      all: {
        imageSrc: observationWellActiveLegendSrc,
        name: 'active'
      },
      artesian: {
        imageSrc: observationWellInactiveLegendSrc,
        name: 'inactive'
      }
    },
    overlay: true
  })
}

export default aquiferLayers
