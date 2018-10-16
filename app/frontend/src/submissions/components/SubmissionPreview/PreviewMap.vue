<template>
  <div style="height: 32rem">
    <l-map
      :zoom="zoom"
      :center="point"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      ></l-tile-layer>

      <l-marker
        :lat-lng="point"
      ></l-marker>

    </l-map>

  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet'
import L from 'leaflet'

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
      default: '-123'
    }
  },
  data () {
    return {

      zoom: 13,
      url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 13,
      showParagraph: false,
      defaultCentre: [49, -123]
    }
  },
  computed: {
    point () {
      if (!this.latitude || !this.longitude || Number.isNaN(this.latitude) || Number.isNaN(this.longitude)) {
        return L.latLng(this.defaultCentre[0], this.defaultCentre[1])
      }
      return L.latLng(Number(this.latitude), Number(this.longitude))
    }
  }
}
</script>

<style>
</style>
