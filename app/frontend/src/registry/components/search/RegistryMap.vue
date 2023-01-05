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
  <div id="registries-search-map" class="map"/>  
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
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER,
  SEARCHED_REGISTRIES_SOURCE_ID,
  SEARCHED_REGISTRIES_LAYER_ID,
  searchedRegistriesLayer,
} from '../../../common/mapbox/layers'
import { LegendControl, BoxZoomControl, SearchOnMoveControl, ClearSearchCriteriaControl } from '../../../common/mapbox/controls'
import { DEFAULT_MAP_ZOOM, CENTRE_LNG_LAT_BC, peopleToGeoJSON, convertLngLatBoundsToDirectionBounds, boundsCompletelyContains } from '../../../common/mapbox/geometry'
import { REQUEST_MAP_POSITION } from '../../store/actions.types'
import { mapGetters, mapActions } from 'vuex'
import { setupFeatureTooltips } from '../../../common/mapbox/popup'
import { createRegistrySearchResultPopupElement } from '../../popup'

export default {
  name: 'RegistryMap',
  props: [
    'initialZoom',
    'initialCentre'
  ],
  data () {
    return {
      map: null,
      browserUnsupported: false,
      legendLayers: [],
      searchOnMapMove: true,
      movedSinceLastSearch: false,
      pendingLocationSearch: null,
      searchInProgress: false,
      hasMapBeenReset: false,
      bboxZoomControl: null
    }
  },
  mounted () {
    this.initMapBox()
  },
  destroyed () {
    this.map.remove()
    this.map = null
  },
  computed: {
    ...mapGetters(['userRoles', 'searchQueryParams']),
    ...mapGetters('registriesStore', [
      'requestedMapPosition',
      'searchResponse'
    ]),
    hasSearchParams(state) {
      return Object.keys(this.searchQueryParams).length > 0
    },
    showUnpublished () {
      return Boolean(this.userRoles.wells.edit)
    },
  },
  methods: {
    initMapBox() {
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
      this.bboxZoomControl = new BoxZoomControl({
        onZoom: this.zoomToBBox,
        suppressClickEvent: true
      });
      this.map.addControl(this.bboxZoomControl, 'top-left')
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

      /*
      this.searchOnMoveControl = new SearchOnMoveControl({
        show: this.hasSearchParams,
        searchOnMapMove: this.searchOnMapMove,
        onSearchThisArea: () => this.triggerSearchMapArea(),
        onSearchAsIMove: (e) => (this.searchOnMapMove = e.checked)
      })
      this.map.addControl(this.searchOnMoveControl, 'top-right')
      */

      /*
      this.clearSearchCriteriaControl = new ClearSearchCriteriaControl({
        show: this.hasSearchParams,
        onClearClick: this.clearSearch
      })
      this.map.addControl(this.clearSearchCriteriaControl, 'bottom-right')
      */

      if (this.legendLayers.length) {
        this.legendControl = new LegendControl({
          layers: this.legendLayers
        })
        this.map.addControl(this.legendControl, 'bottom-right')
      }      

      this.map.on("click", this.onMapClick)

      this.map.on('load', () => {

        const tooltipLayers = {
          [SEARCHED_REGISTRIES_LAYER_ID]: {
            snapToCenter: false,
            showOnHover: false,
            createTooltipContent: this.createRegistrySearchResultPopupElement
          },
        }

        setupFeatureTooltips(this.map, tooltipLayers)

        const mapBounds = this.map.getBounds()

        this.$emit('mapLoaded', mapBounds)

      })
    },
    buildMapStyle() {
      return {
        version: 8,
        sources: {
          [DATABC_ROADS_SOURCE_ID]: DATABC_ROADS_SOURCE,
          [DATABC_CADASTREL_SOURCE_ID]: DATABC_CADASTREL_SOURCE,
          [SEARCHED_REGISTRIES_SOURCE_ID]: { type: 'geojson', data: peopleToGeoJSON([]) }
        },
        layers: [
          DATABC_ROADS_LAYER,
          DATABC_CADASTREL_LAYER,
          searchedRegistriesLayer(),
        ]
      }
    },
    resetMap() {
      this.map.fire('reset')
      this.flyToBC()
      this.hasMapBeenReset = true
    },
    zoomToBBox(bbox) {
      if (bbox) {
        this.map.fitBounds(bbox)
      }
    },
    onMapClick(e) {
      // Zoom to the clicked point.  
      // This is currently disabled because it is less convinent than first hoped,
      // and actually harms the usre experience.
      //if (e.hasOwnProperty("lngLat")) {
      //  const clickedLngLat = e.lngLat;
      //  const zoom = 9;
      //  this.REQUEST_MAP_POSITION({ centre: clickedLngLat, zoom: zoom })
      //}
    },
    triggerSearchMapArea() {
      this.$emit('search', this.map.getBounds(), { showLoadingSpinner: true })
      this.searchOnMoveControl.showSearchAreaButton(false)
    },
    clearSearch() {
      this.clearSearchResultsLayer()
      this.clearSearchCriteriaControl.toggleShow(false)
      this.$emit('clearSearch')
    },

    updateSearchResultsLayer(geoJSON) {
      if (this.map) { 
        this.map.getSource(SEARCHED_REGISTRIES_SOURCE_ID).setData(geoJSON)
      }
    },
    clearSearchResultsLayer() {
      this.updateSearchResultsLayer(peopleToGeoJSON([]))
    },
    flyToBC() {
      this.map.flyTo({ center: CENTRE_LNG_LAT_BC, zoom: DEFAULT_MAP_ZOOM })
    },
    flyToBounds(bounds, options = {}) {
      const defaultOptions = {
        duration: 1000,
        padding: 60
      }
      options = Object.assign({}, defaultOptions, options);
      this.map.fitBounds(bounds, options)
    },
    flyToPoint(centre, zoom) {
      this.map.flyTo({ center: centre, zoom: zoom, duration: 200 })
    },
    clearPopups() {
      //remove all map popups
      const popups = document.getElementsByClassName('mapboxgl-popup');
      if (popups) { 
        for (var i = 0; i < popups.length; i++) {
          popups[i].remove()
        }    
      }
    },
    createRegistrySearchResultPopupElement(features, { canInteract }) {
      return createRegistrySearchResultPopupElement(features, this.map, this.$router, {
        pageSize: 1,
        canInteract,
        wellLayerIds: [
          SEARCHED_REGISTRIES_LAYER_ID,
        ]
      })
    },
    ...mapActions('registriesStore', [
      REQUEST_MAP_POSITION
    ]),
  },
  watch: {
    requestedMapPosition (requestedMapPosition) {
      if (requestedMapPosition) {

        this.clearPopups();

        //requestedMapPosition may specify either {center:..., zoom:...} or {bounds:..., maxZoom: ...}.  
        if (requestedMapPosition.hasOwnProperty("centre") && requestedMapPosition.hasOwnProperty("zoom")) {
          this.flyToPoint(requestedMapPosition.centre, requestedMapPosition.zoom);
        }
        else if (requestedMapPosition.hasOwnProperty("bounds")) {
          const maxZoom = requestedMapPosition.hasOwnProperty("maxZoom") ? requestedMapPosition.maxZoom : null;
          this.flyToBounds(requestedMapPosition.bounds, {maxZoom: maxZoom});
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
    searchResponse(searchResponse) {
      const results = searchResponse && searchResponse.results ?
        searchResponse.results :
        [];
      this.updateSearchResultsLayer(peopleToGeoJSON(searchResponse.results))
    },
    userRoles () {
      this.map.setStyle(this.buildMapStyle())
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";

.mapboxgl-popup {
  min-width: 275px !important;
}
#registries-search-map {
  height: 600px;
}
.mapboxgl-canvas-container {
  cursor: pointer !important;
}
</style>
