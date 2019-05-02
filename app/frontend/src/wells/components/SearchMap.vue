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
  <div class="search-map" :class="{ 'zoom-box-crosshair': zoomBoxActive }">
    <l-map
      ref="map"
      id="map"
      :min-zoom="minZoom"
      :max-zoom="maxZoom"
      :max-bounds="maxBounds"
      :zoom="zoom"
      :center="center"
      :options="{ attributionControl: false, preferCanvas: true }"
      @update:zoom="zoomUpdated"
      @update:bounds="boundsUpdated"
      @update:center="centerUpdated"
      @locationfound="userLocationFound($event)"
      @boxzoomend="deactivateZoomBox()">
      <l-control position="topleft" class="leaflet-control leaflet-bar zoom-box-control">
        <a
          class="zoom-box-icon"
          :class="{ active: zoomBoxActive, 'leaflet-disabled': atMaxZoom }"
          title="Zoom to specific area"
          aria-label="Zoom to specific area"
          role="button"
          href="#"
          @click.stop.prevent="toggleZoomBox()" />
      </l-control>
      <l-control position="topleft" class="leaflet-control leaflet-bar">
        <a
          class="geolocate-icon"
          title="Zoom to your location"
          aria-label="Zoom to your location"
          role="button"
          href="#"
          @click.stop.prevent="geolocate()" />
      </l-control>
      <l-control position="topright" class="leaflet-control leaflet-bar search-as-i-move-control form-inline p-2">
        <div v-if="pendingSearch">
          <div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>
          <strong class="pl-1">Loading...</strong>
        </div>
        <div v-else-if="showSearchThisAreaButton">
          <b-button
            id="search-this-area-btn"
            variant="light"
            size="sm"
            @click.stop="triggerSearch">
            Search this area <span class="pl-1 fa fa-refresh" />
          </b-button>
        </div>
        <div class="ml-1" v-else>
          <b-form-checkbox
            id="search-as-i-move-checkbox"
            :checked="searchOnMapMove"
            @input="searchOnMapMove = $event"
            @click.stop="null">
            Search as I move the map
          </b-form-checkbox>
        </div>
      </l-control>
      <l-control-scale position="bottomleft" metric />
      <l-control position="bottomright">
        <div class="active-search-info d-inline-flex flex-wrap justify-content-end ml-5" v-if="activeSearch">
          <div class="active-search-text py-1 px-3 mb-1">
            <strong>Wells that match active search criteria are displayed.</strong>
          </div>
          <b-button
            class="ml-md-1 mb-1"
            variant="primary"
            size="sm"
            @click.stop="clearSearch()">
            Clear search criteria
          </b-button>
        </div>
      </l-control>
      <!-- esri layer is added on mount -->
      <l-wms-tile-layer
        base-url="https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?"
        format="image/png"
        layers="pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW"
        styles="PMBC_Parcel_Fabric_Cadastre_Outlined"
        :transparent="true"
        :visible="true"
        :z-index="2" />
      <l-feature-group ref="wellMarkers">
        <l-circle-marker
          v-for="marker in markers"
          :key="marker.wellTagNumber"
          :lat-lng="marker.latLng"
          :visible="true"
          :draggable="false"
          :radius="6"
          :weight="1"
          :fill-opacity="1.0"
          color="#000"
          fill-color="#0162fe"
          @click="openPopup(marker)">
        </l-circle-marker>
        <l-popup>
          <div>
            Well Tag Number: <router-link v-if="selectedMarker" :to="{ name: 'wells-detail', params: {id: selectedMarker.wellTagNumber} }">{{ selectedMarker.wellTagNumber }}</router-link>
          </div>
          <div>
            Identification Plate Number: <span v-if="selectedMarker">{{ selectedMarker.idPlateNumber }}</span>
          </div>
          <div>
            Address: <span v-if="selectedMarker">{{ selectedMarker.address }}</span>
          </div>
        </l-popup>
      </l-feature-group>
    </l-map>
    <div class="attribution">
      <a href="http://leafletjs.com" title="A JS library for interactive maps">Leaflet</a> | Powered by <a href="https://www.esri.com">Esri</a>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash.debounce'

