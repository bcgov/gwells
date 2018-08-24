<template>
  <fieldset>
    <legend>Step 9: Screen Information</legend>
    <b-row>
      <b-col cols="12" md="6">
        <form-input id="screen" label="Screen" v-model="screenInput"></form-input>
      </b-col>
      <b-col cols="12" md="6">
        <form-input id="screen" label="Filter material" v-model="materialInput"></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    screen: String,
    material: String,
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
    screenInput: 'screen',
    materialInput: 'material'
  },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
