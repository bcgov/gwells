<template>
  <div style="height: 32rem">
    <l-map :zoom="zoom" :center="mapCentre">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="marker"></l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet'
import L from 'leaflet'

// necessary steps to load leaflet in Vue/webpack
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

export default {
  name: 'PreviewMap',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  props: {
    latitude: {
      type: null,
      default: '49'
    },
    longitude: {
      type: null,
      default: '-129'
    }
  },
  data () {
    return {

      // Leaflet settings
      zoom: 13,
      url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',

      // mapCentre and marker will be updated as location coordinates are entered.
      // these are the default values if no location is given (todo: location should be required)
      mapCentre: L.latLng(49, -129),
      marker: L.latLng(49, -129),
      currentZoom: 13

    }
  },
  watch: {
    // watch latitude and longitude props and update map marker accordingly.
    // binding the marker directly to the prop (or a computed value) seems to
    // result in unusual behavior, so we update the marker value "one-way" from
    // the prop
    latitude () {
      this.updateMarkerPosition(this.latitude, this.longitude)
    },
    longitude () {
      this.updateMarkerPosition(this.latitude, this.longitude)
    }
  },
  methods: {
    updateMarkerPosition (lat, long) {
      // convert lat/long to numbers, check if NaN, and update the existing
      // marker and map centre to the new coordinates.
      lat = Number(lat)
      long = Number(long)

      if (lat && long && !Number.isNaN(lat) && !Number.isNaN(long)) {
        this.marker = L.latLng(lat, long)
        this.mapCentre = L.latLng(lat, long)
      }
    }
  },
  created () {
    this.updateMarkerPosition(this.latitude, this.longitude)
  }
}
</script>

<style>
</style>
