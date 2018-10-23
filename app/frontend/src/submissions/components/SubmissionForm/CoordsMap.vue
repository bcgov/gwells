<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'
export default {
  name: 'CoordsMap',
  props: {
    latitude: {
      type: Number,
      default: 54.5
    },
    longitude: {
      type: Number,
      default: -126.5
    }
  },
  data () {
    return {
      map: null,
      tileLayer: null,
      layers: []
    }
  },
  mounted () {
    this.initLeaflet()
    this.initMap()
  },
  watch: {
    latitude () {
      this.updateCoords()
    },
    longitude () {
      this.updateCoords()
    }
  },
  methods: {
    initLeaflet () {
      // eslint-disable-next-line
      delete L.Icon.Default.prototype._getIconUrl  
      // eslint-disable-next-line
      L.Icon.Default.mergeOptions({  
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png')
      })
    },
    initMap () {
      console.log(this.latitude)
      this.map = L.map('map').setView([this.latitude ? this.latitude : 54.5, this.longitude ? this.longitude : -126.5], 5)

      tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'}).addTo(this.map)

      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
        styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined',
        transparent: true
      }).addTo(this.map)

      this.marker = L.marker([this.latitude ? this.latitude : 54.5, this.longitude ? this.longitude : -126.5])
      this.marker.addTo(this.map)
      this.marker.bindPopup('Latitude: ' + this.latitude + ', Longitude: ' + this.longitude)
    },
    updateCoords () {
      this.marker.setLatLng(L.latLng(this.latitude, this.longitude))
      this.map.setView([this.latitude ? this.latitude : 54.5, this.longitude ? this.longitude : -126.5], 5)
    }
  }
}
</script>
<style>
@import "leaflet/dist/leaflet.css";

.map {
  width: 550px;
  height: 500px;
}

/*
styles like this would be nice, but can't live in this control

@media (min-width: 575px) {
  .map {
    width: 250px;
    height: 250px;
  }
}

@media (min-width: 767px) {
  .map {
    width: 350px;
    height: 350px;
  }
}

@media (min-width: 991px) {
  .map {
    width: 450px;
    height: 450px;
  }
}

@media (min-width: 1199px) {
  .map {
    width: 550px;
    height: 500px;
  }
} */
</style>
