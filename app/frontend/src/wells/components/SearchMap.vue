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
  <div class="search-map">
    <l-map
      ref="map"
      id="map"
      :min-zoom="4"
      :max-zoom="17"
      :zoom="zoom"
      :center="center"
      :options="{ preferCanvas: true }"
      @update:zoom="zoomUpdated"
      @update:bounds="boundsUpdated"
      @update:center="centerUpdated"
      @locationfound="userLocationFound($event)">
      <l-control position="topleft" >
        <div class="geolocate" @click="$refs.map.mapObject.locate()" />
      </l-control>
      <l-control position="topright" >
        <div class="search-as-i-move-control form-inline p-2">
          <div v-if="pendingSearch">
            <div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>
            <strong class="pl-1">Loading...</strong>
          </div>
          <div v-else-if="showSearchThisAreaButton">
            <b-button
              id="search-this-area-btn"
              variant="light"
              size="sm"
              @click="triggerSearch">
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
        </div>
      </l-control>
      <l-control-scale position="bottomleft" metric />
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
          :radius="4"
          :weight="1"
          :fill-opacity="1.0"
          color="#000"
          fill-color="#0162fe">
          <l-popup>
            <div>
              Well Tag Number: <router-link :to="{ name: 'wells-detail', params: {id: marker.wellTagNumber} }">{{ marker.wellTagNumber }}</router-link>
            </div>
            <div>
              Identification Plate Number: {{ marker.idPlateNumber }}
            </div>
          </l-popup>
        </l-circle-marker>
      </l-feature-group>
    </l-map>
  </div>
</template>

<script>
import debounce from 'lodash.debounce'

import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'
import { LMap, LTileLayer, LCircleMarker, LPopup, LControl, LControlScale, LWMSTileLayer, LFeatureGroup } from 'vue2-leaflet'
import { mapGetters } from 'vuex'
import { SEARCH_WELLS, SEARCH_WELL_LOCATIONS } from '@/wells/store/actions.types.js'
import { SET_SEARCH_BOUNDS } from '@/wells/store/mutations.types.js'

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
    'l-map': LMap,
    'l-control': LControl,
    'l-control-scale': LControlScale,
    'l-tile-layer': LTileLayer,
    'l-feature-group': LFeatureGroup,
    'l-wms-tile-layer': LWMSTileLayer,
    'l-circle-marker': LCircleMarker,
    'l-popup': LPopup
  },
  props: {},
  data () {
    return {
      zoom: 5,
      center: [54.5, -126.5],
      bounds: null,
      // Track if we triggered a search, or if it came from another component
      searchTriggered: false,
      searchOnMapMove: false,
      movedSinceLastSearch: false,
      esriLayer: null
    }
  },
  computed: {
    ...mapGetters({
      locations: 'locationSearchResults',
      pendingSearch: 'locationPendingSearch'
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
        return {
          wellTagNumber: location.well_tag_number,
          latLng: L.latLng(location.latitude, location.longitude),
          idPlateNumber: location.identification_plate_number || ''
        }
      })
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
    zoomToMarkers () {
      this.$nextTick(() => {
        if (this.$refs.wellMarkers && this.$refs.wellMarkers.getBounds) {
          const markerBounds = this.$refs.wellMarkers.getBounds().pad(0.5)
          this.$refs.map.mapObject.fitBounds(markerBounds)
        }
      })
    },
    zoomUpdated (zoom) {
      this.zoom = zoom
      this.mapMoved()
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
    triggerSearch: debounce(function () {
      this.searchTriggered = true

      this.$store.dispatch(SEARCH_WELLS, { bounded: true })
      this.$store.dispatch(SEARCH_WELL_LOCATIONS, { bounded: true })
    }, 500),
    mapMoved () {
      if (this.searchOnMapMove) {
        this.triggerSearch()
      } else {
        this.movedSinceLastSearch = true
      }
    },
    userLocationFound (location) {
      this.center = location.latlng
    }
  },
  watch: {
    locations (locations) {
      if (!this.searchTriggered) {
        this.zoomToMarkers()
      }
      this.searchTriggered = false
      this.movedSinceLastSearch = false
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.esriLayer = tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'})
      this.$refs.map.mapObject.addLayer(this.esriLayer)
      // Should be behind the WMS layer
      this.esriLayer.bringToBack()

      // Set max bounds dynamically
      const initialBounds = this.$refs.map.mapObject.getBounds()
      this.$refs.map.mapObject.setMaxBounds(initialBounds)
    })
  },
  beforeDestroy () {
    this.$refs.map.mapObject.removeLayer(this.esriLayer)
  }
}
</script>
<style lang="scss">
@import "leaflet/dist/leaflet.css";

.search-map {
  height: 600px;
}
.geolocate {
    background-image: url('../../common/assets/images/geolocate.png');
    width: 30px;
    height: 30px;
    left: 2px;
    box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
    cursor: pointer;
}

.geolocate:hover {
    opacity: 0.8;
}

.search-as-i-move-control {
  background-clip: padding-box;
  background-color: #fff;
  border: 2px solid rgba(0,0,0,0.2);
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
</style>
