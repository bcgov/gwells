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
              append="W"
              v-model="latitudeInput"
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
              v-model="longitudeInput"
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
                  type="text"
                  hint="Degrees"
                  v-model.number="latitudeDMS.deg"
                  :state="latitudeDMSValidation"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeMin"
                  type="text"
                  hint="Minutes"
                  v-model.number="latitudeDMS.min"
                  :errors="errors['latitude']"
                  :loaded="fieldsLoaded['latitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="latitudeSec"
                  type="text"
                  hint="Seconds"
                  v-model.number="latitudeDMS.sec"
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
                  v-model.number="longitudeDMS.deg"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeMin"
                  type="text"
                  hint="Minutes"
                  v-model.number="longitudeDMS.min"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeSec"
                  type="text"
                  hint="Seconds"
                  v-model.number="longitudeDMS.sec"
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
              :loaded="fieldsLoaded['utmEasting']"
            ></form-input>
          </b-col>
          <b-col cols="12" sm="4" lg="3">
            <form-input
              id="utmNorthing"
              type="text"
              label="UTM Northing"
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
              :options="['GPS']"
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
              :options="['Big drill', 'Small drill']"
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
      latitudeDMS: {
        deg: '',
        min: '',
        sec: ''
      },
      longitudeDMS: {
        deg: '',
        min: '',
        sec: ''
      },
      utm: {
        zone: '',
        easting: '',
        northing: ''
      },
      // BC is covered by UTM zones 7 through 11
      utmZones: [
        {'value': '', 'name': 'Select zone'},
        {'value': '7', 'name': '7'},
        {'value': '8', 'name': '8'},
        {'value': '9', 'name': '9'},
        {'value': '10', 'name': '10'},
        {'value': '11', 'name': '11'}],
      latitudeDMSValidation: false
    }
  },
  computed: {},
  watch: {
    latitudeDMS: {
      deep: true,
      handler: function (value) {
        const dms = Object.assign({}, value)
        dms.min = value.min || 0
        dms.sec = value.sec || 0
        if (this.validDMSLat(dms)) {
          this.latitudeInput = (dms.deg + dms.min / 60 + dms.sec / (60 * 60)).toFixed(6)
          this.latitudeDMSValidation = null
        }
      }
    },
    longitudeDMS: {
      deep: true,
      handler: function (value) {
        const dms = Object.assign({}, value)
        dms.min = value.min || 0
        dms.sec = value.sec || 0
        if (this.validDMSLng(dms)) {
          this.longitudeInput = (dms.deg + dms.min / 60 + dms.sec / (60 * 60)).toFixed(6)
          this.longitudeDMSValidation = null
        }
      }
    }
  },
  methods: {
    validDMSLat (value) {
      return (
        value.deg >= 0 &&
        value.deg <= 90 &&
        value.min >= 0 &&
        value.min <= 60 &&
        value.sec >= 0 &&
        value.sec <= 60)
    },
    validDMSLng (value) {
      return (
        value.deg >= 0 &&
        value.deg <= 180 &&
        value.min >= 0 &&
        value.min <= 60 &&
        value.sec >= 0 &&
        value.sec <= 60)
    }
  }
}
</script>

<style>

</style>
