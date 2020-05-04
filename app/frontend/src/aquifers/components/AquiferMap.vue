<template>
  <div id="aquifer-search-map" class="map"/>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import L from 'leaflet'
import 'leaflet-gesture-handling'
import { tiledMapLayer } from 'esri-leaflet'
import { uniq } from 'lodash'
import { GeoSearchControl, EsriProvider } from 'leaflet-geosearch'
import 'leaflet-lasso'
import 'leaflet-fullscreen/dist/Leaflet.fullscreen.min.js'
import { pointInPolygon } from 'geojson-utils'

import features from '../../common/features'
import aquiferLayers from '../layers'
import { buildLegendHTML } from '../legend'
import { FETCH_SIMPLIFIED_GEOMETRY, SEARCH_AQUIFERS } from '../store/actions.types'

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
const AQUIFER_HOVER_OVER_STYLE = {
  fillOpacity: 0.5
}
const AQUIFER_HOVER_OUT_STYLE = {
  fillOpacity: 0.2
}

const provider = new EsriProvider()
const searchControl = new GeoSearchControl({
  provider: provider,
  autoClose: true
})

const DEFAULT_MAP_CENTRE = new L.LatLng(54.459, -126.495)
const DEFAULT_MAP_ZOOM = 5

export default {
  name: 'AquiferMap',
  props: [
    'initialZoom',
    'initialCentre',
    'aquiferDetails',
    'highlightAquiferIds',
    'loading',
    'selectedId',
    'searchText'
  ],
  mounted () {
    // There seems to be an issue loading leaflet immediately on mount, we use nextTick to ensure
    // that the view has been rendered at least once before injecting the map.
    this.$nextTick(() => {
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
      legendControlContent: null,
      searchMapButtonEnabled: Boolean(this.searchText)
    }
  },
  computed: {
    ...mapState('aquiferStore/aquiferGeoms', {
      aquifersGeometry: 'simplifiedGeoJson',
      aquifersGeometryFetched: 'simplifiedGeoJsonFetched'
    }),
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
        // setTimeout needed when loading map w/ a search. Otherwise
        // `this.highlightLayer.getBounds()` returns invalid bounds (for reasons
        // unknown)
        setTimeout(() => {
          this.zoomToLayer(this.highlightLayer)
        }, 50)
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
    },
    searchText (searchQuery) {
      this.searchMapButtonEnabled = Boolean(searchQuery)
    }
  },
  methods: {
    ...mapActions('aquiferStore/aquiferGeoms', {
      fetchSimplifiedGeometry: FETCH_SIMPLIFIED_GEOMETRY
    }),
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

      this.map._controlCorners['topcenter'] = L.DomUtil.create('div', 'leaflet-top leaflet-center', this.map._controlContainer)

      const zoom = this.initialZoom || DEFAULT_MAP_ZOOM
      const centre = this.initialCentre ? [this.initialCentre.lat, this.initialCentre.lng] : DEFAULT_MAP_CENTRE

      this.map.setView(centre, zoom)

      L.control.scale().addTo(this.map)

      this.map.addControl(this.getFullScreenControl())
      this.map.addControl(searchControl)
      this.map.addControl(this.getAreaSelectControl())
      this.map.addControl(this.getLegendControl())
      this.map.addControl(this.getLocateControl())
      this.map.addControl(this.getMapSearchControl())

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
      this.listenForZoom()
      this.listenForReset()
      this.listenForAreaSelect()

      this.highlightLayer = L.featureGroup()

      this.selectedAquiferLayer = L.featureGroup()

      this.canvasLayer = L.layerGroup()
      this.canvasLayer.addTo(this.map)

      this.buildAquiferLayer()
      this.updateCanvasLayer()

      this.$emit('activeLayers', this.activeLayers)

      if (!this.aquifersGeometryFetched) {
        this.fetchSimplifiedGeometry()
      }
    },

    getLocateControl () {
      const options = {
        position: 'topleft'
      }
      return new (L.Control.extend({
        onAdd (map) {
          const title = 'Zoom to your location'
          let container = L.DomUtil.create('div', 'leaflet-bar geolocate')
          container.title = title
          container.innerHTML = `<a></a>`
          L.DomEvent.addListener(container, 'click', this.click, this)
          return container
        },
        click: (ev) => {
          this.map.locate({ setView: true, maxZoom: 12 })
        }
      }))(options)
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
        onAdd (map) {
          const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-area-select')
          container.title = 'Draw a polygon to zoom'
          container.innerHTML = `<a></a>`
          container.onclick = (e) => {
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
    getMapSearchControl () {
      const self = this
      return new (L.Control.extend({
        options: {
          position: 'topcenter'
        },
        onAdd (map) {
          const container = L.DomUtil.create('div', 'leaflet-control-search leaflet-control-center')
          container.innerHTML = `<button class="btn btn-default" type="button">Search this area</button>`
          const button = container.querySelector('button')
          self.mapSearchButtonContainer = container
          button.onclick = () => {
            self.searchButtonClicked()
          }
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
        this.hideMapSearchButton()
        this.supressShowMapSearchButton = true
        if (this.map) {
          this.map.eachLayer((layer) => {
            if (layer.wmsParams && layer.wmsParams.overlay) {
              this.map.removeLayer(layer)
            }
          })
          this.highlightLayer.clearLayers()
          this.selectedAquiferLayer.clearLayers()
          this.updateCanvasLayer()
          this.map.setView(DEFAULT_MAP_CENTRE, DEFAULT_MAP_ZOOM)
        }
      })
    },
    hideMapSearchButton () {
      window.clearTimeout(this.showMapSearchButtonTimer)
      this.showMapSearchButtonTimer = null
      this.mapSearchButtonContainer.classList.remove('show')
    },
    showMapSearchButton () {
      if (!features.searchInAquiferMap) { return }
      if (this.showMapSearchButtonTimer) { return }
      this.showMapSearchButtonTimer = window.setTimeout(() => {
        this.showMapSearchButtonTimer = null
        if (!this.supressShowMapSearchButton) {
          this.mapSearchButtonContainer.classList.add('show')
        } else {
          this.supressShowMapSearchButton = false
        }
      }, 500)
    },
    getFeaturesOnMap () {
      const layersInBound = []
      const bounds = this.map.getBounds()
      this.map.eachLayer((layer) => {
        if (layer.feature && bounds.overlaps(layer.getBounds())) {
          layersInBound.push(layer)
        }
      })
      return layersInBound
    },
    listenForMapMovement () {
      const startEvents = ['zoomstart', 'movestart']
      startEvents.forEach(eventName => {
        this.map.on(eventName, (e) => {
          if (this.searchMapButtonEnabled) {
            this.showMapSearchButton()
          }
        })
      })
      const endEvents = ['zoomend', 'moveend']
      endEvents.forEach(eventName => {
        this.map.on(eventName, (e) => {
          const bounds = this.map.getBounds()
          const layersInBound = this.getFeaturesOnMap()
          const aquiferIds = layersInBound.map((l) => l.aquiferId)
          this.$emit('moved', bounds, uniq(aquiferIds))
        })
      })
    },
    listenForZoom () {
      this.map.on('zoomend', () => {
        const zoom = this.map.getZoom()
        this.$emit('zoomed', zoom, this.map.getBounds())
      })
    },
    searchButtonClicked () {
      this.hideMapSearchButton()
      this.$emit('search', this.map.getZoom(), this.map.getBounds())
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
    findAquifersUnderPoint (lat, lng) {
      const point = { type: 'Point', coordinates: [lng, lat] }
      const aquifers = []
      this.aquiferLayer.getLayers()
        .filter((layer) => {
          // Filter to those layers' bounds that contain the point
          return layer.getBounds().contains([lat, lng])
        })
        .forEach((layer) => {
          // Build a GeoJSON object to test
          const feature = layer.toGeoJSON()
          const isInPolygon = pointInPolygon(point, feature.geometry)
          if (isInPolygon) {
            aquifers.push({
              layer: layer,
              featureProperties: feature.properties
            })
          }
        })
      return aquifers
    },
    createAquiferPopupContent (clickedLayer, clickedFeatureProperties) {
      var self = this
      return function (e) {
        const latlng = this.getLatLng()

        clickedLayer.setStyle({ fillOpacity: 0.2 })

        const container = L.DomUtil.create('div', 'leaflet-popup-aquifer')
        const ul = L.DomUtil.create('ul')
        container.appendChild(ul)

        self.findAquifersUnderPoint(latlng.lat, latlng.lng).forEach(({ layer, featureProperties }) => {
          const { id: aquiferId } = featureProperties
          const route = { name: 'aquifers-view', params: { id: aquiferId } }
          const url = self.$router.resolve(route)
          const li = L.DomUtil.create('li')
          li.innerHTML = `<a href="${url.href}">Aquifer ${aquiferId}</a>`
          const a = li.querySelector('a')
          a.onclick = (e) => {
            if (!e.ctrlKey) {
              e.preventDefault()
              self.$router.push(route)
            }
          }
          li.onmouseenter = () => {
            layer.setStyle(AQUIFER_HOVER_OVER_STYLE)
          }
          li.onmouseleave = () => {
            layer.setStyle(AQUIFER_HOVER_OUT_STYLE)
          }
          ul.appendChild(li)
        })
        return container
      }
    },
    buildAquiferLayer (aquifers) {
      const self = this
      if (this.highlightLayer) {
        this.highlightLayer.clearLayers()
      }
      if (this.selectedAquiferLayer) {
        this.selectedAquiferLayer.clearLayers()
      }
      if (this.aquifersGeometry && this.aquifersGeometry.features.length > 0) {
        const layerGroup = L.geoJSON(this.aquifersGeometry, {
          style: AQUIFER_LAYER_STYLE,
          // type: 'geojsonfeature',
          onEachFeature (feature, layer) {
            const { id: aquiferId } = feature.properties
            layer.aquiferId = aquiferId

            layer.bindPopup(self.createAquiferPopupContent(layer, feature.properties))
            layer.on('mouseover', () => {
              layer.unbindTooltip()
              if (!layer.isPopupOpen()) {
                layer.setStyle(AQUIFER_HOVER_OVER_STYLE)
                layer.bindTooltip(`Aquifer ${feature.properties.id}`, { sticky: true }).openTooltip()
              }
            })
            layer.on('mouseout', () => {
              layer.setStyle(AQUIFER_HOVER_OUT_STYLE)
            })
            layer.on('click', () => {
              layer.unbindTooltip()
            })

            if (self.selectedId === aquiferId) {
              self.selectedAquiferLayer.addLayer(layer)
              layer.setStyle(SELECTED_LAYER_STYLE)
            } else if (aquiferId in self.highlightIdsMap) {
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
        this.supressShowMapSearchButton = true
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
  },
  created () {
    // On reset or basic search, clear local params
    this.$store.subscribeAction((action, state) => {
      if (action.type === `aquiferStore/search/${SEARCH_AQUIFERS}`) {
        this.hideMapSearchButton()
      }
    })
  }
}
</script>
<style lang="scss">
@import "~leaflet/dist/leaflet.css";
@import '~leaflet-geosearch/assets/css/leaflet.css';
@import '~leaflet-fullscreen/dist/leaflet.fullscreen.css';
@import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";

#aquifer-search-map {
  height: 600px;

  .leaflet-control-area-select a {
    background: url('../../common/assets/images/shape-polygon-plus.svg') no-repeat center center white;
    cursor: pointer;
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
    box-shadow: 1px 1px rgba(0,0,0, 0.2);
    width: 14px;
    height: 14px;
    cursor: move;
  }

  .geolocate a {
    background: url('../../common/assets/images/geolocate.png') no-repeat center center white;
    cursor: pointer;
  }

  .leaflet-control-legend {
    background-color: white;
    box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
    border-radius: 0.1em;
  }

  .leaflet-popup-aquifer {
    ul {
      margin: 0;
      padding: 0;
      list-style-type: none;
    }

    li {
      margin: 0;
      padding: 0;
    }
  }
}

.leaflet-top.leaflet-center {
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
}

.leaflet-control-search {
  opacity: 0;
  border: 2px solid rgba(0,0,0,0.2);
  border-radius: 4px;

  &.show {
    animation: fade-in 300ms ease-in forwards;
  }

  button {
    background-color: white;
    border: none;

    &:hover {
      background-color: #f4f4f4;
    }
  }
}

@keyframes fade-in {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
