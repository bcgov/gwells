<template>
  <fieldset>
    <legend>Step 9: Screen Information</legend>
    <b-row>
      <b-col cols="12" md="6">
        <form-input
          id="screenIntake"
          label="Intake"
          select
          :options="codes.screen_intake_methods"
          text-field="description"
          value-field="screen_intake_code"
          placeholder="Select intake"
          v-model="screenIntakeInput"></form-input>
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
    screenIntakeMethod: String,
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
  // The fields property helps to bind v-model (on the form input components) to a prop.
  // Set v-model to the key (see the form input above); the value corresponds to a prop declared on this component
  // Prop values will then be synced with the parent component. This way we can break apart a large form
  // into smaller components. Normally this is not necessary but we are composing a large POST request
  // out of many small components.
  fields: {
    screenIntakeInput: 'screenIntakeMethod',
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
