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
  vectorSourceConfig,
  WELLS_SOURCE_ID,
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER,
  wellsBaseAndArtesianLayer,
  DATABC_OBSERVATION_WELLS_LAYER,
  DATABC_WATER_LICENCES_LAYER,
  DATABC_ECOCAT_LAYER,
  DATABC_ECOCAT_SOURCE,
  DATABC_WATER_LICENCES_SOURCE_ID,
  DATABC_ECOCAT_SOURCE_ID,
  DATABC_OBSERVATION_WELLS_SOURCE_ID,
  DATABC_OBSERVATION_WELLS_SOURCE,
  DATABC_WATER_LICENCES_SOURCE,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  searchedWellsLayer,
  SEARCHED_WELLS_SOURCE_ID,
  FOCUSED_WELLS_SOURCE_ID,
  focusedWellsLayer
} from '../../common/mapbox/layers'
import { LegendControl, BoxZoomControl, SearchOnMoveControl, ClearSearchCriteriaControl } from '../../common/mapbox/controls'
import { setupMapPopups, WELL_FEATURE_PROPERTIES_FOR_POPUP } from '../popup'
import { DEFAULT_MAP_ZOOM, CENTRE_LNG_LAT_BC, buildWellsGeoJSON, convertLngLatBoundsToDirectionBounds, boundsCompletelyContains } from '../../common/mapbox/geometry'

import { RESET_WELLS_SEARCH, SEARCH_WELLS } from '../../wells/store/actions.types'

import wellsAllLegendSrc from '../../common/assets/images/wells-all.svg'
import wellsAllSearchResultLegendSrc from '../../common/assets/images/wells-search-result.svg'
import wellsArtesianLegendSrc from '../../common/assets/images/wells-artesian.svg'
import wellsArtesianSearchResultLegendSrc from '../../common/assets/images/wells-artesian-search-result.svg'
import { mapGetters } from 'vuex'

export default {
  name: 'SearchMap',
  props: [
    'initialZoom',
    'initialCentre',
    'selectedId',
    'searchText',
    'viewBounds',
    'focusWell',
    'selectedWells'
  ],
  data () {
    return {
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
            }
          ]
        },
        {
          show: true,
          id: 'wells-searched',
          label: 'Search Results',
          legend: [
            {
              imageSrc: wellsAllSearchResultLegendSrc,
              label: 'all'
            },
            {
              imageSrc: wellsArtesianSearchResultLegendSrc,
              label: 'artesian'
            }
          ]
        }
      ],
      searchOnMapMove: true,
      movedSinceLastSearch: false,

      pendingLocationSearch: null,
      searchInProgress: false
    }
  },
  mounted () {
    this.updateVisibilityOfSearchResultsLayer()

    this.initMapBox()

    // When the search is reset - fly the map back to view all of BC
    this.$store.subscribeAction((action, state) => {
      if (action.type === SEARCH_WELLS) {
        this.loadWells()
      } else if (action.type === RESET_WELLS_SEARCH) {
        this.resetMap()
      }
    })
  },
  destroyed () {
    this.map.remove()
  },
  computed: {
    ...mapGetters(['searchQueryParams']),
    hasSearchParams (state) {
      return Object.keys(this.searchQueryParams).length > 0
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

      new GestureHandling().addTo(this.map)

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
        setupMapPopups(this.map, this.$router)

        this.setFocusedWells(this.selectedWells)

        if (this.hasSearchParams) { // must be an existing search so load wells in view
          this.loadWells()
        }

        this.$emit('mapLoaded', this.map.getBounds())
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
          [DATABC_OBSERVATION_WELLS_SOURCE_ID]: DATABC_OBSERVATION_WELLS_SOURCE,
          [WELLS_SOURCE_ID]: vectorSourceConfig(WELLS_SOURCE_ID),
          [SEARCHED_WELLS_SOURCE_ID]: { type: 'geojson', data: buildWellsGeoJSON([]) },
          [FOCUSED_WELLS_SOURCE_ID]: { type: 'geojson', data: buildWellsGeoJSON([]) }
        },
        layers: [
          DATABC_ROADS_LAYER,
          DATABC_CADASTREL_LAYER,
          DATABC_ECOCAT_LAYER,
          DATABC_WATER_LICENCES_LAYER,
          DATABC_OBSERVATION_WELLS_LAYER,
          wellsBaseAndArtesianLayer(),
          searchedWellsLayer(),
          focusedWellsLayer()
        ]
      }
    },
    resetMap () {
      this.flyToBC()
      this.clearWellSearchResultsLayer()
      this.setFocusedWells([])
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
        vm.$emit('search', vm.map.getBounds(), { showLoadingSpinner: false })
        vm.loadWells()
      }
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
      this.clearWellSearchResultsLayer()
      this.clearSearchCriteriaControl.toggleShow(false)
      this.$emit('clearSearch')
    },
    boundsOfSelectedWells () {
      const bounds = new mapboxgl.LngLatBounds()
      this.selectedWells.forEach((well) => {
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

            this.clearWellSearchResultsLayer()
          }
        )
    },
    updateWellSearchResultsLayer (geoJSON) {
      this.map.getSource(SEARCHED_WELLS_SOURCE_ID).setData(geoJSON)
    },
    clearWellSearchResultsLayer () {
      this.updateWellSearchResultsLayer(buildWellsGeoJSON([]))
    },
    setFocusedWells (wells) {
      this.map.getSource(FOCUSED_WELLS_SOURCE_ID).setData(buildWellsGeoJSON(wells, WELL_FEATURE_PROPERTIES_FOR_POPUP))
    },
    flyToBC () {
      this.map.flyTo({ center: CENTRE_LNG_LAT_BC, zoom: DEFAULT_MAP_ZOOM })
    },
    flyToBounds (bounds) {
      this.map.fitBounds(bounds, { duration: 1 * 1000, padding: 60 })
    },
    updateVisibilityOfSearchResultsLayer () {
      const searchResultsLayer = this.mapLayers.find((layer) => layer.id === 'wells-searched')
      searchResultsLayer.show = this.hasSearchParams
    }
  },
  watch: {
    focusWell (well) {
      if (well) {
        const { longitude, latitude } = well
        this.map.flyTo({ center: [longitude, latitude], zoom: 10 })
      }
    },
    selectedWells (wells) {
      this.setFocusedWells(wells)

      if (wells.length > 0) {
        if (wells.length === 1) {
          const { longitude, latitude } = wells[0]
          const wellLngLat = [longitude, latitude]
          if (!this.map.getBounds().contains(wellLngLat)) { // if not in view
            this.map.flyTo({ center: wellLngLat, zoom: 10 })
          }
        } else {
          const selectedWellsBounds = this.boundsOfSelectedWells()

          if (!boundsCompletelyContains(this.map.getBounds(), selectedWellsBounds)) {
            // We can't see all selected wells then fly them into view
            this.flyToBounds(this.boundsOfSelectedWells())
          }
        }
      }
    },
    searchInProgress (isLoading) {
      this.searchOnMoveControl.loading(isLoading)
    },
    hasSearchParams (hasSearchParams) {
      this.updateVisibilityOfSearchResultsLayer()
      this.legendControl.update()
      this.searchOnMoveControl.toggleShow(hasSearchParams)
      this.clearSearchCriteriaControl.toggleShow(hasSearchParams)
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";
@import "~@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";

#wells-search-map {
  height: 600px;

  @import "@/common/mapbox.scss";
}
</style>
