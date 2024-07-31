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
  <div id="wells-search-map" class="map"/>
</template>

<script>
import axios from 'axios'
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'
import { debounce } from 'lodash'

import ApiService from '@/common/services/ApiService.js'

import {
  DATABC_ROADS_SOURCE,
  DATABC_CADASTREL_SOURCE,
  WELLS_SOURCE_ID,
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER,
  wellsBaseAndArtesianLayer,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  searchedWellsLayer,
  SEARCHED_WELLS_SOURCE_ID,
  FOCUSED_WELLS_SOURCE_ID,
  focusedWellsLayer,
  FOCUSED_WELL_IMAGE_ID,
  FOCUSED_WELL_ARTESIAN_IMAGE_ID,
  FOCUSED_WELL_CLOSED_IMAGE_ID,
  wellLayerFilter,
  SEARCHED_WELLS_LAYER_ID,
  WELLS_SOURCE
} from '../../common/mapbox/layers'
import { LegendControl, BoxZoomControl, SearchOnMoveControl, ClearSearchCriteriaControl } from '../../common/mapbox/controls'
import { createWellPopupElement } from '../popup'
import { PulsingWellImage, PulsingArtesianWellImage, PulsingClosedWellImage } from '../../common/mapbox/images'
import { DEFAULT_MAP_ZOOM, CENTRE_LNG_LAT_BC, buildWellsGeoJSON, convertLngLatBoundsToDirectionBounds, boundsCompletelyContains } from '../../common/mapbox/geometry'

import { RESET_WELLS_SEARCH, SEARCH_WELLS } from '../../wells/store/actions.types'

import wellsAllLegendSrc from '../../common/assets/images/wells-all.svg'
import wellsArtesianLegendSrc from '../../common/assets/images/wells-artesian.svg'
import wellsClosedLegendSrc from '../../common/assets/images/wells-closed.svg'
import { mapGetters } from 'vuex'
import { setupFeatureTooltips } from '../../common/mapbox/popup'

const WELL_FEATURE_PROPERTIES_FOR_POPUP = [
  'well_tag_number',
  'identification_plate_number',
  'street_address',
  'is_published'
]
const FOCUSED_WELL_PROPERTIES = WELL_FEATURE_PROPERTIES_FOR_POPUP.concat(['artesian_conditions', 'well_status'])

