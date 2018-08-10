<template>
    <fieldset>
      <legend>Geographic Coordinates</legend>
      <b-card no-body class="p-3 m-1 m-md-1">
        <b-row>
          <b-col cols="12" sm="6" lg="3">
            <form-input
              id="latitude"
              type="text"
              label="Latitude"
              hint="Decimal degrees"
              append="W"
              v-model="latitude"
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
              v-model="longitude"
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
                  :errors="errors['latitude']"
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
                  v-model="longitudeDMS.deg"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeMin"
                  type="text"
                  hint="Minutes"
                  v-model="longitudeDMS.min"
                  :errors="errors['longitude']"
                  :loaded="fieldsLoaded['longitude']"
                ></form-input>
              </b-col>
              <b-col cols="12" sm="4">
                <form-input
                  id="longitudeSec"
                  type="text"
                  hint="Seconds"
                  v-model="longitudeDMS.sec"
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
              :options="['16W', '16V']"
              label="Zone"
              v-model="utm.zone"
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
    </fieldset>
</template>
<script>
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'Step04Coords',
  mixins: [inputBindingsMixin],
  props: {
    latitude: String,
    longitude: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    latitudeInput: 'latitude',
    longitudeInput: 'longitude'
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
      latitudeDMSValidation: null
    }
  },
  computed: {},
  watch: {
    latitudeDMS: {
      deep: true,
      handler: function (value) {
        if (this.validDMSLat(value)) {
          this.latitudeInput = (value.deg + value.min / 60 + value.sec / (60 * 60)).toFixed(6)
          this.latitudeDMSValidation = null
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
