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
    <legend :id="id">Type of Work</legend>
    <b-row>
      <b-col cols="12" md="6">
        <b-form-group label="Type of Work *">
          <b-form-radio-group v-model="wellActivityTypeInput"
                              stacked
                              name="submissionTypeRadio"
                              id="reportType">
            <b-form-radio value="CON" v-if="userRoles.submissions.edit">Construction</b-form-radio>
            <b-form-radio value="ALT" v-if="userRoles.submissions.edit">Alteration</b-form-radio>
            <b-form-radio value="DEC" v-if="userRoles.submissions.edit">Decommissioning</b-form-radio>
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
    wellActivityType: String,
    id: {
      type: String,
      isInput: false
    }
  },
  computed: {
    ...mapGetters(['userRoles'])
  }
}
</script>

<style>
</style>