import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'
import {
  LCircleMarker,
  LControl,
  LControlScale,
  LFeatureGroup,
  LMap,
  LPopup,
  LTileLayer,
  LWMSTileLayer
} from 'vue2-leaflet'
import { mapGetters } from 'vuex'
import { SEARCH_LOCATIONS, SEARCH_WELLS } from '@/wells/store/actions.types.js'
import {
  SET_SEARCH_BOUNDS,
  SET_SEARCH_PARAMS,
  SET_SEARCH_RESULT_FILTERS
} from '@/wells/store/mutations.types.js'
import { MAP_TRIGGER } from '@/wells/store/triggers.types.js'

// There is a known issue using leaflet with webpack, this is a workaround
// Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

export default {
  name: 'SearchMap',
  components: {
    'l-circle-marker': LCircleMarker,
    'l-control': LControl,
    'l-control-scale': LControlScale,
    'l-feature-group': LFeatureGroup,
    'l-map': LMap,
    'l-popup': LPopup,
    'l-tile-layer': LTileLayer,
    'l-wms-tile-layer': LWMSTileLayer
  },
  props: {},
  data () {
    return {
      zoom: 5,
      center: [54.5, -126.5],
      maxBounds: [
        [46.07323062540835, -140.27343750000003],
        [61.438767493682825, -112.71972656250001]
      ],
      maxZoom: 17,
      minZoom: 4,
      bounds: null,
      selectedMarker: null,

      searchOnMapMove: true,
      movedSinceLastSearch: false,
      zoomBoxActive: false,
      zoomToMarkersActive: false,
      esriLayer: null
    }
  },
  computed: {
    ...mapGetters({
      lastSearchTrigger: 'lastSearchTrigger',
      locations: 'locationSearchResults',
      pendingSearch: 'pendingLocationSearch',
      searchParams: 'searchParams',
      searchResultFilters: 'searchResultFilters'
    }),
    searchBoundBox () {
      const sw = this.bounds.getSouthWest()
      const ne = this.bounds.getNorthEast()
      return {
        sw_lat: sw.lat,
        sw_long: sw.lng,
        ne_lat: ne.lat,
        ne_long: ne.lng
      }
    },
    markers () {
      return this.locations.filter(location => location.latitude !== null && location.longitude !== null).map(location => {
        let address = location.street_address
        if (location.city !== undefined && location.city !== null && location.city.toString().trim() !== '') {
          address = `${address}, ${location.city}`
        }

        return {
          wellTagNumber: location.well_tag_number,
          latLng: L.latLng(location.latitude, location.longitude),
          idPlateNumber: location.identification_plate_number || '',
          address: address
        }
      })
    },
    atMaxZoom () {
      return this.zoom === this.maxZoom
    },
    activeSearch () {
      return (
        Object.entries(this.searchParams).length > 0 ||
        Object.entries(this.searchResultFilters).length > 0
      )
    },
    showSearchThisAreaButton () {
      return (!this.searchOnMapMove && this.movedSinceLastSearch && this.zoom >= 9)
    }
  },
  methods: {
    resetView () {
      this.center = [54.5, -126.5]
      this.zoom = 5
    },
    openPopup (marker) {
      this.selectedMarker = marker
      this.$refs.wellMarkers.mapObject.openPopup(marker.latLng)
    },
    zoomToMarkers () {
      this.zoomToMarkersActive = true
      this.$nextTick(() => {
        const markerBounds = this.$refs.wellMarkers.mapObject.getBounds().pad(0.5)
        this.$refs.map.mapObject.fitBounds(markerBounds)
      })
    },
    zoomUpdated (zoom) {
      this.zoom = zoom
    },
    centerUpdated (center) {
      this.center = center
      this.$emit('moved', center)

      this.mapMoved()
    },
    boundsUpdated (bounds) {
      this.bounds = bounds
      this.$store.commit(SET_SEARCH_BOUNDS, this.searchBoundBox)
    },
    mapMoved: debounce(function () {
      if (this.zoomToMarkersActive) {
        this.zoomToMarkersActive = false
        return
      }

      this.movedSinceLastSearch = true
      if (this.searchOnMapMove) {
        this.triggerSearch()
      }
    }, 500),
    triggerSearch () {
      this.$store.dispatch(SEARCH_LOCATIONS)
      this.$store.dispatch(SEARCH_WELLS, { trigger: MAP_TRIGGER, constrain: true })
    },
    clearSearch () {
      this.$store.commit(SET_SEARCH_PARAMS, {})
      this.$store.commit(SET_SEARCH_RESULT_FILTERS, {})

      this.triggerSearch()
    },
    geolocate () {
      this.$refs.map.mapObject.locate()
    },
    userLocationFound (location) {
      this.center = location.latlng
    },
    toggleZoomBox () {
      if (this.atMaxZoom) {
        return
      }

      if (!this.zoomBoxActive) {
        this.activateZoomBox()
      } else {
        this.deactivateZoomBox()
      }
    },
    activateZoomBox () {
      this.zoomBoxActive = true
      this.$refs.map.mapObject.dragging.disable()
      this.$refs.map.mapObject.boxZoom.addHooks()
    },
    deactivateZoomBox () {
      this.$refs.map.mapObject.boxZoom.removeHooks()
      this.$refs.map.mapObject.dragging.enable()
      this.zoomBoxActive = false
    },
    initEsriLayer () {
      this.esriLayer = tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'})
      this.$refs.map.mapObject.addLayer(this.esriLayer)
      // Should be behind the WMS layer
      this.esriLayer.bringToBack()
    },
    removeEsriLayer () {
      this.$refs.map.mapObject.removeLayer(this.esriLayer)
    },
    initZoomBox () {
      // Bind to the map's boxZoom handler
      const mapObject = this.$refs.map.mapObject
      const originalMouseDown = mapObject.boxZoom._onMouseDown
      mapObject.boxZoom._onMouseDown = (event) => {
        // prevent right-click from triggering zoom tool
        if (event.button === 2) {
          return
        }

        const newEvent = {
          clientX: event.clientX,
          clientY: event.clientY,
          which: 1,
          shiftKey: true
        }
        originalMouseDown.call(mapObject.boxZoom, newEvent)
      }
    }
  },
  watch: {
    locations (locations) {
      if (!this.zoomToMarkersActive && this.lastSearchTrigger !== MAP_TRIGGER) {
        this.zoomToMarkers()
      }
      this.movedSinceLastSearch = false
      this.searchOnMapMove = true
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.initEsriLayer()
      this.initZoomBox()
    })
  },
  beforeDestroy () {
    this.removeEsriLayer()
  }
}
</script>
<style lang="scss">
@import "leaflet/dist/leaflet.css";

