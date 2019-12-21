import L from 'leaflet'

import artesianLegendSrc from '../common/assets/images/artesian.png'
import cadastralLegendSrc from '../common/assets/images/cadastral.png'
import ecoCatWaterLegendSrc from '../common/assets/images/ecocat-water.png'
import groundWaterLicenceActiveLegendSrc from '../common/assets/images/gwater-licence-active.svg'
import groundWaterLicenceInactiveLegendSrc from '../common/assets/images/gwater-licence-inactive.svg'
import observationWellInactiveLegendSrc from '../common/assets/images/owells-inactive.png'
import observationWellActiveLegendSrc from '../common/assets/images/owells-active.png'
import wellsAllLegendSrc from '../common/assets/images/wells-all.png'

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
  'Groundwater licences': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    // layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW', -- ask lindsay
    layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
    transparent: true,
    name: 'Groundwater licences',
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
  'Wells – all': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    transparent: true,
    name: 'Wells – all',
    legend: wellsAllLegendSrc,
    overlay: true
  }),
  'Observation wells – active': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: 'Provincial_Groundwater_Observation_Wells_Active',
    transparent: true,
    name: 'Observation wells – active',
    legend: observationWellActiveLegendSrc,
    overlay: true
  }),
  'Observation wells – inactive': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: 'Provincial_Groundwater_Observation_Wells_Inactive',
    transparent: true,
    name: 'Observation wells – inactive',
    legend: observationWellInactiveLegendSrc,
    overlay: true
  }),
  'Artesian wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: 'Water_Wells_Artesian',
    transparent: true,
    name: 'Artesian wells',
    legend: artesianLegendSrc,
    overlay: true
  })
}

export default aquiferLayers
