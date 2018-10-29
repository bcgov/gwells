<template>
  <div>
    <fieldset>
      <legend>Geographic Coordinates</legend>
      <p>To determine coordinates using a Global Positioning System (GPS), set the datum to North America Datum of 1983 (NAD 83), the current ministry standard for mapping.</p>
      <p>After the GPS coordinates are entered, the map pin can be moved by clicking and dragging it on the map. The GPS coordinates will be updated automatically.</p>
      <b-row>
        <b-col sm="12" md="6">
          <b-card no-body class="p-3 m-1 m-md-1">
            <b-row>
              <b-col cols="12" sm="6" lg="3">
                <form-input
                  id="latitude"
                  type="number"
                  :step="0.1"
                  :min="48.2"
                  :max="60"
                  label="Latitude"
                  hint="Decimal degrees"
                  @focus="unfreeze('deg')"
                  @blur="freeze('deg')"
                  v-model.number="latitudeInput"
                  :errors="errors['latitude']"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="6" lg="3" offset-lg="2">
                <form-input
                  id="longitude"
                  type="number"
                  :step="0.1"
                  :min="114"
                  :max="139.07"
                  @focus="unfreeze('deg')"
                  @blur="freeze('deg')"
                  label="Longitude"
                  hint="Decimal degrees"
                  v-model.number="computedLongitude"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
            </b-row>
          </b-card>
          <b-row><b-col><p class="p-3">OR</p></b-col></b-row>
          <b-card no-body class="p-3 mx-1 mx-md-1">
            <b-row>
              <b-col cols="12" md="6" lg="6">
                <b-row class="mb-2"><b-col>Latitude</b-col></b-row>
                <b-row>
                  <b-col cols="12" sm="4" class="px-2">
                    <form-input
                      id="latitudeDeg"
                      @focus="unfreeze('dms')"
                      @blur="freeze('dms')"
                      hint="Degrees"
                      type="number"
                      :step="1"
                      :min="48"
                      :max="60"
                      v-model.number="dms.lat.deg"
                      :loaded="fieldsLoaded['latitude']"
                    ></form-input>
                  </b-col>
                  <b-col cols="12" sm="4" class="px-2">
                    <form-input
                      id="latitudeMin"
                      hint="Minutes"
                      @focus="unfreeze('dms')"
                      @blur="freeze('dms')"
                      type="number"
                      :step="1"
                      :min="0"
                      :max="60"
                      v-model.number="dms.lat.min"
                      :errors="errors['latitude']"
                      :loaded="fieldsLoaded['latitude']"
                    ></form-input>
                  </b-col>
                  <b-col cols="12" sm="4" class="px-1">
                    <form-input
                      id="latitudeSec"
                      type="number"
                      :step="0.1"
                      :min="0"
                      :max="60"
                      @focus="unfreeze('dms')"
                      @blur="freeze('dms')"
                      hint="Seconds"
                      v-model.number="dms.lat.sec"
                      :errors="errors['latitude']"
                      :loaded="fieldsLoaded['latitude']"
                    ></form-input>
                  </b-col>
                </b-row>
              </b-col>
              <b-col cols="12" md="6" lg="6" offset-lg="0">
                <b-row class="mb-2"><b-col>Longitude</b-col></b-row>
                <b-row>
                  <b-col cols="12" sm="4" class="px-2">
                    <form-input
                      id="longitudeDeg"
                      type="number"
                      :step="1"
                      :min="114"
                      :max="139"
                      @focus="unfreeze('dms')"
                      @blur="freeze('dms')"
                      hint="Degrees"
                      v-model.number="computedLongitudeDeg"
                      :errors="errors['longitude']"
                      :loaded="fieldsLoaded['longitude']"
                    ></form-input>
                  </b-col>
                  <b-col cols="12" sm="4" class="px-2">
                    <form-input
                      id="longitudeMin"
                      type="number"
                      :step="1"
                      :min="0"
                      :max="60"
                      @focus="unfreeze('dms')"
                      @blur="freeze('dms')"
                      hint="Minutes"
                      v-model.number="dms.long.min"
                      :errors="errors['longitude']"
                      :loaded="fieldsLoaded['longitude']"
                    ></form-input>
                  </b-col>
                  <b-col cols="12" sm="4" class="px-1">
                    <form-input
                      id="longitudeSec"
                      type="number"
                      :step="0.1"
                      :min="0"
                      :max="60"
                      @focus="unfreeze('dms')"
                      @blur="freeze('dms')"
                      hint="Seconds"
                      v-model.number="dms.long.sec"
                      :errors="errors['longitude']"
                      :loaded="fieldsLoaded['longitude']"
                    ></form-input>
                  </b-col>
                </b-row>
              </b-col>
            </b-row>
          </b-card>
          <b-row><b-col><p class="p-3">OR</p></b-col></b-row>
          <b-card no-body class="p-3 mx-1 mx-md-1">
            <b-row>
              <b-col cols="12" sm="4" lg="4">
                <form-input
                  id="utmZone"
                  select
                  :options="utmZones"
                  label="Zone"
                  @focus="unfreeze('utm')"
                  @blur="freeze('utm')"
                  v-model="utm.zone"
                  text-field="name"
                  value-field="value"
                  :loaded="fieldsLoaded['utmZone']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4" lg="4">
                <!-- UTM Easting should only allow 6 digits to be entered. -->
                <form-input
                  id="utmEasting"
                  type="number"
                  :step="1"
                  label="UTM Easting"
                  v-model.number="utm.easting"
                  @focus="unfreeze('utm')"
                  @blur="freeze('utm')"
                  :loaded="fieldsLoaded['utmEasting']"
                  :max="999999"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4" lg="4">
                <!-- UTM Northing should only allow 7 digits to be entered. -->
                <form-input
                  id="utmNorthing"
                  type="number"
                  :step="1"
                  label="UTM Northing"
                  @focus="unfreeze('utm')"
                  @blur="freeze('utm')"
                  v-model.number="utm.northing"
                  :max="9999999"
                  :loaded="fieldsLoaded['utmNorthing']"
                ></form-input>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
        <b-col sm="12" md="6">
          <coords-map :latitude="latitudeInput" :longitude="longitudeInput" v-on:coordinate="handleMapCoordinate"/>
        </b-col>
      </b-row>

      <!-- Error message when coordinates not entered in at least one of the 3 input groups -->
      <b-alert class="mt-3" variant="danger" :show="errorCoordsNotProvided">
        Must enter geographic coordinates in either decimal degrees, degrees/minutes/seconds, or UTM format.
      </b-alert>
    </fieldset>
  </div>
