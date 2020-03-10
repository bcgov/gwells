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
  <fieldset>
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Well Work Dates</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">
            Save
          </b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <b-row v-if="isStaffEdit">
      <b-col cols="6" md="6">
        <form-input
          id="constructionStartDateInput"
          type="date"
          label="Start Date of Construction"
          placeholder="YYYY-MM-DD"
          v-model="constructionStartDateInput"
          :errors="errors.construction_start_date"
          :loaded="fieldsLoaded['construction_start_date']">
        </form-input>
      </b-col>
      <b-col cols="6" md="6">
        <form-input
          id="constructionEndDateInput"
          type="date"
          label="End Date of Construction"
          placeholder="YYYY-MM-DD"
          v-model="constructionEndDateInput"
          :errors="errors.construction_end_date"
          :loaded="fieldsLoaded['construction_end_date']">
        </form-input>
      </b-col>
    </b-row>
    <b-row v-if="isStaffEdit">
      <b-col cols="6" md="6">
        <form-input
          id="alterationStartDateInput"
          type="date"
          label="Start Date of Alteration"
          placeholder="YYYY-MM-DD"
          v-model="alterationStartDateInput"
          :errors="errors.alteration_start_date"
          :loaded="fieldsLoaded['alteration_start_date']">
        </form-input>
      </b-col>
      <b-col cols="6" md="6">
        <form-input
          id="alterationEndDateInput"
          type="date"
          label="End Date of Alteration"
          placeholder="YYYY-MM-DD"
          v-model="alterationEndDateInput"
          :errors="errors.alteration_end_date"
          :loaded="fieldsLoaded['alteration_end_date']">
        </form-input>
      </b-col>
    </b-row>
    <b-row v-if="isStaffEdit">
      <b-col cols="6" md="6">
        <form-input
          id="decommissionStartDateInput"
          type="date"
          label="Start Date of Decommission"
          placeholder="YYYY-MM-DD"
          v-model="decommissionStartDateInput"
          :errors="errors.decommission_start_date"
          :loaded="fieldsLoaded['decommission_start_date']">
        </form-input>
      </b-col>
      <b-col cols="6" md="6">
        <form-input
          id="decommissionEndDateInput"
          type="date"
          label="End Date of Decommission"
          placeholder="YYYY-MM-DD"
          v-model="decommissionEndDateInput"
          :errors="errors.decommission_end_date"
          :loaded="fieldsLoaded['decommission_end_date']">
        </form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    constructionStartDate: String,
    constructionEndDate: String,
    alterationStartDate: String,
    alterationEndDate: String,
    decommissionStartDate: String,
    decommissionEndDate: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
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
  computed: {
  },
  methods: {
  },
  watch: {
  },
  data () {
    return {
    }
  }
}
</script>

<style>
</style>
