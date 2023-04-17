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
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'
import { debounce } from 'lodash'
import {
  DATABC_ROADS_SOURCE,
  DATABC_ROADS_SOURCE_ID,
  DATABC_ROADS_LAYER,
  SEARCHED_REGISTRIES_SOURCE_ID,
  SEARCHED_REGISTRIES_LAYER_ID,
  searchedRegistriesLayer,
  REGISTRY_SOURCE_ID,
  REGISTRY_FILL_LAYER_ID,
  setupRegistryHover,
  registryFillLayer,
  registryLineLayer,
  REGISTRY_SOURCE
} from '../../../common/mapbox/layers'
import { LegendControl, BoxZoomControl } from '../../../common/mapbox/controls'
import { DEFAULT_MAP_ZOOM, CENTRE_LNG_LAT_BC, peopleToGeoJSON } from '../../../common/mapbox/geometry'
import {
  REQUEST_MAP_POSITION,
  SEARCH_AGAIN,
  SEARCH_REGION
} from '../../store/actions.types'
import { SET_CURRENT_MAP_BOUNDS } from '../../store/mutations.types'
import { mapGetters, mapActions, mapMutations } from 'vuex'
import { setupFeatureTooltips } from '../../../common/mapbox/popup'
import {
  createRegistrySearchResultPopupElement,
  createRegistryRegionPopupElement
} from '../../popup'

