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

import aquiferLayers from '../layers'
import { buildLegendHTML } from '../legend'

const AQUIFER_LAYER_STYLE = {
  color: '#FF6500',
  fillColor: '#FF6500',
  weight: 1
}
const HIGHLIGHT_LAYER_STYLE = {
  weight: 1,
  color: 'purple',
  fillColor: 'purple'
}
const SELECTED_LAYER_STYLE = {
  weight: 2,
  color: 'green',
  fillColor: 'green'
}

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
  props: ['aquifersGeometry', 'aquiferDetails', 'highlightAquiferIds', 'loading', 'selectedId', 'viewBBox'],
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
        this.zoomToLayer(this.highlightLayer)
      }
    },
    selectedId (newId, oldId) {
      if (oldId) {
        this.unSelectAquifer(oldId)
      }

      if (newId) {
        const selectedLayer = this.selectAquifer(newId)

        this.zoomToLayer(selectedLayer)
      }

      this.updateCanvasLayer()
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
      })

      if (this.viewBBox) { // if initial view is set then
        this.map.fitBounds(this.viewBBox)
      } else {
        this.map.setView([54.5, -126.5], 5)
      }

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

      this.highlightLayer = L.featureGroup()

      this.selectedAquiferLayer = L.featureGroup()

      this.canvasLayer = L.layerGroup()
      this.canvasLayer.addTo(this.map)

      this.buildAquiferLayer()
      this.updateCanvasLayer()

      this.$emit('activeLayers', this.activeLayers)
    },

    getLocateControl () {
      const locateButton = L.control.locate({ position: 'topleft' })
      locateButton.onClick = (ev) => {
        this.map.locate({ setView: true, maxZoom: 12 })
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
          this.selectedAquiferLayer.clearLayers()
          this.updateCanvasLayer()
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
          const aquiferIds = layersInBound.map((l) => l.aquiferId)
          this.$emit('moved', this.map.getBounds(), aquiferIds)
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

        this.canvasLayer.addLayer(this.highlightLayer)
      }

      if (this.selectedAquiferLayer) {
        this.canvasLayer.addLayer(this.selectedAquiferLayer)
      }
    },
    createAquiferPopupContent (aquiferId, name) {
      return () => {
        const route = { name: 'aquifers-view', params: { id: aquiferId } }
        const url = this.$router.resolve(route)
        const container = L.DomUtil.create('div', 'leaflet-popup-aquifer')
        container.innerHTML = [
          `<div><a href="${url.href}">Aquifer ${aquiferId}</a></div>`,
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
        const layerGroup = L.geoJSON(this.aquifersGeometry, {
          style: AQUIFER_LAYER_STYLE,
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
              layer.setStyle(HIGHLIGHT_LAYER_STYLE)
              layer.bringToFront()
            }
          }
        })
        this.aquiferLayer = layerGroup
      }
    },
    zoomToLayer (layer) {
      const bounds = layer.getBounds()
      if (bounds.isValid()) {
        this.map.fitBounds(bounds)
      }
    },
    selectAquifer (aquiferId) {
      const foundLayer = this.aquiferLayer.getLayers().find((l) => {
        return l.aquiferId === aquiferId
      })

      if (foundLayer) {
        this.highlightLayer.getLayers().forEach((l) => {
          if (l.aquiferId === aquiferId) {
            l.remove()
          }
        })

        this.selectedAquiferLayer.addLayer(foundLayer)
        foundLayer.setStyle(SELECTED_LAYER_STYLE)
        return foundLayer
      }

      return null
    },
    unSelectAquifer (previousAquiferId) {
      this.selectedAquiferLayer.getLayers().forEach((layer) => {
        layer.remove()
        if (layer.aquiferId in this.highlightIdsMap) {
          this.highlightLayer.addLayer(layer)
          layer.setStyle(HIGHLIGHT_LAYER_STYLE)
          layer.bringToFront()
        } else {
          layer.setStyle(AQUIFER_LAYER_STYLE)
        }
      })
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
