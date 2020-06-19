/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
  <div id="aquifer-search-map" class="map"/>
</template>

<script>
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'
import { difference, uniq } from 'lodash'
import { mapGetters } from 'vuex'

import { SEARCH_AQUIFERS } from '../store/actions.types'
import {
  DATABC_ROADS_SOURCE,
  DATABC_CADASTREL_SOURCE,
  WELLS_SOURCE_ID,
  AQUIFERS_SOURCE_ID,
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER,
  DATABC_CADASTREL_LAYER_ID,
  wellsBaseAndArtesianLayer,
  aquifersLineLayer,
  aquifersFillLayer,
  setupAquiferHover,
  DATABC_ECOCAT_LAYER_ID,
  DATABC_SURFACE_WATER_LICENCES_LAYER_ID,
  DATABC_ECOCAT_SOURCE,
  DATABC_ECOCAT_SOURCE_ID,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  AQUIFERS_FILL_LAYER_ID,
  aquiferLayerFilter,
  wellLayerFilter,
  DATABC_GROUND_WATER_LICENCES_LAYER_ID,
  DATABC_WATER_LICENCES_SOURCE,
  DATABC_WATER_LICENCES_SOURCE_ID,
  groundWaterLicencesLayer,
  surfaceWaterLicencesLayer,
  ecoCatLayer,
  WELLS_SOURCE,
  AQUIFERS_SOURCE,
  observationWellsLayer,
  WELLS_OBSERVATION_LAYER_ID
} from '../../common/mapbox/layers'
import {
  LayersControl,
  LegendControl,
  BoxZoomControl,
  SearchAreaControl,
  DataBCGeocoder
} from '../../common/mapbox/controls'
import features from '../../common/features'
import { DEFAULT_MAP_ZOOM, CENTRE_LNG_LAT_BC } from '../../common/mapbox/geometry'
import {
  createAquiferPopupElement,
  createWellPopupElement,
  createEcocatPopupElement,
  createWaterLicencePopupElement
} from '../popup'

import cadastralLegendSrc from '../../common/assets/images/cadastral.png'
import ecoCatWaterLegendSrc from '../../common/assets/images/ecocat-water.svg'
import surfaceWaterLicenceActiveLegendSrc from '../../common/assets/images/swater-licence-active.svg'
import groundWaterLicenceActiveLegendSrc from '../../common/assets/images/gwater-licence.svg'
import ecoCatGroundWaterLegendSrc from '../../common/assets/images/ecocat-groundwater.svg'
import observationWellInactiveLegendSrc from '../../common/assets/images/owells-inactive.svg'
import observationWellActiveLegendSrc from '../../common/assets/images/owells-active.svg'
import wellsAllLegendSrc from '../../common/assets/images/wells-all.svg'
import wellsArtesianLegendSrc from '../../common/assets/images/wells-artesian.svg'
import { setupFeatureTooltips } from '../../common/mapbox/popup'

