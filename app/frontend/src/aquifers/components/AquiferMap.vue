<template>
  <div class="aquifer-map">
    <div id="map" class="map"/>
    <ul>
      <li v-for="activeLayer in activeLayers" :key="activeLayer.layerId">
        {{ activeLayer.layerName }}
      </li>
    </ul>
  </div>
</template>

<script>
import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'
import { filter } from 'lodash'
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'
import 'leaflet-geosearch/assets/css/leaflet.css'
export default {
  name: 'AquiferMap',
  props: ['aquifers'],
  created () {
    // There seems to be an issue loading leaflet immediately on mount, we use nextTick to ensure
    // that the view has been rendered at least once before injecting the map.
    this.$nextTick(function () {
      this.initLeaflet()
      this.initMap()
    })
  },

  data () {
    return {
      activeLayers: []
    }
  },

  watch: {
    aquifers: function (newAquifers, oldAquifers) {
      this.map.eachLayer((layer) => {
       if ( layer.options.type === "geojsonfeature" ) {
         this.map.removeLayer(layer)
       }
      })
      this.map.removeLayer(L.geoJSON)
      this.addAquifersToMap(newAquifers)
    }
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
      this.map = L.map('map').setView([54.5, -126.5], 5)
      L.control.scale().addTo(this.map)
      //var areaSelect = L.areaSelect({width:200, height:300});
      //areaSelect.addTo(this.map);

      // Add geo search
      const provider = new OpenStreetMapProvider()
      const searchControl = new GeoSearchControl({
        provider: provider
      })
      this.map.addControl(searchControl)

      // Add map layers.
      tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'}).addTo(this.map)
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
        styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined',
        transparent: true
      }).addTo(this.map)

      // Aquifer outlines
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
        transparent: true
      }).addTo(this.map)

      var mapLayers = {
        // Aquifers likely hydralically connected:

        'Artesian wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
          styles: 'Water_Wells_Artesian',
          transparent: true,
          name: 'Artesian wells'
        }),
        'Cadastral': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
          transparent: true,
          name: 'Cadastral'
        }),
        'Ecocat - Water related reports': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
          transparent: true,
          name: 'Ecocat - Water related reports'
        }),
        'Groundwater licenses': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW',
          transparent: true,
          name: 'Groundwater licenses'
        }),
        'Observation wells - active': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
          styles: 'Provincial_Groundwater_Observation_Wells_Active',
          transparent: true,
          name: 'Observation wells - active'
        }),
        'Observation wells - inactive': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
          styles: 'Provincial_Groundwater_Observation_Wells_Inactive',
          transparent: true,
          name: 'Observation wells - inactive'
        }),
        'Wells - All': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
          format: 'image/png',
          layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
          transparent: true,
          name: 'Wells - All'
        })
      }

      // Add checkboxes for layers
      L.control.layers(null, mapLayers, {collapsed: true}).addTo(this.map)
      /*
      this.map.on('layeradd', (e) => {
        const layerId = e.layer._leaflet_id
        const layerName = e.layer.options.name
        this.activeLayers.push({layerId, layerName})
      })

      this.map.on('layerremove', (e) => {
        const layerId = e.layer._leaflet_id
        this.activeLayers = filter(this.activeLayers, o => o.layerId !== layerId)
      })
      */
    },
    addAquifersToMap (aquifers) {
      console.log("Add Called")
      if (aquifers !== undefined && aquifers.constructor === Array && aquifers.length > 0) {
        var myStyle = {
          'color': 'purple'
        }
        aquifers = aquifers.filter((a) => a.geom !== null)
        aquifers.forEach(aquifer => {
          L.geoJSON(aquifer.geom, {
            aquifer_id: aquifer['aquifer_id'],
            style: myStyle,
            type: 'geojsonfeature',
            onEachFeature: function (feature, layer) {
              layer.bindPopup(`<p>Aquifer: <a href="/gwells/aquifers/${aquifer.aquifer_id}">${aquifer.aquifer_id}</a></p><p>Aquifer Name: ${aquifer.aquifer_name}</p>
                <p>Subtype: ${aquifer.subtype}</p>`)
            }
          }).addTo(this.map)
        })
      }
    },
    zoomToSelectedAquifer (data) {
  
      this.map.eachLayer((layer) => {
        if ( (layer.options.aquifer_id === data.aquifer_id) && layer.feature) {
          this.$nextTick(function() {
            layer.openPopup()
          })
          
        }
      });
      var aquiferGeom = L.geoJSON(data.geom)
      this.map.fitBounds(aquiferGeom.getBounds())
      this.$SmoothScroll(document.getElementById('map'))
    }
  }
}
</script>
<style>
@import "leaflet/dist/leaflet.css";
.map {
  width: 100%;
  height: 500px;
}

.leaflet-areaselect-shade {
    position: absolute;
    background: rgba(0,0,0, 0.4);
}
.leaflet-areaselect-handle {
    position: absolute;
    background: #fff;
    border: 1px solid #666;
    -moz-box-shadow: 1px 1px rgba(0,0,0, 0.2);
    -webkit-box-shadow: 1px 1px rgba(0,0,0, 0.2);
    box-shadow: 1px 1px rgba(0,0,0, 0.2);
    width: 14px;
    height: 14px;
    cursor: move;
}
</style>
