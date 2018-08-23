<template>
  <div>
    <fieldset>
      <legend>Step 4: Geographic Coordinates</legend>
      <p>To determine coordinates using a Global Positioning System (GPS), set the datum to North America Datum of 1983 (NAD 83), the current ministry standard for mapping.</p>
      <b-card no-body class="p-3 m-1 m-md-1">
        <b-row>
          <b-col cols="12" sm="6" lg="3">
            <form-input
              id="latitude"
              type="text"
              label="Latitude"
              hint="Decimal degrees"
              @focus="unfreeze('deg')"
              @blur="freeze('deg')"
              v-model="degrees.latitude"
              :errors="errors['latitude']"
              :loaded="fieldsLoaded['latitude']"
            ></form-input>
          </b-col>
          <b-col cols="12" sm="6" lg="3" offset-lg="2">
            <form-input
              id="longitude"
              type="text"
              @focus="unfreeze('deg')"
              @blur="freeze('deg')"
              label="Longitude"
              hint="Decimal degrees"
              v-model="degrees.longitude"
              :errors="errors['longitude']"
              :loaded="fieldsLoaded['longitude']"
            ></form-input>
          </b-col>
        </b-row>
      </b-card>
      <b-row><b-col><p class="p-3">OR</p></b-col></b-row>
      <b-card no-body class="p-3 mx-1 mx-md-1">
        <b-row>
          <b-col cols="12" md="6" lg="4">
            <b-row class="mb-2"><b-col>Latitude</b-col></b-row>
            <b-row>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeDeg"
                  @focus="unfreeze('dms')"
                  @blur="freeze('dms')"
                  hint="Degrees"
                  v-model="dms.lat.deg"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeMin"
                  hint="Minutes"
                  @focus="unfreeze('dms')"
                  @blur="freeze('dms')"
                  v-model="dms.lat.min"
                  :errors="errors['latitude']"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeSec"
                  type="text"
                  @focus="unfreeze('dms')"
                  @blur="freeze('dms')"
                  hint="Seconds"
                  v-model="dms.lat.sec"
                  :errors="errors['latitude']"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
            </b-row>
          </b-col>
          <b-col cols="12" md="6" lg="4" offset-lg="1">
            <b-row class="mb-2"><b-col>Longitude</b-col></b-row>
            <b-row>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeDeg"
                  type="text"
                  @focus="unfreeze('dms')"
                  @blur="freeze('dms')"
                  hint="Degrees"
                  v-model="dms.long.deg"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeMin"
                  @focus="unfreeze('dms')"
                  @blur="freeze('dms')"
                  hint="Minutes"
                  v-model="dms.long.min"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeSec"
                  @focus="unfreeze('dms')"
                  @blur="freeze('dms')"
                  hint="Seconds"
                  v-model="dms.long.sec"
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
          <b-col cols="12" sm="4" lg="2">
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
          <b-col cols="12" sm="4" lg="3">
            <form-input
              id="utmEasting"
              type="text"
              label="UTM Easting"
              v-model="utm.easting"
              @focus="unfreeze('utm')"
              @blur="freeze('utm')"
              :loaded="fieldsLoaded['utmEasting']"
            ></form-input>
          </b-col>
          <b-col cols="12" sm="4" lg="3">
            <form-input
              id="utmNorthing"
              type="text"
              label="UTM Northing"
              @focus="unfreeze('utm')"
              @blur="freeze('utm')"
              v-model="utm.northing"
              :loaded="fieldsLoaded['utmNorthing']"
            ></form-input>
          </b-col>
        </b-row>
      </b-card>

      <!-- Error message when coordinates not entered in at least one of the 3 input groups -->
      <b-alert class="mt-3" variant="danger" :show="errorCoordsNotProvided">
        Must enter geographic coordinates in either decimal degrees, degrees/minutes/seconds, or UTM format.
      </b-alert>
    </fieldset>
    <fieldset class="mt-4">
      <legend>Method of Drilling</legend>
      <b-row>
        <b-col cols="12" md="3">
          <form-input
              id="groundElevation"
              label="Ground Elevation"
              type="number"
              hint="Feet above sea level"
              v-model.number="groundElevationInput"
              :errors="errors['ground_elevation']"
              :loaded="fieldsLoaded['ground_elevation']"></form-input>
        </b-col>
        <b-col cols="12" md="3">
          <form-input
              id="groundElevationMethod"
              label="Method for Determining Ground Elevation"
              select
              placeholder="Select method"
              :options="codes.ground_elevation_methods"
              value-field="ground_elevation_method_code"
              text-field="description"
              v-model="groundElevationMethodInput"
              :errors="errors['ground_elevation_method']"
              :loaded="fieldsLoaded['ground_elevation_method']"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="3">
          <form-input
              id="drillingMethod"
              label="Drilling Method *"
              select
              :options="codes.drilling_methods"
              placeholder="Select method"
              value-field="drilling_method_code"
              text-field="description"
              v-model="drillingMethodInput"
              :errors="errors['drilling_method']"
              :loaded="fieldsLoaded['drilling_method']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="3">
          <form-input
              id="otherDrillingMethod"
              label="Specify Other Method of Drilling"
              type="text"
              v-model="otherDrillingMethodInput"
              :errors="errors['other_drilling_method']"
              :loaded="fieldsLoaded['other_drilling_method']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group label="Orientation of Well">
            <b-form-radio-group v-model="wellOrientationInput"
                                stacked
                                name="wellOrientationRadio">
              <b-form-radio value="VERTICAL">Vertical</b-form-radio>
              <b-form-radio value="HORIZONTAL">Horizontal</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
      </b-row>
    </fieldset>
  </div>