export default {
  name: 'AquiferMap',
  props: [
    'initialZoom',
    'initialCentre',
    'highlightAquiferIds',
    'selectedId',
    'viewBounds',
    'searchText',
    'showRetired'
  ],
  data () {
    return {
      map: null,
      browserUnsupported: false,
      activeLayers: [],
      searchMapButtonEnabled: Boolean(this.searchText),
      mapLayers: [
        {
          show: true,
          id: DATABC_CADASTREL_LAYER_ID,
          label: 'Cadastrals',
          imageSrc: cadastralLegendSrc
        },
        {
          show: false,
          id: DATABC_ECOCAT_LAYER_ID,
          label: 'EcoCat',
          legend: [
            {
              imageSrc: ecoCatGroundWaterLegendSrc,
              label: 'groundwater reports'
            },
            {
              imageSrc: ecoCatWaterLegendSrc,
              label: 'water related reports'
            }
          ]
        },
        {
          show: false,
          id: DATABC_SURFACE_WATER_LICENCES_LAYER_ID,
          label: 'Surface water licences',
          imageSrc: surfaceWaterLicenceActiveLegendSrc
        },
        {
          show: false,
          id: DATABC_GROUND_WATER_LICENCES_LAYER_ID,
          label: 'Groundwater licences',
          imageSrc: groundWaterLicenceActiveLegendSrc
        },
        {
          show: false,
          id: WELLS_BASE_AND_ARTESIAN_LAYER_ID,
          label: 'Wells',
          legend: [
            {
              imageSrc: wellsAllLegendSrc,
              label: 'all'
            },
            {
              imageSrc: wellsArtesianLegendSrc,
              label: 'artesian'
            }
          ]
        },
        {
          show: false,
          id: WELLS_OBSERVATION_LAYER_ID,
          label: 'Observation wells',
          legend: [
            {
              imageSrc: observationWellActiveLegendSrc,
              label: 'active'
            },
            {
              imageSrc: observationWellInactiveLegendSrc,
              label: 'inactive'
            }
          ]
        }
      ],
      previousHighlightedAquiferIds: []
    }
  },
  mounted () {
    this.$emit('mapLoading')

    // On reset or basic search, clear local params
    this.unsubscribeAction = this.$store.subscribeAction((action, state) => {
      if (action.type === `aquiferStore/search/${SEARCH_AQUIFERS}`) {
        this.hideMapSearchButton()
      }
    })

    this.initMapBox()

    this.listenForReset()
  },
  destroyed () {
    this.unsubscribeAction()
    this.map.remove()
    this.map = null
  },
  computed: {
    ...mapGetters(['userRoles']),
    highlightIdsMap () {
      return this.highlightAquiferIds.reduce((obj, aquiferId) => {
        obj[aquiferId] = aquiferId
        return obj
      }, {})
    },
    showUnpublishedAquifers () {
      return Boolean(this.userRoles.aquifers.edit)
    },
    showUnpublishedWells () {
      return Boolean(this.userRoles.wells.edit)
    }
  },
  methods: {
    initMapBox () {
      if (!mapboxgl.supported()) {
        this.browserUnsupported = true
        return
      }

      const zoom = this.initialZoom || DEFAULT_MAP_ZOOM
      const centre = this.initialCentre ? this.initialCentre : CENTRE_LNG_LAT_BC

      var mapConfig = {
        container: this.$el,
        zoom,
        minZoom: 4,
        maxPitch: 0,
        dragRotate: false,
        center: centre,
        style: this.buildMapStyle()
      }

      this.map = new mapboxgl.Map(mapConfig)

      this.addTopCentreControlConainer()

      new GestureHandling({ modifierKey: 'ctrl' }).addTo(this.map)

      /* Add controls */

      this.map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-left')
      this.map.addControl(new mapboxgl.FullscreenControl(), 'top-left')
      this.map.addControl(new DataBCGeocoder(), 'top-left')
      this.map.addControl(new BoxZoomControl({
        onZoom: this.zoomToBBox
      }), 'top-left')
      this.map.addControl(new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true
        }
      }), 'top-left')
      this.map.addControl(new mapboxgl.ScaleControl({
        maxWidth: 80,
        unit: 'imperial'
      }))
      this.map.addControl(new mapboxgl.ScaleControl({
        maxWidth: 80,
        unit: 'metric'
      }))
      this.map.addControl(new mapboxgl.AttributionControl({
        customAttribution: 'MapBox | Government of British Columbia, DataBC, GeoBC '
      }))
      this.layersControl = new LayersControl({
        layers: this.mapLayers,
        onChange: this.layersChanged
      })
      this.map.addControl(this.layersControl)
      this.legendControl = new LegendControl({
        layers: this.mapLayers
      })
      this.map.addControl(this.legendControl, 'bottom-right')
      this.searchAreaControl = new SearchAreaControl({
        show: false,
        onClick: this.searchButtonClicked
      })
      this.map.addControl(this.searchAreaControl, 'top-centre')

      this.listenForMapMovement()

      this.listenForZoom()

      this.map.on('load', () => {
        /* Setup tooltips  */
        const tooltipLayers = {
          [AQUIFERS_FILL_LAYER_ID]: {
            createTooltipContent: this.createAquiferPopupElement
          },
          [DATABC_ECOCAT_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createEcocatPopupElement
          },
          [DATABC_SURFACE_WATER_LICENCES_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createSurfaceWaterLicencePopupElement
          },
          [DATABC_GROUND_WATER_LICENCES_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createGroundWaterLicencePopupElement
          },
          [DATABC_GROUND_WATER_LICENCES_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createGroundWaterLicencePopupElement
          },
          [WELLS_OBSERVATION_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          },
          [WELLS_BASE_AND_ARTESIAN_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          }
        }

        setupFeatureTooltips(this.map, tooltipLayers)

        /* Setup aquifer hover effect */
        setupAquiferHover(this.map, AQUIFERS_FILL_LAYER_ID)

        this.setHighlightedAquifers(this.highlightAquiferIds, true)

        if (this.highlightAquiferIds.length > 0) {
          this.zoomToMapBounds()
        }

        this.$emit('mapLoaded')
      })
    },
    buildMapStyle () {
      return {
        version: 8,
        sources: {
          [DATABC_ROADS_SOURCE_ID]: DATABC_ROADS_SOURCE,
          [DATABC_CADASTREL_SOURCE_ID]: DATABC_CADASTREL_SOURCE,
          [DATABC_ECOCAT_SOURCE_ID]: DATABC_ECOCAT_SOURCE,
          [DATABC_WATER_LICENCES_SOURCE_ID]: DATABC_WATER_LICENCES_SOURCE,
          [WELLS_SOURCE_ID]: WELLS_SOURCE,
          [AQUIFERS_SOURCE_ID]: AQUIFERS_SOURCE
        },
        layers: [
          DATABC_ROADS_LAYER,
          DATABC_CADASTREL_LAYER,
          aquifersFillLayer({ filter: aquiferLayerFilter(this.showUnpublishedAquifers, this.showRetired) }),
          aquifersLineLayer({ filter: aquiferLayerFilter(this.showUnpublishedAquifers, this.showRetired) }),
          ecoCatLayer({ layout: { visibility: 'none' } }),
          surfaceWaterLicencesLayer({ layout: { visibility: 'none' } }),
          groundWaterLicencesLayer({ layout: { visibility: 'none' } }),
          wellsBaseAndArtesianLayer({ layout: { visibility: 'none' }, filter: wellLayerFilter(this.showUnpublishedWells) }),
          observationWellsLayer({ layout: { visibility: 'none' } }),
        ]
      }
    },
    addTopCentreControlConainer () {
      const positionName = 'top-centre'
      const positionContainer = document.createElement('div')
      positionContainer.className = `mapboxgl-ctrl-${positionName}`
      this.map._controlContainer.appendChild(positionContainer)
      this.map._controlPositions[positionName] = positionContainer
    },
    layersChanged (layerId, show) {
      // Find the layer and mark it as shown so the legend can be updated properly
      this.mapLayers.find((layer) => layer.id === layerId).show = show

      this.legendControl.update()

      // Turn the layer's visibility on / off
      this.map.setLayoutProperty(layerId, 'visibility', show ? 'visible' : 'none')
    },
    listenForReset () {
      this.$parent.$on('resetLayers', (data) => {
        this.hideMapSearchButton()
        this.supressShowMapSearchButton = true

        this.mapLayers.forEach((layer) => {
          let show = false
          if (layer.id === DATABC_CADASTREL_LAYER_ID) {
            show = true
          }
          layer.show = show
          this.map.setLayoutProperty(layer.id, 'visibility', layer.show ? 'visible' : 'none')
        })
        this.layersControl.update()
        this.legendControl.update()
        this.map.flyTo({ center: CENTRE_LNG_LAT_BC, zoom: DEFAULT_MAP_ZOOM })
        this.map.fire('reset')
      })
    },
    hideMapSearchButton () {
      window.clearTimeout(this.showMapSearchButtonTimer)
      this.showMapSearchButtonTimer = null
      this.searchAreaControl.hide()
    },
    showMapSearchButton () {
      if (!features.searchInAquiferMap) { return }
      if (this.showMapSearchButtonTimer) { return }
      this.showMapSearchButtonTimer = window.setTimeout(() => {
        this.showMapSearchButtonTimer = null
        if (!this.supressShowMapSearchButton) {
          this.searchAreaControl.show()
        } else {
          this.supressShowMapSearchButton = false
        }
      }, 500)
    },
    zoomToBBox (bbox) {
      if (bbox) {
        this.map.fitBounds(bbox)
      }
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
          const visibleFeatures = this.map.queryRenderedFeatures({ layers: [ AQUIFERS_FILL_LAYER_ID ] })
          const bounds = this.map.getBounds()
          const aquiferIds = visibleFeatures.map((l) => l.properties.aquifer_id)
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
    zoomToMapBounds () {
      if (this.viewBounds) {
        this.supressShowMapSearchButton = true
        this.map.fitBounds(this.viewBounds, { padding: 40 })
      }
    },
    setSelectedAquifer (aquiferId, selected = true) {
      this.map.setFeatureState(
        { source: AQUIFERS_SOURCE_ID, id: aquiferId, sourceLayer: AQUIFERS_SOURCE_ID },
        { selected }
      )
    },
    setHighlightedAquifers (aquiferIds, highlight = true) {
      aquiferIds.forEach((aquiferId) => {
        this.map.setFeatureState(
          { source: AQUIFERS_SOURCE_ID, id: aquiferId, sourceLayer: AQUIFERS_SOURCE_ID },
          { searchResult: highlight }
        )
      })
    },
    createAquiferPopupElement (features, { canInteract }) {
      return createAquiferPopupElement(features, this.map, this.$router, {
        canInteract,
        aquiferLayerIds: [ AQUIFERS_FILL_LAYER_ID ]
      })
    },
    createWellPopupElement (features, { canInteract }) {
      return createWellPopupElement(features, this.map, this.$router, {
        canInteract,
        wellLayerIds: [ WELLS_BASE_AND_ARTESIAN_LAYER_ID, WELLS_OBSERVATION_LAYER_ID ]
      })
    },
    createEcocatPopupElement (features, { canInteract }) {
      return createEcocatPopupElement(features, this.map, {
        canInteract,
        ecocatLayerIds: [ DATABC_ECOCAT_LAYER_ID ]
      })
    },
    createSurfaceWaterLicencePopupElement (features, { canInteract }) {
      return createWaterLicencePopupElement(features, this.map, this.$router, {
        canInteract,
        ecocatLayerIds: [ DATABC_ECOCAT_LAYER_ID ]
      })
    },
    createGroundWaterLicencePopupElement (features, { canInteract }) {
      return createWaterLicencePopupElement(features, this.map, this.$router, {
        canInteract,
        ecocatLayerIds: [ DATABC_ECOCAT_LAYER_ID ]
      })
    }
  },
  watch: {
    highlightAquiferIds (newIds, oldIds) {
      const newlyHighlightedIds = difference(newIds, oldIds)
      const noLongerHighlightedIds = difference(oldIds, newIds)
      this.setHighlightedAquifers(noLongerHighlightedIds, false)
      this.setHighlightedAquifers(newlyHighlightedIds, true)

      if (newIds.length > 0) {
        this.zoomToMapBounds()
      }
    },
    selectedId (newId, oldId) {
      if (oldId) {
        this.setSelectedAquifer(oldId, false)
      }

      if (newId) {
        this.setSelectedAquifer(newId, true)
      }

      this.zoomToMapBounds()
    },
    searchText (searchQuery) {
      this.searchMapButtonEnabled = Boolean(searchQuery)
    },
    showRetired () {
      this.map.setStyle(this.buildMapStyle())
    },
    userRoles () {
      this.map.setStyle(this.buildMapStyle())
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";
@import "~@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";

#aquifer-search-map {
  height: 600px;
}
</style>