const CURRENT_REGISTRY_FILL_LAYER_ID = 'cur-registry-fill'
const CURRENT_REGISTRY_LINE_LAYER_ID = 'cur-registry-line'

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
    ...mapGetters(['userRoles']),
    ...mapGetters('registriesStore', [
      'requestedMapPosition',
      'searchResponse',
      'currentMapBounds',
      'doSearchOnBoundsChange',
      'limitSearchToCurrentMapBounds',
      'snapMapToSearchResults'
    ]),
    // hasSearchParams(state) {
    //  return Object.keys(this.searchQueryParams).length > 0
    // },
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

      const mapConfig = {
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
      })
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

      if (this.legendLayers.length) {
        this.legendControl = new LegendControl({
          layers: this.legendLayers
        })
        this.map.addControl(this.legendControl, 'bottom-right')
      }

      this.map.on('click', this.onMapClick)
      this.map.on('load', () => {
        const tooltipLayers = {
          [REGISTRY_FILL_LAYER_ID]: {
            showOnHover: true,
            createTooltipContent: this.createRegistryRegionPopupElement
          },
          [CURRENT_REGISTRY_FILL_LAYER_ID]: {
            showOnHover: true,
            createTooltipContent: this.createRegistryRegionPopupElement
          },
          [SEARCHED_REGISTRIES_LAYER_ID]: {
            snapToCenter: false,
            showOnHover: false,
            createTooltipContent: this.createRegistrySearchResultPopupElement
          }
        }

        /* Setup registry region hover effect */
        setupRegistryHover(this.map, REGISTRY_FILL_LAYER_ID)
        setupRegistryHover(this.map, CURRENT_REGISTRY_FILL_LAYER_ID)

        setupFeatureTooltips(this.map, tooltipLayers)

        const mapBounds = this.map.getBounds()

        this.$emit('mapLoaded', mapBounds)
        this.SET_CURRENT_MAP_BOUNDS(mapBounds)
      })

      // listen to map move/zoom events
      const mapChangedHandler = debounce(
        e => {
          const bounds = this.map.getBounds()
          this.SET_CURRENT_MAP_BOUNDS(bounds)
          if (this.limitSearchToCurrentMapBounds && this.doSearchOnBoundsChange) {
            this.SEARCH_AGAIN()
          }
        },
        200
      );
      ['zoomend', 'moveend', 'resize'].forEach(eventName => {
        this.map.on(eventName, mapChangedHandler)
      })
    },
    buildMapStyle () {
      return {
        version: 8,
        sources: {
          [DATABC_ROADS_SOURCE_ID]: DATABC_ROADS_SOURCE,
          [SEARCHED_REGISTRIES_SOURCE_ID]: { type: 'geojson', data: peopleToGeoJSON([]) },
          [REGISTRY_SOURCE_ID]: REGISTRY_SOURCE
        },
        layers: [
          DATABC_ROADS_LAYER,
          searchedRegistriesLayer(),
          { ...registryFillLayer({ filter: this.allOtherRegistryFilter() }), maxzoom: 8 },
          registryLineLayer({ filter: this.allOtherRegistryFilter() }),
          { ...registryFillLayer({ id: CURRENT_REGISTRY_FILL_LAYER_ID, filter: this.currentRegistryFilter() }), maxzoom: 8 },
          registryLineLayer({ id: CURRENT_REGISTRY_LINE_LAYER_ID, filter: this.currentRegistryFilter() })
        ]
      }
    },
    currentRegistryFilter () {
      return [
        'case',
        ['==', ['get', 'name'], this.name], true,
        false
      ]
    },
    allOtherRegistryFilter () {
      return [
        'case',
        ['!=', ['get', 'name'], this.name], true,
        false
      ]
    },
    resetMap () {
      this.map.fire('reset')
      this.flyToBC()
      this.hasMapBeenReset = true
    },
    zoomToBBox (bbox) {
      if (bbox) {
        this.map.fitBounds(bbox)
      }
    },
    onMapClick (e) {
      const features = this.map.queryRenderedFeatures(e.point, {
        layers: [CURRENT_REGISTRY_FILL_LAYER_ID]
      })
      if (features.length > 0) {
        const clickedPolygon = features[0]
        this.SEARCH_REGION([clickedPolygon.properties.regional_area_guid])
      }
    },
    triggerSearchMapArea () {
      this.$emit('search', this.map.getBounds(), { showLoadingSpinner: true })
      this.searchOnMoveControl.showSearchAreaButton(false)
    },
    clearSearch () {
      this.clearSearchResultsLayer()
      this.clearSearchCriteriaControl.toggleShow(false)
      this.$emit('clearSearch')
    },

    updateSearchResultsLayer (geoJSON) {
      if (this.map) {
        this.map.getSource(SEARCHED_REGISTRIES_SOURCE_ID).setData(geoJSON)
      }
    },
    clearSearchResultsLayer () {
      this.updateSearchResultsLayer(peopleToGeoJSON([]))
    },
    flyToBC () {
      this.map.flyTo({ center: CENTRE_LNG_LAT_BC, zoom: DEFAULT_MAP_ZOOM })
    },
    flyToBounds (bounds, options = {}) {
      const defaultOptions = {
        duration: 1000,
        padding: 60
      }
      options = Object.assign({}, defaultOptions, options)
      this.map.fitBounds(bounds, options)
    },
    flyToPoint (centre, zoom) {
      const existingCentre = this.map.getCenter()
      const existingZoom = this.map.getZoom()
      // don't adjust the map if the requested position is the same as
      // (or within 1 metre of) the existing position (this avoids a
      // cascade of map moved events)
      if (centre.distanceTo(existingCentre) < 1 && zoom === existingZoom) {
        return
      }
      this.map.flyTo({ center: centre, zoom: zoom, duration: 200 })
    },
    clearPopups () {
      // remove all map popups
      const popups = document.getElementsByClassName('mapboxgl-popup')
      if (popups) {
        for (var i = 0; i < popups.length; i++) {
          popups[i].remove()
        }
      }
    },
    geoJsonToBounds (geoJson) {
      if (!geoJson.features.length) {
        return null
      }
      const bounds = new mapboxgl.LngLatBounds()
      geoJson.features.forEach((f) => {
        const g = f.geometry
        bounds.extend(new mapboxgl.LngLat(g.coordinates[0], g.coordinates[1]))
      })
      return bounds
    },
    createRegistrySearchResultPopupElement (features, { canInteract }) {
      return createRegistrySearchResultPopupElement(features, this.map, this.$router, {
        pageSize: 1,
        canInteract,
        registryLayerIds: [
          SEARCHED_REGISTRIES_LAYER_ID
        ]
      })
    },
    createRegistryRegionPopupElement (features, { canInteract }) {
      return createRegistryRegionPopupElement(features, this.map, this.$router, {
        canInteract,
        registryLayerIds: [ REGISTRY_FILL_LAYER_ID ]
      })
    },
    ...mapActions('registriesStore', [
      REQUEST_MAP_POSITION,
      SEARCH_AGAIN,
      SEARCH_REGION
    ]),
    ...mapMutations('registriesStore', [
      SET_CURRENT_MAP_BOUNDS
    ])
  },
  watch: {
    requestedMapPosition (requestedMapPosition) {
      if (requestedMapPosition) {
        this.clearPopups()

        // requestedMapPosition may specify either {center:..., zoom:...} or {bounds:..., maxZoom: ...}.
        if (requestedMapPosition.hasOwnProperty('centre') && requestedMapPosition.hasOwnProperty('zoom')) {
          this.flyToPoint(requestedMapPosition.centre, requestedMapPosition.zoom)
        } else if (requestedMapPosition.hasOwnProperty('bounds')) {
          const maxZoom = requestedMapPosition.hasOwnProperty('maxZoom') ? requestedMapPosition.maxZoom : null
          this.flyToBounds(requestedMapPosition.bounds, { maxZoom: maxZoom })
        }
      }
    },
    searchInProgress (isLoading) {
      this.searchOnMoveControl.loading(isLoading)
    },
    searchResponse (searchResponse) {
      const geoJson = peopleToGeoJSON(searchResponse.results)
      this.updateSearchResultsLayer(geoJson)
      if (this.snapMapToSearchResults) {
        const bounds = this.geoJsonToBounds(geoJson)
        if (bounds) {
          this.flyToBounds(bounds, { maxZoom: 12 })
        }
      }
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
