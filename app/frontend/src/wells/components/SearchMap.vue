<template>
  <div id="map" class="map"/>
</template>

<script>
import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'
import debounce from 'lodash.debounce'

// Extend control, making a locate
L.Control.Locate = L.Control.extend({
  onAdd: function (map) {
    let container = L.DomUtil.create('div', 'geolocate')
    L.DomEvent.addListener(container, 'click', this.click, this)
    return container
  },
  onRemove: function (map) {

  },
  click: function (ev) {
    // Use callback to handle clicks
    if (this.onClick) {
      this.onClick(ev)
    }
  }
})
L.control.locate = function (opts) {
  return new L.Control.Locate(opts)
}

export default {
  name: 'SearchMap',
  props: {
    latitude: {
      type: Number
    },
    longitude: {
      type: Number
    },
    locations: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      map: null,
      cluster: null,
      markerGroup: null
    }
  },
  created () {
    // There seems to be an issue loading leaflet immediately on mount, we use nextTick to ensure
    // that the view has been rendered at least once before injecting the map.
    this.$nextTick(function () {
      this.initLeaflet()
      this.initMap()
      this.createMarkers()
    })
  },
  watch: {
    locations () {
      this.createMarkers()
    },
    latitude () {
      this.map.setView([this.latitude ? this.latitude : 54.5, this.getLongitude() ? this.getLongitude() : -126.5])
    },
    longitude () {
      this.map.setView([this.latitude ? this.latitude : 54.5, this.getLongitude() ? this.getLongitude() : -126.5])
    }
  },
  methods: {
    initLeaflet () {
      // There is a known issue using leaflet with webpack, this is a workaround
      // Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png')
      })
    },
    initMap () {
      // Create map, with default centered and zoomed to show entire BC.
      this.map = L.map('map', {
        preferCanvas: true
      }).setView([this.latitude ? this.latitude : 54.5, this.getLongitude() ? this.getLongitude() : -126.5], 5)
      L.control.scale().addTo(this.map)
      // Add map layers.
      tiledMapLayer({url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer'}).addTo(this.map)
      L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
        format: 'image/png',
        layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
        styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined',
        transparent: true
      }).addTo(this.map)
      // Add locate control
      const locateButton = L.control.locate({ position: 'topleft' })
      locateButton.onClick = (ev) => {
        this.map.locate()
      }
      locateButton.addTo(this.map)
      this.map.on('locationfound', (ev) => {
        this.$emit('coordinate', ev.latlng)
      })

      const debouncedEmitMoved = debounce(() => {
        this.$emit('moved', true)
      }, 500)

      this.map.on('moveend', debouncedEmitMoved)
      this.map.on('zoomend', debouncedEmitMoved)

      this.map.setMaxZoom(17)
    },
    createMarkers () {
      // clear markers
      if (this.markerGroup) {
        this.map.removeLayer(this.markerGroup)
      }

      // create a new marker group
      this.markerGroup = L.layerGroup()
      this.markerGroup.addTo(this.map)

      // filter locations for coordinates (coordinate either present or not),
      // and then add them to the new marker group
      this.locations.filter((item) => {
        return item[0] && item[1]
      }).map((item) => {
        return L.circleMarker(L.latLng(item[0], item[1]), {
          radius: 4, // The radius of the circleMarker
          color: '#000', // The color of the circleMarker
          weight: 1,
          fillColor: '#0162fe', // The fill color of the circleMarker
          fillOpacity: 1.0 // How transparent the circleMarker's fill is
        }).bindPopup(`
          <div>
            Well Tag Number: <a href="/gwells/well/${item[2]}">${item[2]}</a>
          </div>
          <div>
            Identification Plate Number: ${item[3] || ''}
          </div>
        `)
      }).forEach((marker) => {
        marker.addTo(this.markerGroup)
      })
    },
    setMarkerPopup (latitude, longitude) {
      this.marker.bindPopup('Latitude: ' + latitude + ', Longitude: ' + longitude)
    },
    insideBC (latLng) {
      // could check this against databc by reverse geocoding change checking that the point is in BC
      // - https://geocoder.api.gov.bc.ca/addresses.json?locationDescriptor=any&parcelPoint=55%2C-124
      // Using a very simple, rough bounding box
      return !!latLng && latLng.lat < 60 && latLng.lat > 48.2 && latLng.lng > -139.07 && latLng.lng < -114
    },
    getLongitude () {
      // In B.C. users are used to omitting the minus sign on longitude, it's always negative. So we're
      // very forgiving, and just always make sure longitude is negative.
      return this.longitude > 0 ? this.longitude * -1 : this.longitude
    },
    encodeHTML (input) {

    }
  }
}
</script>
<style>
@import "leaflet/dist/leaflet.css";

.map {
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
</style>
