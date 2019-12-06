import L from 'leaflet'

import ArtesianLegend from '../common/assets/images/artesian.png'
import CadastralLegend from '../common/assets/images/cadastral.png'
import EcocatWaterLegend from '../common/assets/images/ecocat-water.png'
import GWaterLicenceLegend from '../common/assets/images/gwater-licence.png'
import OWellsInactiveLegend from '../common/assets/images/owells-inactive.png'
import OWellsActiveLegend from '../common/assets/images/owells-active.png'
import WellsAllLegend from '../common/assets/images/wells-all.png'


const aquiferLayers = {
  'Cadastral': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
    transparent: true,
    name: 'Cadastral',
    legend: CadastralLegend,
    overlay: true
  }),
  'Ecocat - Water related reports': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
    transparent: true,
    name: 'Ecocat - Water related reports',
    legend: EcocatWaterLegend,
    overlay: true
  }),
  'Groundwater licences': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    // layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW', -- ask lindsay
    layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
    transparent: true,
    name: 'Groundwater licences',
    legend: GWaterLicenceLegend,
    overlay: true
  }),
  'Wells - All': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    transparent: true,
    name: 'Wells - All',
    legend: WellsAllLegend,
    overlay: true
  }),
  'Observation wells - active': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: 'Provincial_Groundwater_Observation_Wells_Active',
    transparent: true,
    name: 'Observation wells - active',
    legend: OWellsActiveLegend,
    overlay: true
  }),
  'Observation wells - inactive': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: 'Provincial_Groundwater_Observation_Wells_Inactive',
    transparent: true,
    name: 'Observation wells - inactive',
    legend: OWellsInactiveLegend,
    overlay: true
  }),
  'Artesian wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/ows?', {
    format: 'image/png',
    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    styles: 'Water_Wells_Artesian',
    transparent: true,
    name: 'Artesian wells',
    legend: ArtesianLegend,
    overlay: true
  }),
};

export default aquiferLayers;
