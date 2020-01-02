<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import 'leaflet-gesture-handling'
import { tiledMapLayer } from 'esri-leaflet'
import { GeoSearchControl, EsriProvider } from 'leaflet-geosearch'
import 'leaflet-lasso'
import 'leaflet-fullscreen/dist/Leaflet.fullscreen.min.js'
import { filter } from 'lodash'

import aquiferLayers from '../layers'
import { buildLegendHTML } from '../legend'

const provider = new EsriProvider()
const searchControl = new GeoSearchControl({
  provider: provider,
  autoClose: true
})

// Extend control, making a locate
L.Control.Locate = L.Control.extend({
  onAdd: function (map) {
    let container = L.DomUtil.create('div', 'geolocate')
    L.DomEvent.addListener(container, 'click', this.click, this)
    return container
  },
  onRemove: function (map) {

  },
  click: function (ev) {
    // Use callback to handle clicks
    if (this.onClick) {
      this.onClick(ev)
    }
  }
})
L.control.locate = function (opts) {
  return new L.Control.Locate(opts)
}

export default {
  name: 'AquiferMap',
  props: ['aquifersGeometry', 'aquiferDetails', 'highlightAquiferIds', 'loading'],
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

  data () {
    return {
      activeLayers: [],
      map: null,
      legendControlContent: null
    }
  },
  computed: {
    highlightIdsMap () {
      return this.highlightAquiferIds.reduce((obj, aquiferId) => {
        obj[aquiferId] = aquiferId
        return obj
      }, {})
    }
  },
  watch: {
    aquifersGeometry () {
      this.buildAquiferLayer()
    },
    highlightAquiferIds (newIds) {
      this.buildAquiferLayer()
      if (newIds.length > 0) {
        this.zoomToHighlightedAquifers()
      }
    },
    loading () {
      this.updateCanvasLayer()
    }
  },
  methods: {
    initLeaflet () {
      // There is a known issue using leaflet with webpack, this is a workaround
      // Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('../../common/assets/images/marker-icon-2x.png'),
        iconUrl: require('../../common/assets/images/marker-icon.png'),
        shadowUrl: require('../../common/assets/images/marker-shadow.png')
      })
    },
    initMap () {
      this.map = L.map(this.$el, {
        preferCanvas: true,
        gestureHandling: true,
        minZoom: 4,
        maxZoom: 17
      }).setView([54.5, -126.5], 5)
      L.control.scale().addTo(this.map)

      this.map.addControl(this.getFullScreenControl())
      this.map.addControl(searchControl)
      this.map.addControl(this.getAreaSelectControl())
      this.map.addControl(this.getLegendControl())
      this.map.addControl(this.getLocateControl())

      // Add map layers.
      tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)

      L.control.layers(null, aquiferLayers, { collapsed: false }).addTo(this.map)
      const cadastralLayer = aquiferLayers['Cadastral']
      cadastralLayer.addTo(this.map)

      Object.keys(aquiferLayers).forEach((layerName) => {
        const layer = aquiferLayers[layerName]
        this.activeLayers[layerName] = {
          layerName: layer.options.name,
          legend: layer.options.legend,
          show: false
        }
      })
      this.activeLayers[cadastralLayer.options.name].show = true

      this.listenForLayerToggle()
      this.listenForLayerAdd()
      this.listenForLayerRemove()
      this.listenForMapMovement()
      this.listenForReset()
      this.listenForAreaSelect()

      this.canvasRenderer = L.canvas({ padding: 0.1 })

      this.canvasLayer = L.layerGroup()
      this.canvasLayer.addTo(this.map)

      this.highlightLayer = L.featureGroup()
      this.highlightLayer.addTo(this.map)

      this.buildAquiferLayer()
      this.updateCanvasLayer()

      this.$emit('activeLayers', this.activeLayers)
    },

    getLocateControl () {
      const locateButton = L.control.locate({ position: 'topleft' })
      locateButton.onClick = (ev) => {
        this.map.locate({ setView: true, maxZoom: 12 })
        this.$parent.fetchResults()
      }
      return locateButton
    },
    getFullScreenControl () {
      return new L.Control.Fullscreen({
        position: 'topleft'
      })
    },
    getAreaSelectControl () {
      const lasso = L.lasso(this.map)
      return new (L.Control.extend({
        options: {
          position: 'topleft'
        },
        onAdd: function (map) {
          var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control')
          container.innerHTML = '<a class="leaflet-bar-part leaflet-bar-part-single"><span class="fa fa-hand-paper-o"></span></a>'
          container.onclick = function (map) {
            lasso.enable()
          }
          return container
        }
      }))()
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
        this.legendControlContent.innerHTML = buildLegendHTML(data)
      })
    },
    listenForAreaSelect () {
      this.map.on('lasso.finished', (event) => {
        this.map.fitBounds(event.latLngs)
      })
    },
    listenForLayerRemove () {
      this.map.on('layerremove', (e) => {
        const { legend, name } = e.layer.options
        if (legend) {
          this.activeLayers[name].show = false
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    listenForLayerAdd () {
      this.map.on('layeradd', (e) => {
        const { legend, name } = e.layer.options
        if (legend) {
          this.activeLayers[name].show = true
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    listenForReset () {
      this.$parent.$on('resetLayers', (data) => {
        if (this.map) {
          this.map.eachLayer((layer) => {
            if (layer.wmsParams && layer.wmsParams.overlay) {
              this.map.removeLayer(layer)
            }
          })
          this.highlightLayer.clearLayers()
          this.map.setView([54.5, -126.5], 5)
        }
      })
    },
    getFeaturesOnMap (map) {
      const layersInBound = []
      const bounds = map.getBounds()
      map.eachLayer((layer) => {
        if (layer.feature && bounds.overlaps(layer.getBounds())) {
          layersInBound.push(layer)
        }
      })
      return layersInBound
    },
    listenForMapMovement () {
      const events = ['zoomend', 'moveend']
      events.map(eventName => {
        this.map.on(eventName, (e) => {
          const map = e.target
          const layersInBound = this.getFeaturesOnMap(map)
          this.$parent.$emit('featuresOnMap', layersInBound)
        })
      })
    },
    updateCanvasLayer () {
      this.canvasLayer.clearLayers()

      if (this.aquiferLayer) {
        this.canvasLayer.addLayer(this.aquiferLayer)
      }

      if (this.highlightLayer) {
        this.highlightLayer.getLayers().forEach((l) => {
          l.bringToFront()
        })
      }
    },
    createAquiferPopupContent (aquiferId, name) {
      return () => {
        const route = { name: 'aquifers-view', params: { id: aquiferId } }
        const url = this.$router.resolve(route)
        const container = L.DomUtil.create('div', 'leaflet-popup-aquifer')
        container.innerHTML = [
          `<div>Aquifer ID: <a href="${url.href}">${aquiferId}</a></div>`,
          name ? `<div>Aquifer name: ${name}</div>` : null
        ].filter(Boolean).join('\n')
        L.DomEvent.on(container.querySelector('a'), 'click', (e) => {
          if (!e.ctrlKey) {
            e.preventDefault()
            this.$router.push(route)
          }
        })
        return container
      }
    },
    buildAquiferLayer (aquifers) {
      const self = this
      if (this.highlightLayer) {
        this.highlightLayer.clearLayers()
      }
      if (this.aquifersGeometry && this.aquifersGeometry.features.length > 0) {
        const style = {
          color: '#FF6500',
          weight: 1
        }
        const highLightStyle = {
          ...style,
          color: 'purple',
          fillColor: 'purple'
        }
        const layerGroup = L.geoJSON(this.aquifersGeometry, {
          style,
          // type: 'geojsonfeature',
          onEachFeature (feature, layer) {
            const { id: aquiferId, name } = feature.properties
            layer.aquiferId = aquiferId

            layer.bindPopup(self.createAquiferPopupContent(aquiferId, name))
            layer.on('mouseover', () => {
              layer.unbindTooltip()
              if (!layer.isPopupOpen()) {
                layer.bindTooltip(`Aquifer ${feature.properties.id}`, { sticky: true }).openTooltip()
              }
            })
            layer.on('click', () => {
              layer.unbindTooltip()
            })

            if (aquiferId in self.highlightIdsMap) {
              self.highlightLayer.addLayer(layer)
              layer.setStyle(highLightStyle)
              layer.bringToFront()
            }
          }
        })
        this.aquiferLayer = layerGroup
      }
    },
    zoomToHighlightedAquifers (data) {
      const bounds = this.highlightLayer.getBounds()
      this.map.fitBounds(bounds)
    }
  }
}
</script>
<style>
@import "~leaflet/dist/leaflet.css";
@import '~leaflet-geosearch/assets/css/leaflet.css';
@import '~leaflet-fullscreen/dist/leaflet.fullscreen.css';
@import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";

.map {
  width: 100%;
  height: 500px;
}

.leaflet-control-geosearch a.reset {
  display: none;
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
.geolocate {
    background-image: url('../../common/assets/images/geolocate.png');
    width: 30px;
    height: 30px;
    left: 2px;
    box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
    cursor: pointer;
}

.leaflet-control-address {
    width: 30px;
    height: 30px;
    left: 2px;
    box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
    cursor: pointer;
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}
.geolocate:hover {
    opacity: 0.8;
}

.leaflet-control-legend {
  background-color: white;
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
  border-radius: 0.1em;
}
</style>
