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
  <form-subsection title="Change History" :id="id" class="mt-12" :hideSave="true">
    <div class="flex">
      <well-history :well-tag-number="wellTagNumber" resource="wells" :events="events" ref="wellHistory"/>
    </div>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'
import WellHistory from './WellHistory.vue'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  name: 'StaffEditHistory',
  props: {
    id: {
      type: String
    },
    wellTagNumber: {
      type: Number,
      isInput: false
    },
    // TBD events handled differently in Vue 3
    // and not need to be passed a prop
    // Possibly replace with vue watch.
    // events: {
    //   type: Vue
    // }
  },
  components: {
    WellHistory,
    FormSubsection
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
  }
}
</script>

<style>

</style>
