<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import 'leaflet-edgebuffer'
import 'leaflet-gesture-handling'
import { tiledMapLayer } from 'esri-leaflet'

import aquiferLayers from '../layers'
import { buildLegendHTML } from '../legend'
import wellsAquiferIcon from '../../common/assets/images/wells-aquifer.svg'
import uncorrelatedWellsIcon from '../../common/assets/images/wells-uncorrelated.svg'
import emsWellsIcon from '../../common/assets/images/wells-ems.svg'

const LAYER_AQUIFER_WELLS = { layerName: 'Wells near aquifer', legend: wellsAquiferIcon, show: true }
const LAYER_UNCORRELATED_WELLS = { layerName: 'Wells not correlated to aquifer', legend: uncorrelatedWellsIcon, show: false }
const LAYER_EMS_WELLS = { layerName: 'EMS wells in aquifer', legend: emsWellsIcon, show: false }

const DEFAULT_CIRCLE_MARKER_OPTIONS = {
  radius: 3,
  fillColor: '#0162fe',
  fillOpacity: 1,
  stroke: true,
  color: '#000', // stroke color
  weight: 1, // stroke width
  opacity: 1
}

const UNCORRELATED_WELL_CIRCLE_MARKER_OPTIONS_OVERRIDES = {
  fillColor: 'white',
  opacity: 1,
  fillOpacity: 1
}

const EMS_WELL_CIRCLE_MARKER_OPTIONS_OVERRIDES = {
  fillColor: '#0CA287',
  opacity: 1,
  fillOpacity: 1
}

const AQUIFER_LAYER_STYLES = {
  color: '#FF6500',
  fillOpacity: 0.1
}