</template>
<script>
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import CoordsMap from '@/submissions/components/SubmissionForm/CoordsMap.vue'
import { mapGetters } from 'vuex'
import proj4 from 'proj4'
export default {
  components: {
    'coords-map': CoordsMap
  },
  name: 'Coords',
  mixins: [inputBindingsMixin],
  props: {
    latitude: Number,
    longitude: Number,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    errorCoordsNotProvided: Boolean
  },
  data () {
    return {
      ellps: 'GRS80', // UTM config parameters. This does not apply to degrees latitude/longitude
      datum: 'nad83',
      lock: {
        utm: true,
        dms: true,
        deg: true
      },
      utm: {
        easting: null,
        northing: null,
        zone: ''
      },
      degrees: {
        latitude: null,
        longitude: null
      },
      dms: {
        lat: {
          deg: null,
          min: null,
          sec: null
        },
        long: {
          deg: null,
          min: null,
          sec: null
        }
      },
      latitudeDMSValidation: false
    }
  },
  computed: {
    // BC is covered by UTM zones 7 through 11
    utmZones () {
      const zones = [{
        'value': '',
        'name': 'Select zone'
      }]

      for (let i = 1; i <= 60; i++) {
        zones.push({
          'value': i,
          'name': i
        })
      }

      return zones
    },
    // In the background, longitude is stored as a negative number (West == minus). However, our B.C. based
    // users are used to ommitting the negative, because it's implicit. As such we need a workaround to
    // transform the longitude.
    computedLongitude: {
      get: function () {
        return this.transformToPositive(this.longitudeInput)
      },
      set: function (value) {
        this.longitudeInput = this.transformToNegative(value)
      }
    },
    computedLongitudeDeg: {
      get: function () {
        return this.transformToPositive(this.dms.long.deg)
      },
      set: function (value) {
        this.dms.long.deg = this.transformToNegative(value)
      }
    },
    ...mapGetters(['codes'])
  },
  watch: {
    'dms.lat': {
      deep: true,
      handler: function (value) {
        if (!this.lock.dms) {
          if (!value.deg && !value.min && !value.sec) {
          // early return if all fields empty
          // reset other coordinate fields at the same time (e.g. clean up previously calculated valuess)
            this.resetUTM()
            this.resetDegrees()
            return null
          }

          const dms = Object.assign({}, value)
          dms.deg = value.deg
          dms.min = value.min
          dms.sec = value.sec

          const lat = this.convertDMStoDeg(dms)
          const { easting, northing, zone } = this.convertToUTM(this.longitudeInput, lat)
          this.updateDegrees(this.longitudeInput, lat)
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'dms.long': {
      deep: true,
      handler: function (value) {
        if (!this.lock.dms) {
          if (!value.deg && !value.min && !value.sec) {
            this.resetUTM()
            this.resetDegrees()
            return null
          }

          const dms = Object.assign({}, value)
          dms.deg = value.deg
          dms.min = value.min
          dms.sec = this.roundSeconds(value.sec)

          const long = this.convertDMStoDeg(dms)

          const { easting, northing, zone } = this.convertToUTM(long, this.latitudeInput)
          this.updateDegrees(long, this.latitudeInput)
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'latitudeInput': {
      deep: true,
      handler: function (latitude) {
        if (!this.lock.deg && !isNaN(latitude)) {
          if (!latitude) {
            this.resetUTM()
            this.resetDMS()
            return null
          }
          const { easting, northing, zone } = this.convertToUTM(this.longitudeInput, latitude)

          this.updateDMS(this.convertToDMS(this.longitudeInput), this.convertToDMS(latitude))
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'longitudeInput': {
      deep: true,
      handler: function (long) {
        if (!this.lock.deg && !isNaN(long)) {
          if (!long) {
            this.resetUTM()
            this.resetDMS()
            return null
          }

          const { easting, northing, zone } = this.convertToUTM(long, this.latitudeInput)

          this.updateDMS(this.convertToDMS(long), this.convertToDMS(this.latitudeInput))
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'utm.northing': {
      deep: true,
      handler: function (value) {
        if (!this.lock.utm) {
          if (!value) {
            this.resetDMS()
            this.resetDegrees()
            return null
          }

          const { longitude, latitude } = this.convertToWGS84(this.utm.easting, value, this.utm.zone || 0)

          this.updateDegrees(longitude, latitude)
          this.updateDMS(this.convertToDMS(longitude), this.convertToDMS(latitude))
        }
      }
    },
    'utm.easting': {
      deep: true,
      handler: function (value) {
        if (!this.lock.utm) {
          if (!value) {
            this.resetDMS()
            this.resetDegrees()
            return null
          }

          const { longitude, latitude } = this.convertToWGS84(value, this.utm.northing, this.utm.zone || 0)

          this.updateDegrees(longitude, latitude)
          this.updateDMS(this.convertToDMS(longitude), this.convertToDMS(latitude))
        }
      }
    },
    'utm.zone': {
      deep: true,
      handler: function (value) {
        if (!this.lock.utm) {
          if (!value) {
            this.resetDMS()
            this.resetDegrees()
            return null
          }

          const { longitude, latitude } = this.convertToWGS84(this.utm.easting, this.utm.northing, value)

          this.updateDegrees(longitude, latitude)
          this.updateDMS(this.convertToDMS(longitude), this.convertToDMS(latitude))
        }
      }
    }
  },
  methods: {
    transformToPositive (value) {
      // Take a value, if it's a number - make it positive. If it's not a number, leave it alone
      return value === '' || isNaN(value) || value === null ? value : Math.abs(value)
    },
    transformToNegative (value) {
      // Take a value, if it's a number - make it negative. If it's not a number, leave it alone.
      return value === '' || isNaN(value) || value === null ? value : Math.abs(value) * -1
    },
    convertToUTM (long, lat) {
      // converts input coordinates and returns an object containing UTM easting, northing, and zone
      const utm = {
        easting: null,
        northing: null,
        zone: null
      }

      if (!!long && !!lat) {
        if (long > 0) {
          // In B.C. everything is negative by convention, so we have to introduct a minus here to make
          // the math work.
          long *= -1
        }
        // determine zone
        const zone = Math.floor((long + 180) / 6) + 1

        // proj4 coordinate system definitions
        const utmProjection = `+proj=utm +zone=${zone} +ellps=GRS80 +datum=NAD83 +units=m +no_defs`
        const coords = proj4(utmProjection, [long, lat])

        utm.easting = coords[0]
        utm.northing = coords[1]
        utm.zone = zone
      }

      return utm
    },
    convertToWGS84 (easting, northing, zone) {
      // converts from UTM to WGS84

      // proj4 coordinate system definitions
      const wgs84Projection = proj4.defs('EPSG:4326')
      const utmProjection = `+proj=utm +zone=${zone} +ellps=${this.ellps} +datum=${this.datum} +units=m +no_defs`

      const coords = proj4(utmProjection, wgs84Projection, [easting, northing])

      return {
        longitude: coords[0],
        latitude: coords[1]
      }
    },
    convertToDMS (degrees) {
      // converts from decimal degrees to degrees, minutes seconds
      // returns an object with keys 'deg', 'min', 'sec'

      const angle = Math.abs(degrees)
      const deg = Math.floor(angle) * Math.sign(degrees)
      const sec = 3600 * (angle - Math.floor(angle)) % 60
      const min = Math.floor((3600 * (angle - Math.floor(angle))) / 60)

      return {
        deg: deg,
        min: min,
        sec: this.roundSeconds(sec)
      }
    },
    convertDMStoDeg (dms) {
      const sign = Math.sign(dms.deg)
      return this.roundDecimalDegrees(dms.deg + sign * dms.min / 60 + sign * dms.sec / (60 * 60))
    },
    roundDecimalDegrees (deg) {
      // Regulations are specific about how GPS coordinates are to be provided.
      // DD to at least 5 decimal places.
      return Math.round(deg * 100000) / 100000
    },
    roundSeconds (seconds) {
      // Regulations are specific about how GPS coordinates are to be provided.
      // DMS toat least 2 decimal places;
      return Math.round(seconds * 100) / 100
    },
    updateUTM (easting, northing, zone) {
      this.utm.easting = Math.round(easting)
      this.utm.northing = Math.round(northing)
      this.utm.zone = zone
    },
    resetUTM () {
      this.utm = {
        easting: null,
        northing: null,
        zone: null
      }
    },
    updateDMS (longitude = {}, latitude = {}) {
      this.dms.long = longitude
      this.dms.lat = latitude
    },
    resetDMS () {
      this.dms = {
        lat: {
          deg: null,
          min: null,
          sec: null
        },
        long: {
          deg: null,
          min: null,
          sec: null
        }
      }
    },
    updateDegrees (longitude, latitude) {
      this.longitudeInput = this.roundDecimalDegrees(longitude)
      this.latitudeInput = this.roundDecimalDegrees(latitude)
    },
    resetDegrees () {
      this.degrees = {
        latitude: null,
        longitude: null
      }
    },
    freeze (type) {
      // freeze updates the 'lock' object for the given type
      // param 'type' should be one of 'utm', 'deg', 'dms'
      // locking a type will prevent its form input field from being auto-updated
      // while user is providing input.
      this.lock[type] = true
    },
    unfreeze (type) {
      this.lock[type] = false
    },
    handleMapCoordinate (latlng) {
      this.updateDegrees(latlng.lng, latlng.lat)

      const { easting, northing, zone } = this.convertToUTM(latlng.lng, latlng.lat)

      this.updateDMS(this.convertToDMS(latlng.lng), this.convertToDMS(latlng.lat))
      this.updateUTM(easting, northing, zone)
    }
  }
}
</script>

<style>

</style>
