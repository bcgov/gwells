<template>
    <fieldset>
      <legend>Geographic Coordinates</legend>
      <b-row>
        <b-col cols="12" sm="6" lg="3">
          <form-input
            id="latitude"
            type="text"
            label="Latitude"
            hint="Decimal degrees"
            v-model="latitudeInput"
            :errors="errors['latitude']"
            :loaded="fieldsLoaded['latitude']"
          ></form-input>
        </b-col>
        <b-col cols="12" sm="6" lg="3">
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
      <b-row><b-col><p>OR</p></b-col></b-row>
      <b-row>
        <b-col cols="12" sm="6" lg="3">
            <form-input
              id="latitude"
              type="text"
              label="Latitude"
              hint="Degrees, minutes, seconds"
              v-model="latitudeInput"
              :errors="errors['latitude']"
              :loaded="fieldsLoaded['latitude']"
            ></form-input>
        </b-col>
        <b-col cols="12" sm="6" lg="3">
          <form-input
            id="longitude"
            type="text"
            label="Longitude"
            hint="Degrees, minutes, seconds"
            v-model="longitudeInput"
            :errors="errors['longitude']"
            :loaded="fieldsLoaded['longitude']"
          ></form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>
<script>
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
// import ApiService from '@/common/services/ApiService.js'
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

    }
  },
  computed: {},
  watch: {},
  methods: {}
}
</script>

<style>

</style>
