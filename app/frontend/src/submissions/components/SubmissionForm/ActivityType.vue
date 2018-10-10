<template>
  <fieldset>
    <legend>Type of Work</legend>
    <b-row>
      <b-col cols="12" md="6">
        <b-form-group label="Type of Work *">
          <b-form-radio-group v-model="wellActivityTypeInput"
                              stacked
                              name="submissionTypeRadio">
            <b-form-radio value="CON">Construction</b-form-radio>
            <b-form-radio value="ALT">Alteration</b-form-radio>
            <b-form-radio value="DEC">Decommissioning</b-form-radio>
            <b-form-radio value="STAFF_EDIT" v-if="userRoles.wells.edit">Other Report Types</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
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
    wellActivityType: String
  },
  computed: {
    ...mapGetters(['userRoles'])
  }
}
</script>

<style>
</style>