#map {
  height: 600px;
}
.search-map {

  &.zoom-box-crosshair {
      cursor: crosshair !important;
  }
  .zoom-box-control {
      font-size: 18px;
  }
  .zoom-box-icon {
    background-image: url('../../common/assets/images/select-zoom.png');

    &.active, &:hover {
      opacity: 0.8;
    }
    &.leaflet-disabled{
      opacity: 0.6;
    }
  }

  .geolocate-icon {
    background-image: url('../../common/assets/images/geolocate.png');
    &:hover {
      opacity: 0.8;
    }
  }

  .search-as-i-move-control {
    background-color: #fff;
  }

  .active-search-text {
    color: #000;
    background-color: rgba(0,0,0,0.3);
    border-radius: 4px;
  }

  /* Spinner styles — these can be removed when moving to bootstrap 4.3 */

  $spinner-width:         2rem !default;
  $spinner-height:        $spinner-width !default;
  $spinner-border-width:  .25em !default;

  $spinner-width-sm:        1rem !default;
  $spinner-height-sm:       $spinner-width-sm !default;
  $spinner-border-width-sm: .2em !default;

  @keyframes spinner-border {
    to { transform: rotate(360deg); }
  }

  .spinner-border {
    display: inline-block;
    width: $spinner-width;
    height: $spinner-height;
    vertical-align: text-bottom;
    border: $spinner-border-width solid currentColor;
    border-right-color: transparent;
    // stylelint-disable-next-line property-blacklist
    border-radius: 50%;
    animation: spinner-border .75s linear infinite;
  }

  .spinner-border-sm {
    width: $spinner-width-sm;
    height: $spinner-height-sm;
    border-width: $spinner-border-width-sm;
  }

  //
  // Growing circle
  //

  @keyframes spinner-grow {
    0% {
      transform: scale(0);
    }
    50% {
      opacity: 1;
    }
  }
}
</style>
