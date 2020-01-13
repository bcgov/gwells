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
                  @input="handleDegreesChange"
                  v-model.number="degrees.latitude"
                  :errors="errors['latitude']"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="6" lg="3" offset-lg="2">
                <form-input
                  id="longitude"
                  type="text"
                  @input="handleDegreesChange"
                  label="Longitude"
                  hint="Decimal degrees"
                  v-model.number="degrees.longitude"
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
                      @input="handleDMSChange"
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
                      @input="handleDMSChange"
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
                      @input="handleDMSChange"
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
                      @input="handleDMSChange"
                      hint="Degrees"
                      v-model.number="dms.long.deg"
                      :errors="errors['longitude']"
                      :loaded="fieldsLoaded['longitude']"
                    ></form-input>
                  </b-col>
                  <b-col cols="12" sm="4" class="px-2">
                    <form-input
                      id="longitudeMin"
                      type="text"
                      @input="handleDMSChange"
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
                      @input="handleDMSChange"
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
                  @input="handleUTMChange"
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
                  @input="handleUTMChange"
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
                  @input="handleUTMChange"
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
      utm: {
        easting: null,
        northing: null,
        zone: ''
      },
      latitudeDMSValidation: false,
      coordinateLookup: new Map(),
      coordinateResolveLookup: new Map(),
      validCoordinate: null,
      timeout: null
    }
  },
  created () {
    if (this.latitude || this.longitude) {
      // If we're loaded with a latitude and longitude, trigger an update so that degree,minute,second
      // and East/Northing get populated.
      this.handleMapCoordinate({ lng: Math.abs(Number(this.longitude)), lat: Number(this.latitude) })
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
    mapLatitude () {
      // We have to make sure that the map get's a number or a null, otherwise "" may turn into 0.
      return this.degrees.latitude ? Number(this.degrees.latitude) : null
    },
    mapLongitude () {
      // We have to make sure that the map get's a number or a null, otherwise "" may turn into 0.
      return this.degrees.longitude ? Number(this.degrees.longitude) : null
    },
    ...mapGetters(['codes'])
  },
  methods: {
    transformToPositive (value) {
      // Take a value, if it's a number - make it positive. If it's not a number, leave it alone
      return isFinite(value) ? Math.abs(value) : value
    },
    transformToNegative (value) {
      // Take a value, if it's a number - make it negative. If it's not a number, leave it alone.
      return isFinite(value) ? Math.abs(value) * -1 : value
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
    handleDegreesChange () {
      if (!this.degrees.latitude || !this.degrees.longitude) {
        this.resetUTM()
        this.resetDMS()
        return null
      }
      const { longitude, latitude } = this.degrees

      this.updateDegrees(longitude, latitude)

      const { easting, northing, zone } = this.convertToUTM(longitude, latitude)
      this.checkIfCoordinateIsValid(latitude, longitude)
      this.updateDMS(this.convertToDMS(longitude), this.convertToDMS(latitude))
      this.updateUTM(easting, northing, zone)
    },
    handleDMSChange () {
      if (!isFinite(this.dms.lat.deg) || !isFinite(this.dms.lat.min) || !isFinite(this.dms.lat.sec) || !isFinite(this.dms.long.deg) || !isFinite(this.dms.long.min) || !isFinite(this.dms.long.sec)) {
        // early return if any fields empty
        // reset other coordinate fields at the same time (e.g. clean up previously calculated valuess)
        this.resetUTM()
        this.resetDegrees()
        return null
      }

      const lat = this.convertDMStoDeg(this.dms.lat)
      const lng = this.convertDMStoDeg(this.dms.long)
      this.updateDegrees(lng, lat)
      const { easting, northing, zone } = this.convertToUTM(this.degrees.longitude, this.degrees.latitude)
      this.updateUTM(easting, northing, zone)
    },
    handleUTMChange () {
      if (!isFinite(this.utm.easting) || !isFinite(this.utm.northing) || !this.utm.zone) {
        this.resetDMS()
        this.resetDegrees()
        return null
      }

      const { longitude, latitude } = this.convertToWGS84(this.utm.easting, this.utm.northing, this.utm.zone || 0)
      this.updateDegrees(longitude, latitude)
      this.updateDMS(this.convertToDMS(longitude), this.convertToDMS(latitude))
    },
    updateDMS (longitude = {}, latitude = {}) {
      this.dms.long = longitude
      this.dms.long.deg = Math.abs(longitude.deg)
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
      // Set the prop value of longitude and latitude
      this.longitudeInput = newLong
      this.latitudeInput = newLat
      this.degrees.longitude = Math.abs(newLong)
      this.degrees.latitude = newLat
      this.checkIfCoordinateIsValid(newLat, newLong)
    },
    resetDegrees () {
      this.degrees = {
        latitude: null,
        longitude: null
      }
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
          const params = { latitude, longitude }
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
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.insideBC(latitude, longitude).then((result) => {
          this.validCoordinate = result
        })
      }, 500)
    }
  }
}
</script>

<style>

</style>
