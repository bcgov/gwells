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
              @focus="freeze('deg')"
              @blur="unfreeze('deg')"
              v-model="degrees.latitude"
              :errors="errors['latitude']"
              :loaded="fieldsLoaded['latitude']"
            ></form-input>
          </b-col>
          <b-col cols="12" sm="6" lg="3" offset-lg="2">
            <form-input
              id="longitude"
              type="text"
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
                  type="number"
                  hint="Degrees"
                  v-model.number="dms.lat.deg"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeMin"
                  type="number"
                  hint="Minutes"
                  v-model.number="dms.lat.min"
                  :errors="errors['latitude']"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeSec"
                  type="text"
                  hint="Seconds"
                  v-model.number="dms.lat.sec"
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
                  hint="Degrees"
                  v-model.number="dms.long.deg"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeMin"
                  type="number"
                  hint="Minutes"
                  v-model.number="dms.long.min"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeSec"
                  type="number"
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
          <b-col cols="12" sm="4" lg="2">
            <form-input
              id="utmZone"
              select
              :options="utmZones"
              label="Zone"
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
      <b-btn variant="primary" @click="convertToUTM">UTM</b-btn>
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
      coords: {
        latitude: '',
        longitude: '',
        latSource: '',
        longSource: ''
      },
      utmZone: '',
      // BC is covered by UTM zones 7 through 11
      utmZones: [
        {'value': '', 'name': 'Select zone'},
        {'value': 7, 'name': '7'},
        {'value': 8, 'name': '8'},
        {'value': 9, 'name': '9'},
        {'value': 10, 'name': '10'},
        {'value': 11, 'name': '11'}],
      latitudeDMSValidation: false
    }
  },
  computed: {
    lat () {
      const lat = Number(this.coords.latitude)

      // we have latitude as a number now, but the initial check
      // will be for the original this.coords.latitude input. It will
      // allow us to differentiate between no input and the number 0.
      if (this.coords.latitude && lat >= -180 && lat <= 180) {
        return Number(this.coords.latitude)
      }
      return null
    },
    long () {
      const long = Number(this.coords.longitude)

      // ensure that longitude is within range and original input has a value
      if (this.coords.longitude && long >= -180 && long <= 180) {
        return Number(this.coords.longitude)
      }
      return null
    },
    utmEasting: {
      set: function (val) {
        if (!this.lock.utm) {
          if (this.utmZone && val.length === 6) {
            this.coords.longitude = this.convertToWGS84(Number(val), 0, this.utmZone).longitude
            this.coords.longSource = 'utmE'
          }
          this.utm.easting = val
        }
      },

      get: function () {
        if (this.coords.longSource === 'utmE') {
          return this.utm.easting
        }
        // get easting from coords
        return this.long ? this.convertToUTM(this.long, 0).easting : ''
      }
    },
    utmNorthing: {
      set: function (val) {
        if (!this.lock.utm) {
          this.coords.latitude = this.convertToWGS84(0, Number(val)).latitude
          this.coords.latSource = 'utmN'
          this.utm.northing = val
        }
      },

      get: function () {
        if (this.coords.latSource === 'utmN') {
          return this.utm.northing
        }
        // get northing from coords
        return this.lat ? this.convertToUTM(0, this.lat).northing : ''
      }
    },
    ...mapGetters(['codes'])
  },
  watch: {
    'dms.lat': {
      deep: true,
      handler: function (value) {
        if (!value.deg && !value.min && !value.sec) {
          // early return if all fields empty
          // reset other coordinate fields at the same time (e.g. clean up previously calculated values)
          this.degrees.latitude = ''
          this.utm.northing = ''
          return null
        }

        const dms = Object.assign({}, value)
        dms.deg = Number(value.deg) || 0
        dms.min = Number(value.min) || 0
        dms.sec = Number(value.sec) || 0

        const lat = (dms.deg + dms.min / 60 + dms.sec / (60 * 60)).toFixed(6)
        if (!this.lock.deg) this.degrees.latitude = lat
        if (!this.lock.utm) this.utm.northing = this.convertToUTM(0, lat).northing
      }
    },
    'dms.long': {
      deep: true,
      handler: function (value) {
        if (!value.deg && !value.min && !value.sec) {
          this.degrees.longitude = ''
          this.utm.easting = ''
          this.utm.zone = ''
          return null
        }

        const dms = Object.assign({}, value)
        dms.deg = Number(value.deg) || 0
        dms.min = Number(value.min) || 0
        dms.sec = Number(value.sec) || 0

        const long = (dms.deg + dms.min / 60 + dms.sec / (60 * 60)).toFixed(6)

        this.degrees.longitude = long

        const { easting, zone } = this.convertToUTM(long, 0)
        this.utm.easting = easting
        this.utm.zone = zone
      }
    },
    'degrees.latitude': {
      deep: true,
      handler: function (value) {
        if (!value) {
          this.dms.lat = {
            deg: '',
            min: '',
            sec: ''
          }
          this.utm.northing = ''
          return null
        }

        const lat = Number(value)
        const deg = Math.floor(lat)
        const sec = (3600 * (lat - Math.floor(lat)) % 60).toFixed(2)
        const min = Math.floor((3600 * (lat - Math.floor(lat))) / 60)

        const dms = {
          deg: deg,
          min: min,
          sec: sec
        }

        this.dms.lat = dms
        this.utm.northing = this.convertToUTM(0, lat).northing
      }
    }
  },
  methods: {
    validDMSLat (value) {
      return (
        value.deg >= -90 &&
        value.deg <= 90 &&
        value.min >= 0 &&
        value.min <= 60 &&
        value.sec >= 0 &&
        value.sec <= 60)
    },
    validDMSLng (value) {
      return (
        value.deg >= -180 &&
        value.deg <= 180 &&
        value.min >= 0 &&
        value.min <= 60 &&
        value.sec >= 0 &&
        value.sec <= 60)
    },
    convertToUTM (long, lat) {
      // converts input coordinates and returns an object containing UTM easting, northing, and zone
      const utm = {
        easting: '',
        northing: '',
        zone: ''
      }

      lat = Number(lat)
      long = Number(long)

      const wgs84Projection = proj4.defs('EPSG:4326')

      // determine zone
      const zone = Math.floor((long + 180) / 6) + 1

      const utmProjection = `+proj=utm +zone=${zone} +ellps=${this.ellps} +datum=${this.datum} +units=m +no_defs`
      const coords = proj4(wgs84Projection, utmProjection, [long, lat])

      utm.easting = coords[0]
      utm.northing = coords[0]
      utm.zone = zone

      return utm
    },
    convertToWGS84 (easting, northing, zone) {
      // converts from UTM to WGS84
      northing = Number(northing)
      easting = Number(easting)
      zone = Number(zone)

      const wgs84Projection = proj4.defs('EPSG:4326')
      const utmProjection = `+proj=utm +zone=${zone} +ellps=${this.ellps} +datum=${this.datum} +units=m +no_defs`

      const coords = proj4(utmProjection, wgs84Projection, [easting, northing])

      return {
        longitude: coords[0],
        latitude: coords[1]
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
    }
  }
}
</script>

<style>

</style>
