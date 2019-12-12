<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import 'leaflet-edgebuffer'
import { filter } from 'lodash'
import { tiledMapLayer } from 'esri-leaflet'

import aquiferLayers from '../layers'

export default {
  name: 'SingleAquiferMap',
  props: ['geom'],
  data () {
    return {
      map: null,
      legendControlContent: null,
      activeLayers: []
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
  destroyed () {
    this.map.remove()
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
      this.map = L.map(this.$el, {
        preferCanvas: true,
        minZoom: 4,
        maxZoom: 17
      }).setView([54.5, -126.5], 5)
      L.control.scale().addTo(this.map)
      // Add map layers.
      tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)

      // Aquifer outlines
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
        transparent: true
      }).addTo(this.map)
      L.control.layers(null, aquiferLayers, { collapsed: false }).addTo(this.map)
      const cadastralLayer = aquiferLayers['Cadastral']
      cadastralLayer.addTo(this.map)

      this.map.addControl(this.getLegendControl())
      this.listenForLayerToggle()
      this.listenForLayerAdd()
      this.listenForLayerRemove()

      this.activeLayers = [
        { layerId: cadastralLayer._leaflet_id, layerName: cadastralLayer.options.name, legend: cadastralLayer.options.legend }
      ]
      this.$emit('activeLayers', this.activeLayers)
    },
    getLegendControl () {
      const self = this
      return new (L.Control.extend({
        options: {
          position: 'bottomright'
        },
        onAdd (map) {
          const container = L.DomUtil.create('div', 'leaflet-control-legend')
          const content = L.DomUtil.create('div', 'leaflet-control-legend-content')
          self.legendControlContent = content
          content.innerHTML = `<div class="m-1">Legend</div>`
          container.appendChild(content)
          return container
        }
      }))()
    },
    listenForLayerToggle () {
      this.$on('activeLayers', (data) => {
        let innerContent = `<ul class="p-0 m-0" style="list-style-type: none;">`
        innerContent += `<li class="m-1 text-center">Legend</li>`
        data.map(l => {
          innerContent += `<li class="m-1"><img src="${l.legend}"> ${l.layerName}</li>`
        })
        innerContent += `</ul>`
        this.legendControlContent.innerHTML = innerContent
      })
    },
    listenForLayerRemove () {
      this.map.on('layerremove', (e) => {
        const layerId = e.layer._leaflet_id
        const legend = e.layer.options.legend
        if (legend) {
          this.activeLayers = filter(this.activeLayers, o => o.layerId !== layerId)
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    listenForLayerAdd () {
      this.map.on('layeradd', (e) => {
        const layerId = e.layer._leaflet_id
        const layerName = e.layer.options.name
        const legend = e.layer.options.legend
        if (legend) {
          this.activeLayers.push({ layerId, layerName, legend })
          this.$emit('activeLayers', this.activeLayers)
        }
      })
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
@import "~leaflet/dist/leaflet.css";

.map {
  height: 500px;
}

.leaflet-control-legend {
  background-color: white;
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
  border-radius: 0.1em;
}

.leaflet-control-layers label:last-child {
  margin-bottom: 0;
}
</style>
