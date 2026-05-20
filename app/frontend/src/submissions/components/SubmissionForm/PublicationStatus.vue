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
  <form-subsection title="Well Publication Status" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <responsive-grid v-if="isStaffEdit" :cols="12" :md="4">
      <Select
        id="wellPublicationStatusCodeInput"
        v-model="wellPublicationStatusCodeInput"
        :options="codes?.well_publication_status_codes"
        optionValue="well_publication_status_code"
        optionLabel="well_publication_status_code"
        :loading="!fieldsLoaded['well_publication_status']"
        placeholder="Select Publication Status"/>
    </responsive-grid>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

export default {
  mixins: [inputBindingsMixin],
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
  components: {
    FormSubsection,
    ResponsiveGrid
  },
  data () {
    return {
      submissionStore: null
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    }
  },
  methods: {
  },
  watch: {
  }
}
</script>

<style>
</style>