</template>
<script>
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import { mapGetters } from 'vuex'
import proj4 from 'proj4'
export default {
  name: 'Step04Coords',
  mixins: [inputBindingsMixin],
  props: {
    latitude: String,
    longitude: String,
    groundElevation: null,
    groundElevationMethod: String,
    drillingMethod: String,
    otherDrillingMethod: String,
    wellOrientation: String,
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
  fields: {
    latitudeInput: 'latitude',
    longitudeInput: 'longitude',
    groundElevationInput: 'groundElevation',
    groundElevationMethodInput: 'groundElevationMethod',
    drillingMethodInput: 'drillingMethod',
    otherDrillingMethodInput: 'otherDrillingMethod',
    wellOrientationInput: 'wellOrientation'
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
        easting: '',
        northing: '',
        zone: ''
      },
      degrees: {
        latitude: '',
        longitude: ''
      },
      dms: {
        lat: {
          deg: '',
          min: '',
          sec: ''
        },
        long: {
          deg: '',
          min: '',
          sec: ''
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
          dms.deg = Number(this.parseCoordValue(value.deg)) || 0
          dms.min = Number(this.parseCoordValue(value.min)) || 0
          dms.sec = Number(this.parseCoordValue(value.sec)) || 0

          const lat = this.convertDMStoDeg(dms)
          const { easting, northing, zone } = this.convertToUTM(Number(this.degrees.longitude), lat)
          this.updateDegrees(this.degrees.longitude, lat)
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
          dms.deg = Number(this.parseCoordValue(value.deg)) || 0
          dms.min = Number(this.parseCoordValue(value.min)) || 0
          dms.sec = Number(this.parseCoordValue(value.sec)) || 0

          const long = this.convertDMStoDeg(dms)

          const { easting, northing, zone } = this.convertToUTM(long, Number(this.degrees.latitude))
          this.updateDegrees(long, this.degrees.latitude)
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'degrees.latitude': {
      deep: true,
      handler: function (value) {
        if (!this.lock.deg) {
          value = this.parseCoordValue(value)
          if (!value) {
            this.resetUTM()
            this.resetDMS()
            return null
          }

          const lat = Number(value)
          const { easting, northing, zone } = this.convertToUTM(Number(this.degrees.longitude), lat)

          this.updateDMS(this.convertToDMS(Number(this.degrees.longitude)), this.convertToDMS(lat))
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'degrees.longitude': {
      deep: true,
      handler: function (value) {
        if (!this.lock.deg) {
          value = this.parseCoordValue(value)
          if (!value) {
            this.resetUTM()
            this.resetDMS()
            return null
          }

          const long = Number(value)
          const { easting, northing, zone } = this.convertToUTM(long, Number(this.degrees.latitude))

          this.updateDMS(this.convertToDMS(long), this.convertToDMS(Number(this.degrees.latitude)))
          this.updateUTM(easting, northing, zone)
        }
      }
    },
    'utm.northing': {
      deep: true,
      handler: function (value) {
        if (!this.lock.utm) {
          value = this.parseCoordValue(value)
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
          value = this.parseCoordValue(value)
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
    convertToUTM (long, lat) {
      // converts input coordinates and returns an object containing UTM easting, northing, and zone
      const utm = {
        easting: '',
        northing: '',
        zone: ''
      }

      lat = Number(lat)
      long = Number(long)

      // determine zone
      const zone = Math.floor((long + 180) / 6) + 1

      // proj4 coordinate system definitions
      const utmProjection = `+proj=utm +zone=${zone} +ellps=GRS80 +datum=NAD83 +units=m +no_defs`
      const coords = proj4(utmProjection, [long, lat])

      utm.easting = String(coords[0])
      utm.northing = String(coords[1])
      utm.zone = zone

      return utm
    },
    convertToWGS84 (easting, northing, zone) {
      // converts from UTM to WGS84
      northing = Number(northing)
      easting = Number(easting)
      zone = Number(zone)

      // proj4 coordinate system definitions
      const wgs84Projection = proj4.defs('EPSG:4326')
      const utmProjection = `+proj=utm +zone=${zone} +ellps=${this.ellps} +datum=${this.datum} +units=m +no_defs`

      const coords = proj4(utmProjection, wgs84Projection, [easting, northing])

      return {
        longitude: String(coords[0]),
        latitude: String(coords[1])
      }
    },
    convertToDMS (degrees) {
      // converts from decimal degrees to degrees, minutes seconds
      // returns an object with keys 'deg', 'min', 'sec'

      degrees = Number(degrees)

      const angle = Math.abs(degrees)
      const deg = Math.floor(angle) * Math.sign(degrees)
      const sec = (3600 * (angle - Math.floor(angle)) % 60).toFixed(2)
      const min = Math.floor((3600 * (angle - Math.floor(angle))) / 60)

      return {
        deg: String(deg),
        min: String(min),
        sec: String(sec)
      }
    },
    convertDMStoDeg (dms) {
      const sign = Math.sign(dms.deg)

      return (dms.deg + sign * dms.min / 60 + sign * dms.sec / (60 * 60)).toFixed(6)
    },
    updateUTM (easting, northing, zone) {
      this.utm.easting = easting
      this.utm.northing = northing
      this.utm.zone = zone
    },
    resetUTM () {
      this.utm = {
        easting: '',
        northing: '',
        zone: ''
      }
    },
    updateDMS (longitude = {}, latitude = {}) {
      this.dms.long = longitude
      this.dms.lat = latitude
    },
    resetDMS () {
      this.dms = {
        lat: {
          deg: '',
          min: '',
          sec: ''
        },
        long: {
          deg: '',
          min: '',
          sec: ''
        }
      }
    },
    updateDegrees (longitude, latitude) {
      this.degrees.longitude = longitude
      this.degrees.latitude = latitude
    },
    resetDegrees () {
      this.degrees = {
        latitude: '',
        longitude: ''
      }
    },
    parseCoordValue (value) {
      // check that the input contains at least one number
      if (!value.match(/[0-9]/)) {
        value = '0'
      }

      // check that there are no dashes except when at the beginning of the string
      if (value.length > 1 && value.substr(1).match(/-/)) {
        value = '0'
      }

      // check that there is maximum one decimal ('.') character
      if ((value.match(/\./g) || []).length > 1) {
        value = '0'
      }

      value = value.replace(/[^0-9.-]/g, '')
      return value
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
    }
  }
}
</script>

<style>

</style>