export default {
  name: 'SearchMap',
  props: [
    'initialZoom',
    'initialCentre',
    'focusedWells'
  ],
  data () {
    return {
      map: null,
      browserUnsupported: false,
      mapLayers: [
        {
          show: true,
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
            },
            {
              imageSrc: wellsClosedLegendSrc,
              label: 'closed/abandoned'
            }
          ]
        }
      ],
      searchOnMapMove: true,
      movedSinceLastSearch: false,

      pendingLocationSearch: null,
      searchInProgress: false,
      hasMapBeenReset: false
    }
  },
  mounted () {
    this.initMapBox()

    // When the search is reset - fly the map back to view all of BC
    this.unsubscribeAction = this.$store.subscribeAction((action, state) => {
      if (action.type === SEARCH_WELLS) {
        this.hasMapBeenReset = false
        this.loadWells()
      } else if (action.type === RESET_WELLS_SEARCH) {
        // Check to make sure we don't accidentially reset the map again
        if (!this.hasMapBeenReset) {
          this.resetMap()
        }
      }
    })
  },
  destroyed () {
    this.unsubscribeAction()
    this.map.remove()
    this.map = null
  },
  computed: {
    ...mapGetters(['userRoles', 'searchQueryParams']),
    hasSearchParams (state) {
      return Object.keys(this.searchQueryParams).length > 0
    },
    showUnpublished () {
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

      new GestureHandling({ modifierKey: 'ctrl' }).addTo(this.map)

      /* Add controls */

      this.map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-left')
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

      this.searchOnMoveControl = new SearchOnMoveControl({
        show: this.hasSearchParams,
        searchOnMapMove: this.searchOnMapMove,
        onSearchThisArea: () => this.triggerSearchMapArea(),
        onSearchAsIMove: (e) => (this.searchOnMapMove = e.checked)
      })
      this.map.addControl(this.searchOnMoveControl, 'top-right')

      this.clearSearchCriteriaControl = new ClearSearchCriteriaControl({
        show: this.hasSearchParams,
        onClearClick: this.clearSearch
      })
      this.map.addControl(this.clearSearchCriteriaControl, 'bottom-right')

      this.legendControl = new LegendControl({
        layers: this.mapLayers
      })
      this.map.addControl(this.legendControl, 'bottom-right')

      this.listenForMapMovement()

      this.map.on('load', () => {
        this.map.addImage(FOCUSED_WELL_ARTESIAN_IMAGE_ID, new PulsingArtesianWellImage(this.map), { pixelRatio: 2 })
        this.map.addImage(FOCUSED_WELL_IMAGE_ID, new PulsingWellImage(this.map), { pixelRatio: 2 })
        this.map.addImage(FOCUSED_WELL_CLOSED_IMAGE_ID, new PulsingClosedWellImage(this.map), { pixelRatio: 2 })

        const tooltipLayers = {
          [WELLS_BASE_AND_ARTESIAN_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          },
          [SEARCHED_WELLS_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          }
        }

        setupFeatureTooltips(this.map, tooltipLayers)

        this.setFocusedWells(this.focusedWells)

        if (this.hasSearchParams) { // must be an existing search so load wells in view
          this.loadWells()
        }

        const mapBounds = this.map.getBounds()

        this.$emit('mapLoaded', mapBounds)
      })
    },
    buildMapStyle () {
      return {
        version: 8,
        sources: {
          [DATABC_ROADS_SOURCE_ID]: DATABC_ROADS_SOURCE,
          [DATABC_CADASTREL_SOURCE_ID]: DATABC_CADASTREL_SOURCE,
          [WELLS_SOURCE_ID]: WELLS_SOURCE,
          [SEARCHED_WELLS_SOURCE_ID]: { type: 'geojson', data: buildWellsGeoJSON([]) },
          [FOCUSED_WELLS_SOURCE_ID]: { type: 'geojson', data: buildWellsGeoJSON([]) }
        },
        layers: [
          DATABC_ROADS_LAYER,
          DATABC_CADASTREL_LAYER,
          wellsBaseAndArtesianLayer({ filter: wellLayerFilter(this.showUnpublished) }),
          searchedWellsLayer(),
          focusedWellsLayer()
        ]
      }
    },
    resetMap () {
      this.map.fire('reset')
      this.flyToBC()
      this.clearWellSearchResultsLayer()
      this.setFocusedWells([])
      this.hasMapBeenReset = true
    },
    zoomToBBox (bbox) {
      if (bbox) {
        this.map.fitBounds(bbox)
      }
    },
    listenForMapMovement () {
      ['zoomend', 'moveend', 'resize'].forEach((eventName) => {
        this.map.on(eventName, (e) => {
          this.$emit('boundsChanged', this.map.getBounds(), this.map.getZoom(), this.map.getCenter())
          this.deboucedBoundsUpdated(this)
        })
      })
    },
    deboucedBoundsUpdated: debounce((vm) => {
      vm.movedSinceLastSearch = true
      if (vm.searchOnMapMove) {
        // Only emit a 'search' when the map was moved because of the user, not when the reset
        // button was clicked.
        if (!vm.hasMapBeenReset) {
          vm.$emit('search', vm.map.getBounds(), { showLoadingSpinner: false })
        }
        vm.loadWells()
      }
      vm.hasMapBeenReset = false
    }, 500),
    loadWells () {
      if (this.hasSearchParams) {
        this.fetchWellsGeoJSON()
      } else {
        this.$emit('wellsLoaded', 0)
      }
    },
    triggerSearchMapArea () {
      this.$emit('search', this.map.getBounds(), { showLoadingSpinner: true })
      this.searchOnMoveControl.showSearchAreaButton(false)
    },
    clearSearch () {
      this.setFocusedWells([])
      this.clearWellSearchResultsLayer()
      this.clearSearchCriteriaControl.toggleShow(false)
      this.$emit('clearSearch')
    },
    boundsOfFocusedWells () {
      const bounds = new mapboxgl.LngLatBounds()
      this.focusedWells.forEach((well) => {
        bounds.extend(new mapboxgl.LngLat(well.longitude, well.latitude))
      })
      return bounds
    },
    fetchWellsGeoJSON () {
      if (this.pendingLocationSearch !== null) {
        this.searchInProgress = false
        this.pendingLocationSearch.cancel()
        this.pendingLocationSearch = null
      }

      this.pendingLocationSearch = axios.CancelToken.source()

      const params = {
        ...this.searchQueryParams,
        ...convertLngLatBoundsToDirectionBounds(this.map.getBounds()),
        geojson: true
      }

      this.searchInProgress = true
      this.$emit('wellsLoading')

      ApiService.query('wells/locations', params, { cancelToken: this.pendingLocationSearch.token })
        .then(
          // resolved
          (response) => {
            this.searchInProgress = false
            this.searchOnMapMove = true
            this.movedSinceLastSearch = false
            this.pendingLocationSearch = null

            const features = response.data.features
            this.$emit('wellsLoaded', features.length)

            if (features.length === 0) {
              this.$emit('error', { noFeatures: true })
            }

            this.updateWellSearchResultsLayer(response.data)
          }, (err) => { // rejected
            // If the search was cancelled, a new one is pending, so don't bother resetting.
            if (axios.isCancel(err)) { return }

            this.searchInProgress = false

            const errorMessage = err.response && err.response.data
              ? err.response.data.detail
              : 'Server error'

            this.$emit('error', { serverError: errorMessage })
            this.$emit('wellsLoaded', 0)

            this.clearWellSearchResultsLayer()
          }
        )
    },
    updateWellSearchResultsLayer (geoJSON) {
      if (this.map) { // map could have been unloaded by the time this function is called
        this.map.getSource(SEARCHED_WELLS_SOURCE_ID).setData(geoJSON)
      }
    },
    clearWellSearchResultsLayer () {
      this.updateWellSearchResultsLayer(buildWellsGeoJSON([]))
    },
    setFocusedWells (wells) {
      this.map.getSource(FOCUSED_WELLS_SOURCE_ID).setData(buildWellsGeoJSON(wells, FOCUSED_WELL_PROPERTIES))
    },
    flyToBC () {
      this.map.flyTo({ center: CENTRE_LNG_LAT_BC, zoom: DEFAULT_MAP_ZOOM })
    },
    flyToBounds (bounds) {
      this.map.fitBounds(bounds, { duration: 1 * 1000, padding: 60 })
    },
    createWellPopupElement (features, { canInteract }) {
      return createWellPopupElement(features, this.map, this.$router, {
        canInteract,
        wellLayerIds: [
          WELLS_BASE_AND_ARTESIAN_LAYER_ID,
          SEARCHED_WELLS_LAYER_ID
        ]
      })
    }
  },
  watch: {
    focusedWells (wells) {
      this.setFocusedWells(wells)

      if (wells.length > 0) {
        if (wells.length === 1) {
          const { longitude, latitude } = wells[0]
          const wellLngLat = [longitude, latitude]
          if (!this.map.getBounds().contains(wellLngLat)) { // if not in view
            this.map.flyTo({ center: wellLngLat, zoom: 10 })
          }
        } else {
          const focusedWellsBounds = this.boundsOfFocusedWells()

          if (!boundsCompletelyContains(this.map.getBounds(), focusedWellsBounds)) {
            // We can't see all focused wells then fly them into view
            this.flyToBounds(this.boundsOfFocusedWells())
          }
        }
      }
    },
    searchInProgress (isLoading) {
      this.searchOnMoveControl.loading(isLoading)
    },
    hasSearchParams (hasSearchParams) {
      this.searchOnMoveControl.toggleShow(hasSearchParams)
      this.clearSearchCriteriaControl.toggleShow(hasSearchParams)
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

#wells-search-map {
  height: 600px;
}
</style>