export default {
  name: 'SingleAquiferMap',
  props: ['aquifer-id', 'geom', 'wells', 'loading'],
  data () {
    return {
      map: null,
      legendControlContent: null,
      activeLayers: {}
    }
  },
  computed: {
    correlatedWells () {
      return this.wells.filter(w => w.aquifer_id !== null)
    },
    emsWells () {
      return this.correlatedWells.filter(w => w.ems !== null)
    },
    uncorrelatedWells () {
      return this.wells.filter(w => w.aquifer_id === null)
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
        gestureHandling: true,
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
      const layersControl = L.control.layers(null, aquiferLayers, { collapsed: false })
      layersControl.addTo(this.map)
      const cadastralLayer = aquiferLayers['Cadastral']
      cadastralLayer.addTo(this.map)
      const wellsAllLayer = aquiferLayers['Wells']
      wellsAllLayer.addTo(this.map)

      Object.keys(aquiferLayers).forEach((layerName) => {
        const layer = aquiferLayers[layerName]
        this.activeLayers[layerName] = {
          layerName: layer.options.name,
          legend: layer.options.legend,
          show: false
        }
      })
      this.activeLayers[cadastralLayer.options.name].show = true
      this.activeLayers[wellsAllLayer.options.name].show = true

      // Add non-image tile layers
      this.activeLayers.aquiferWells = LAYER_AQUIFER_WELLS
      this.activeLayers.uncorrelatedWells = LAYER_UNCORRELATED_WELLS
      this.activeLayers.emsWells = LAYER_EMS_WELLS

      this.addWellsLayersControl(layersControl)

      this.map.addControl(this.getLegendControl())

      this.canvasRenderer = L.canvas({ padding: 0.1 })

      this.canvasLayer = L.layerGroup()
      this.canvasLayer.addTo(this.map)

      this.updateCanvasLayer()
      if (this.geom) {
        this.zoomToAquifer()
      }

      this.listenForLayerAdd()
      this.listenForLayerRemove()
      this.listenForLayerToggle()

      this.$emit('activeLayers', this.activeLayers)
    },
    addWellsLayersControl (layersControl) {
      const overlaysContainer = layersControl.getContainer().querySelector('.leaflet-control-layers-overlays')

      const layerNames = [ 'uncorrelatedWells', 'emsWells' ]

      layerNames.forEach((name) => {
        const checked = this.activeLayers[name].show ? 'checked' : ''
        const wellsLayerControlLabel = document.createElement('label')
        wellsLayerControlLabel.innerHTML =
        '<div>' +
          '<input type="checkbox" class="leaflet-control-layers-selector" ' + checked + '>' +
          '<span> ' + this.activeLayers[name].layerName + '</span>' +
        '</div>'
        const emsWellsCheckbox = wellsLayerControlLabel.querySelector('input')
        emsWellsCheckbox.onchange = (e) => {
          this.toggleLayerOnCanvas(name, e.currentTarget.checked)
        }

        overlaysContainer.appendChild(wellsLayerControlLabel)
      })
    },
    toggleLayerOnCanvas (name, show) {
      this.activeLayers[name].show = show
      this.$emit('activeLayers', this.activeLayers)
      this.updateWellsCanvasLayer()
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
        const layers = {}
        Object.keys(data).forEach((key) => {
          if (key === 'aquiferWells') { return }
          layers[key] = data[key]
        })

        this.legendControlContent.innerHTML = buildLegendHTML(layers)
      })
    },
    listenForLayerRemove () {
      this.map.on('overlayremove', (e) => {
        const { legend, name } = e.layer.options
        if (legend) {
          this.activeLayers[name].show = false
          if (name === 'Wells') {
            this.activeLayers.aquiferWells.show = false
            this.updateWellsCanvasLayer()
          }
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    listenForLayerAdd () {
      this.map.on('overlayadd', (e) => {
        const { legend, name } = e.layer.options
        if (legend) {
          this.activeLayers[name].show = true
          if (name === 'Wells') {
            this.activeLayers.aquiferWells.show = true
            this.updateWellsCanvasLayer()
          }
          this.$emit('activeLayers', this.activeLayers)
        }
      })
    },
    updateCanvasLayer () {
      this.canvasLayer.clearLayers()

      this.buildAquiferLayer()

      this.buildWellLayers()

      if (!this.loading) {
        if (this.aquiferLayer) {
          this.canvasLayer.addLayer(this.aquiferLayer)
        }

        if (this.wellsLayer) {
          this.updateWellsCanvasLayer()
          this.canvasLayer.addLayer(this.wellsLayer)
        }
      }
    },
    updateWellsCanvasLayer () {
      if (!this.wellsLayer) { return }
      this.wellsLayer.getLayers().forEach((layer) => {
        this.updateWellLayerStyle(layer)
      })
    },
    buildAquiferLayer () {
      if (!this.geom) { return }

      if (this.aquiferLayer) {
        this.aquiferLayer.remove()
      }

      const options = {
        style: AQUIFER_LAYER_STYLES,
        renderer: this.canvasRenderer
      }
      this.aquiferLayer = L.geoJSON(this.geom, options)
      this.aquiferLayer.bindTooltip(`Aquifer ${this.aquiferId}`, { sticky: true })
    },
    buildWellLayers (wells) {
      if (this.wellsLayer) {
        this.wellsLayer.remove()
      }
      this.wellsLayer = L.layerGroup()

      this.wells.forEach((well) => {
        const wellCircleMarker = this.buildWellMarker(well)

        if (!wellCircleMarker) { return } // Couldn't be built - skip this well (likely no lat/lng)

        this.wellsLayer.addLayer(wellCircleMarker)
      })
    },
    buildWellMarker (well) {
      const { latitude, longitude } = well

      if (!latitude || !longitude) { return } // wells might not have lat / lng

      let correlatedAquiferItem = 'Uncorrelated well'
      if (well.aquifer_id) {
        correlatedAquiferItem = `Correlated to aquifer ${well.aquifer_id}`
      }

      const wellCircleMarker = L.circleMarker(L.latLng(latitude, longitude), this.getWellLayerStyle(well))
      const wellTooltip = [
        `Well Tag Number: ${well.well_tag_number}`,
        `Identification Plate Number: ${well.identification_plate_number || '—'}`,
        `Address: ${well.street_address || 'N/A'}`,
        correlatedAquiferItem,
        well.ems ? `EMS ID: ${well.ems}` : null
      ].filter(Boolean).join('<br>')

      wellCircleMarker.bindPopup(this.createWellPopupContent(well))
      wellCircleMarker.on('mouseover', () => {
        if (!wellCircleMarker.isPopupOpen()) {
          wellCircleMarker.bindTooltip(wellTooltip)
          wellCircleMarker.openTooltip()
        }
      })
      wellCircleMarker.on('click', () => {
        wellCircleMarker.unbindTooltip()
      })

      wellCircleMarker.well = well

      return wellCircleMarker
    },
    createWellPopupContent (well) {
      return () => {
        const routes = [
          { name: 'wells-detail', params: { id: well.well_tag_number } },
          { name: 'aquifers-view', params: { id: well.aquifer_id } }
        ]

        let correlatedAquiferItem = 'Uncorrelated well'
        if (well.aquifer_id) {
          correlatedAquiferItem = `Correlated to aquifer ${well.aquifer_id}`
          if (well.aquifer_id !== this.aquiferId) { // well is correlated to diff aquifer = link it
            const aquiferDetailsUrl = this.$router.resolve(routes[1])
            correlatedAquiferItem = `Correlated to <a href="${aquiferDetailsUrl.href}">aquifer ${well.aquifer_id}</a>`
          }
        }

        const url = this.$router.resolve(routes[0])
        const container = L.DomUtil.create('div', 'leaflet-popup-aquifer')
        container.innerHTML = [
          `<a href="${url.href}">Well ${well.well_tag_number}</a>`,
          `Identification Plate Number: ${well.identification_plate_number || '—'}`,
          `Address: ${well.street_address || 'N/A'}`,
          correlatedAquiferItem,
          well.ems ? `EMS ID: ${well.ems}` : null
        ].filter(Boolean).join('<br>')
        const anchors = container.querySelectorAll('a')
        for (let i = 0; i < anchors.length; i++) {
          L.DomEvent.on(anchors[i], 'click', (e) => {
            if (!e.ctrlKey) {
              e.preventDefault()
              this.$router.push(routes[i])
            }
          })
        }
        return container
      }
    },
    getWellLayerStyle (well) {
      const { ems, aquifer_id: aquiferId } = well

      let style = {
        ...DEFAULT_CIRCLE_MARKER_OPTIONS,
        renderer: this.canvasRenderer
      }

      if (!this.activeLayers.aquiferWells.show) {
        Object.assign(style, {
          opacity: 0,
          fillOpacity: 0
        })
      }
      if (this.activeLayers.uncorrelatedWells.show && !aquiferId) {
        Object.assign(style, UNCORRELATED_WELL_CIRCLE_MARKER_OPTIONS_OVERRIDES)
      }
      if (this.activeLayers.emsWells.show && ems) {
        Object.assign(style, EMS_WELL_CIRCLE_MARKER_OPTIONS_OVERRIDES)
      }

      return style
    },
    updateWellLayerStyle (layer) {
      layer.setStyle(this.getWellLayerStyle(layer.well))
    },
    zoomToAquifer () {
      // Set map view to aquifer
      this.map.fitBounds(this.aquiferLayer.getBounds())
    }
  },
  watch: {
    geom (newGeom, oldGeom) {
      if (oldGeom || newGeom) {
        this.updateCanvasLayer()
        this.zoomToAquifer()
      }
    },
    wells (newWells, oldWells) {
      if (oldWells || newWells) {
        this.updateCanvasLayer()
      }
    },
    uncorrelatedWells (newWells, oldWells) {
      if (oldWells || newWells) {
        this.updateCanvasLayer()
      }
    },
    loading () {
      this.updateCanvasLayer()
    }
  }
}
</script>
<style>
@import "~leaflet/dist/leaflet.css";
@import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";

.map {
  height: 500px;
}

.leaflet-control-legend {
  background-color: white;
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
  border-radius: 0.1em;
}

.leaflet-control-legend li {
  line-height: 20px;
}

.leaflet-control-layers label:last-child {
  margin-bottom: 0;
}
</style>
