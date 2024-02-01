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
  <div id="single-well-map" class="map">
    <p id="unsupported-browser" v-if="browserUnsupported">Your browser is unable to view the map</p>
  </div>
</template>

<script>
import axios from 'axios'
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'

import {
  DATABC_ROADS_SOURCE,
  DATABC_CADASTREL_SOURCE,
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER
} from '../../../common/mapbox/layers'
import { buildLeafletStyleMarker } from '../../../common/mapbox/images'
import { fetchInsideBCCheck, checkCoordsAreTheSame } from '../../../common/mapbox/geometry'

export default {
  name: 'CoordsMap',
  props: {
    latitude: {
      type: Number
    },
    longitude: {
      type: Number
    },
    draggable: {
      type: Boolean,
      default: true
    },
    insideBC: {
      type: Function,
      default: () => {}
    }
  },
  data () {
    return {
      map: null,
      browserUnsupported: false,
      marker: null,
      insideBCCheckCancelSource: null,
      coordsChangeTimer: null,
      markerOnMap: false
    }
  },
  mounted () {
    this.$emit('mapLoading')

    this.initMapBox()
  },
  destroyed () {
    this.map.remove()
    this.map = null
  },
  computed: {
    insideBCCheckInProgress () {
      return !!this.insideBCCheckCancelSource
    },
    hasCoords () {
      return Boolean(this.longitude) && Boolean(this.latitude)
    }
  },
  methods: {
    initMapBox () {
      if (!mapboxgl.supported()) {
        this.browserUnsupported = true
        return
      }

      var mapConfig = {
        container: this.$el,
        zoom: 4,
        minZoom: 4,
        maxPitch: 0,
        dragRotate: false,
        center: [this.longitude || -126.5, this.latitude || 54.5],
        style: {
          version: 8,
          sources: {
            [DATABC_ROADS_SOURCE_ID]: DATABC_ROADS_SOURCE,
            [DATABC_CADASTREL_SOURCE_ID]: DATABC_CADASTREL_SOURCE
          },
          layers: [
            DATABC_ROADS_LAYER,
            DATABC_CADASTREL_LAYER
          ]
        }
      }

      this.map = new mapboxgl.Map(mapConfig)
      new GestureHandling({ modifierKey: 'ctrl' }).addTo(this.map)

      /* Add controls */

      this.map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-left')
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

      this.map.on('load', () => {
        this.marker = buildLeafletStyleMarker(this.longitude, this.latitude, { draggable: this.draggable })

        if (this.draggable) {
          this.marker.on('dragend', (ev) => {
            this.handleDrag(ev)
          })
        }

        // Allow users to place a marker if one is not already present
        this.map.on('click', (ev) => {
          if(!this.latitude || !this.longitude){
            this.handleMapClick(ev);
          }
        });
        
        if (this.longitude && this.latitude) {
          this.coordsChanged(this.longitude, this.latitude)

          this.marker.addTo(this.map)

          this.map.setZoom(12)
        }

        this.$emit('mapLoaded')
      })
    },
    resetMap () {
      this.markerOnMap = false
      this.marker.remove()
      this.map.flyTo({ center: [-126.5, 54.5], zoom: 5 })
    },
    coordsChanged (longitude, latitude) {
      const markerCoords = this.marker.getLngLat() // get previous coords
      const newCoords = new mapboxgl.LngLat(this.longitude, this.latitude)

      // Check to see if the current marker position is the the same-ish as the where the
      // incoming longitude and latitude arguments. If they are the same-ish then the user must
      // have just dragged the map where they wanted and this `coordsChanged` is being called
      // because the latitude and longitude props has changed based on that drag position. In
      // this case there is no need to fly to the marker.
      const coordsAreSame = checkCoordsAreTheSame(markerCoords, newCoords)
      if (this.markerOnMap && coordsAreSame) {
        // the spinner could have been loading - toggle marker loading off
        this.toggleMarkerLoading(false)
        return
      }

      this.performCheck(longitude, latitude).then((isInsideBC) => {
        if (isInsideBC) {
          this.updateMarkerLatLong([longitude, latitude])
          const flyToOptions = { center: [longitude, latitude] }
          if (!this.markerOnMap) {
            this.markerOnMap = true
            this.marker.addTo(this.map)
            flyToOptions.zoom = 12 // change the zoom level the first time we add the marker
          }
          this.map.flyTo(flyToOptions)
        } else if (this.markerOnMap) {
          this.markerOnMap = false
          this.marker.remove()
        }
      })
    },
    coordPropsChanged () {
      if (this.longitude && this.latitude) {
        clearTimeout(this.coordsChangeTimer)

        this.coordsChangeTimer = setTimeout(() => {
          this.coordsChanged(this.longitude, this.latitude)
        }, 500)
      } else {
        this.resetMap()
      }
    },
    /**
     * @desc Updates the Longitude / Latitude of the map marker when user clicks, if click is within BC
     * @summary Updates map marker to click location
     * @param {Object} event Mapbox event
     */
    handleMapClick(event) {
      const { lat, lng } = event.lngLat
      this.performCheck(lng, lat).then((isInsideBC) => {
        if (isInsideBC) {
          const longLat = { lng: Math.abs(lng), lat }
          this.$emit('coordinate', longLat);
        }
      });
    },
    handleDrag () {
      const markerLngLat = this.marker.getLngLat()
      this.performCheck(markerLngLat.lng, markerLngLat.lat).then((isInsideBC) => {
        if (isInsideBC) {
          // In B.C. that longitude is always negative, so people aren't used to seeing the minus sign - so
          // we're hiding it away from them.
          const lngLat = { lng: Math.abs(markerLngLat.lng), lat: markerLngLat.lat }
          this.$emit('coordinate', lngLat)
        } else {
          // We don't allow dragging the marker outside of BC, put it back.
          this.updateMarkerLatLong([this.longitude, this.latitude])
        }
      })
    },
    updateMarkerLatLong (lngLat) {
      if (this.marker) {
        // this.setMarkerPopup(latlng.lat, latlng.lng)
        this.marker.setLngLat(lngLat)
      }
    },
    performCheck (longitude, latitude) {
      if (this.insideBCCheckCancelSource) {
        this.insideBCCheckCancelSource.cancel()
      }
      this.insideBCCheckCancelSource = axios.CancelToken.source()
      const options = { cancelToken: this.insideBCCheckCancelSource.token }

      longitude = Math.round(longitude * 100000) / 100000
      latitude = Math.round(latitude * 100000) / 100000

      return fetchInsideBCCheck(longitude, latitude, options).finally(() => (this.insideBCCheckCancelSource = null))
    },
    toggleMarkerLoading (isLoading) {
      this.marker.getElement().classList.toggle('loading', isLoading)
    }
  },
  watch: {
    latitude (newLatitude) {
      this.toggleMarkerLoading(true)
      this.coordPropsChanged()
    },
    longitude () {
      this.toggleMarkerLoading(true)
      this.coordPropsChanged()
    },
    insideBCCheckInProgress (fetchInProgress) {
      this.toggleMarkerLoading(fetchInProgress)
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";

#coords-map {
  width: 550px;
  height: 600px;
}
</style>
