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
  <div>
    <fieldset>
      <b-row>
        <b-col cols="12" lg="6">
          <legend :id="id">Geographic Coordinates</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <p>To determine coordinates using a Global Positioning System (GPS), set the datum to North America Datum of 1983 (NAD 83), the current ministry standard for mapping.</p>
      <p>After the GPS coordinates are entered, the map pin can be moved by clicking and dragging it on the map. The GPS coordinates will be updated automatically.</p>
      <b-row>
        <b-col sm="12" md="6">
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
                  v-model.number="latitudeInput"
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
                  v-model.number="computedLongitude"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
            </b-row>
          </b-card>
          <b-row><b-col><p class="p-3 m-0">OR</p></b-col></b-row>
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
                      type="text"
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
                      type="text"
                      v-model.number="dms.lat.min"
                      :errors="errors['latitude']"
                      :loaded="fieldsLoaded['latitude']"
                    ></form-input>
                  </b-col>
                  <b-col cols="12" sm="4" class="px-1">
                    <form-input
                      id="latitudeSec"
                      type="text"
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
                      type="text"
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
                      type="text"
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
                      type="text"
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
          <b-row><b-col><p class="p-3 m-0">OR</p></b-col></b-row>
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
                  type="text"
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
                  type="text"
                  label="UTM Northing"
                  @focus="unfreeze('utm')"
                  @blur="freeze('utm')"
                  v-model.number="utm.northing"
                  :max="9999999"
                  :loaded="fieldsLoaded['utmNorthing']"
                ></form-input>
              </b-col>
            </b-row>
            <b-row v-if="isStaffEdit">
              <b-col>
                <form-input
                  id="coordinateAcquisitionCode"
                  select
                  :options="codes.coordinate_acquisition_codes"
                  label="Coordinate Acquisition"
                  v-model="coordinateAcquisitionCodeInput"
                  text-field="description"
                  value-field="code"
                  :loaded="fieldsLoaded['coordinateAcquisitionCode']"
                ></form-input>
              </b-col>
            </b-row>
          </b-card>
          <b-row>
            <b-col class="mt-3">
              <div v-if="validCoordinate === false">
                <div class="alert alert-danger" role="alert">You have entered an invalid coordinate</div>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col sm="12" md="6">
          <coords-map :latitude="mapLatitude" :longitude="mapLongitude" v-on:coordinate="handleMapCoordinate" :insideBC="insideBC"/>
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
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ApiService from '@/common/services/ApiService.js'
export default {
  components: {
    'coords-map': CoordsMap
  },
  name: 'Coords',
  mixins: [inputBindingsMixin, convertCoordinatesMixin],
  props: {
    latitude: null,
    longitude: null,
    coordinateAcquisitionCode: null,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    errorCoordsNotProvided: Boolean,
    id: {
      type: String,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      ellps: 'GRS80', // UTM config parameters. This does not apply to degrees latitude/longitude
      datum: 'nad83',
      lock: {
        utm: true,
        dms: true,
        deg: false
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
      latitudeDMSValidation: false,
      coordinateLookup: new Map(),
      coordinateResolveLookup: new Map(),
      validCoordinate: null
    }
  },
  created () {
    if (this.latitude || this.longitude) {
      // If we're loaded with a latitude and longitude, trigger an update so that degree,minute,second
      // and East/Northing get populated.
      this.handleMapCoordinate({lng: Number(this.longitude), lat: Number(this.latitude)})
    }
  },
  computed: {
    // BC is covered by UTM zones 7 through 11
    utmZones () {
      const zones = [{
        'value': '',
        'name': 'Select zone'
      }]
      const options = [7, 8, 9, 10, 11]
      options.forEach(i => {
        zones.push({
          'value': i,
          'name': i
        })
      })
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
    mapLatitude () {
      // We have to make sure that the map get's a number or a null, otherwise "" may turn into 0.
      return this.latitudeInput ? Number(this.latitudeInput) : null
    },
    mapLongitude () {
      // We have to make sure that the map get's a number or a null, otherwise "" may turn into 0.
      return this.longitudeInput ? Number(this.longitudeInput) : null
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
          latitude = Number(latitude)
          const { easting, northing, zone } = this.convertToUTM(Number(this.longitudeInput), Number(latitude))

          this.checkIfCoordinateIsValid(latitude, this.longitudeInput)
          this.updateDMS(this.convertToDMS(Number(this.longitudeInput)), this.convertToDMS(Number(latitude)))
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
          long = Number(long)
          const { easting, northing, zone } = this.convertToUTM(long, Number(this.latitudeInput))

          this.checkIfCoordinateIsValid(this.latitudeInput, long)
          this.updateDMS(this.convertToDMS(long), this.convertToDMS(Number(this.latitudeInput)))
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
      const newLong = this.roundDecimalDegrees(longitude)
      const newLat = this.roundDecimalDegrees(latitude)
      this.longitudeInput = newLong
      this.latitudeInput = newLat
      this.checkIfCoordinateIsValid(newLat, newLong)
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
    },
    insideBC (latitude, longitude) {
      return new Promise((resolve, reject) => {
        // Longitude may sometimes drop the minus (negative) sign, we make sure to add it back in.
        longitude = this.roundDecimalDegrees(this.transformToNegative(longitude))
        latitude = this.roundDecimalDegrees(latitude)
        // We use a dictionary to reduce network traffic, by storing and checking for coordinates locally.
        const key = `${latitude};${longitude}`
        if (this.coordinateLookup.has(key)) {
          // We already have this key, so we don't have to do a network call.
          resolve(this.coordinateLookup.get(key))
        } else if (this.coordinateResolveLookup.has(key)) {
          // We already have an outstanding promise for this key, so we store a reference to the resolve for
          // this promise.
          const resolveList = this.coordinateResolveLookup.get(key)
          resolveList.push(resolve)
        } else {
          const resolveList = []
          this.coordinateResolveLookup.set(key, resolveList)
          const params = {
            latitude: latitude,
            longitude: longitude}
          ApiService.query('gis/insidebc', params).then((response) => {
            // Store the result for future lookups.
            this.coordinateLookup.set(key, response.data.inside)
            // Remove our promise lookup
            this.coordinateResolveLookup.delete(key)
            // Call resolve for any other promises that have been made on this key
            resolveList.forEach((item) => {
              // We resolve all the other promises
              item(response.data.inside)
            })
            // We resolve this promise
            resolve(response.data.inside)
          })
        }
      })
    },
    checkIfCoordinateIsValid (latitude, longitude) {
      this.insideBC(latitude, longitude).then((result) => {
        this.validCoordinate = result
      })
    }
  }
}
</script>

<style>

</style>
