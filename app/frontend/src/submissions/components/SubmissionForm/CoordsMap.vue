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
      type: Number
    },
    longitude: {
      type: Number
    }
  },
  data () {
    return {
      map: null
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
      // Create map, with default centered and zoomed to show entire BC.
      this.map = L.map('map').setView([this.latitude ? this.latitude : 54.5, this.longitude ? this.longitude : -126.5], 5)

      // Add map layers.
      tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'}).addTo(this.map)
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
        styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined',
        transparent: true
      }).addTo(this.map)
    },
    createMarker () {
      if (this.latitude !== null && this.longitude !== null) {
        this.marker = L.marker([this.latitude, this.longitude], {draggable: true, autoPan: true})
        this.marker.on('dragend', (ev) => {
          this.handleDrag(ev)
        })
        this.marker.addTo(this.map)
        this.setMarkerPopup()
      }
    },
    updateMarkerLatLong (latlng) {
      if (this.marker) {
        this.setMarkerPopup(latlng.lat, latlng.lng)
        this.marker.setLatLng(latlng)
      }
    },
    setMarkerPopup (latitude, longitude) {
      this.marker.bindPopup('Latitude: ' + latitude + ', Longitude: ' + longitude)
    },
    updateCoords () {
      if (!isNaN(this.latitude) && !isNaN(this.longitude)) {
        const latlng = L.latLng(this.latitude, this.longitude)
        if (this.insideBC(latlng)) {
          if (this.marker) {
            this.updateMarkerLatLong(latlng)
          } else {
            this.createMarker()
          }
          this.map.panTo(latlng)
        } else {
          if (this.marker) {
            this.map.removeLayer(this.marker)
            this.marker = null
          }
        }
      }
    },
    handleDrag (ev) {
      if (this.insideBC(this.marker.getLatLng())) {
        this.$emit('coordinate', this.marker.getLatLng())
      } else {
        // We don't allow dragging the marker outside of BC, put it back.
        const latlng = L.latLng(this.latitude, this.longitude)
        this.updateMarkerLatLong(latlng)
      }
    },
    insideBC (latLng) {
      // could check this against databc by reverse geocoding change checking that the point is in BC
      // - https://geocoder.api.gov.bc.ca/addresses.json?locationDescriptor=any&parcelPoint=55%2C-124
      // Using a very simple, rough bounding box
      return !!latLng && latLng.lat < 60 && latLng.lat > 48.2 && latLng.lng > -139.07 && latLng.lng < -114
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

</style>
