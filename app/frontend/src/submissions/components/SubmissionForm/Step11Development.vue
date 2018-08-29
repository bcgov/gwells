<template>
  <fieldset>
    <legend>Step 11: Well Development</legend>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="developmentMethod"
            label="Development Method"
            select
            :options="codes.development_methods"
            text-field="description"
            value-field="development_method_code"
            v-model="developmentMethodInput"
            placeholder="Select method"
            :errors="errors['development_method']"
            :loaded="fieldsLoaded['development_method']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="2">
        <form-input
            id="developmentHours"
            label="Development Hours"
            v-model="developmentHoursInput"
            :errors="errors['development_hours']"
            :loaded="fieldsLoaded['development_hours']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="10" lg="6">
        <form-input
            id="developmentNotes"
            label="Development Notes"
            v-model="developmentNotesInput"
            :errors="errors['development_notes']"
            :loaded="fieldsLoaded['development_notes']"></form-input>
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
    developmentMethod: String,
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
    developmentMethodInput: 'developmentMethod',
    developmentHoursInput: 'developmentHours',
    developmentNotesInput: 'developmentNotes'

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
