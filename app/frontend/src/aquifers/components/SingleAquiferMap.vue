<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'

export default {
  name: 'SingleAquiferMap',
  props: ['geom'],
  data () {
    return {
      map: null
    }
  },
  mounted () {
    // There seems to be an issue loading leaflet immediately on mount, we use nextTick to ensure
    // that the view has been rendered at least once before injecting the map.
    this.$nextTick(function () {
      this.initLeaflet()
      this.initMap()
    })
  },
  methods: {
    initLeaflet () {
      // There is a known issue using leaflet with webpack, this is a workaround
      // Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png')
      })
    },
    initMap () {
      // Create map, with default centered and zoomed to show entire BC.
      this.map = L.map(this.$el).setView([54.5, -126.5], 5)
      L.control.scale().addTo(this.map)
      // Add map layers.
      tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'}).addTo(this.map)
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
        styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined',
        transparent: true
      }).addTo(this.map)

      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
        styles: 'Aquifers_BC_Outlined',
        transparent: true
      }).addTo(this.map)

      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP',
        styles: 'FWA_Stream_Network',
        transparent: true
      }).addTo(this.map)

      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP',
        styles: 'Digital_Road_Atlas',
        transparent: true
      }).addTo(this.map)

      const toggleLayers = {
        'Observation Wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
          styles: 'Water_Wells_All',
          transparent: true,
          overlay: true
        }),
        'Water Wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
          styles: 'Provincial_Groundwater_Observation_Wells_Active',
          transparent: true,
          overlay: true
        })
      }
      L.control.layers(null, toggleLayers, {collapsed: false}).addTo(this.map)
    }
  },
  watch: {
    geom: function (newGeom, oldGeom) {
      if (oldGeom || newGeom) {
        var aquiferGeom = L.geoJSON(newGeom, {
          style: {
            'color': 'red'
          }
        }).addTo(this.map)
        // Set map view to aquifer
        this.map.fitBounds(aquiferGeom.getBounds())
      }
    }
  }
}
</script>
<style>
@import "leaflet/dist/leaflet.css";

.map {
  height: 500px;
}

</style>
