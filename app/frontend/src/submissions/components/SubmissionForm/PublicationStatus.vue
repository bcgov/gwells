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
        <legend :id="id">Well Publication Status</legend>
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
      <b-col cols="12" md="4">
        <b-form-group id="wellPublicationStatusCodeInput">
          <b-form-select
            v-model="wellPublicationStatusCodeInput"
            :options="codes.well_publication_status_codes"
            value-field="well_publication_status_code"
            text-field="well_publication_status_code"
            :errors="errors['well_publication_status']"
            :loaded="fieldsLoaded['well_publication_status']">
            <template slot="first">
              <option :value="null" disabled>Select Publication Status</option>
            </template>
          </b-form-select>
        </b-form-group>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'

export default {
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    wellPublicationStatusCode: String,
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
    ...mapGetters(['codes'])
  },
  methods: {
  },
  watch: {
  }
}
</script>

<style>
</style>
