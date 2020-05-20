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
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'

import {
  DATABC_ROADS_SOURCE,
  DATABC_CADASTREL_SOURCE,
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER
} from '../../common/mapbox/layers'
import { buildLeafletStyleMarker } from '../../common/mapbox/images'

export default {
  name: 'SingleWellMap',
  props: {
    latitude: {
      type: Number
    },
    longitude: {
      type: Number
    }
  },
  data () {
    return {
      map: null,
      browserUnsupported: false
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
  methods: {
    initMapBox () {
      if (!mapboxgl.supported()) {
        this.browserUnsupported = true
        return
      }

      var mapConfig = {
        container: this.$el,
        zoom: 6,
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
        if (this.longitude && this.latitude) {
          buildLeafletStyleMarker(this.longitude, this.latitude).addTo(this.map)

          this.map.setZoom(12)
        }

        this.$emit('mapLoaded')
      })
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";

#single-well-map {
  height: 500px;
}
</style>
