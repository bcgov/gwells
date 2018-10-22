<template>
  <b-row>
    <b-col>
      <div id="map" class="map">The map will go here</div>
    </b-col>
  </b-row>
</template>

<script>
import L from 'leaflet'
export default {
  name: 'CoordsMap',
  components: {

  },
  data () {
    return {
      map: null,
      tileLayer: null,
      layers: []
    }
  },
  mounted () {
    this.initMap()
    this.initLayers()
  },
  methods: {
    initMap () {
      this.map = L.map('map').setView([51.505, -0.09], 13)

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)

      L.marker([51.5, -0.09]).addTo(this.map)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
        .openPopup()
    },
    initLayers () {
    }
  }
}
</script>
<style>
.map {
  height: 200px;
  width: 300px;
  position: absolute;
  top: 10;
  left: 10;
}
</style>
