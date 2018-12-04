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
        <legend :id="id">Comments</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="8">
        <b-form-group label="Comments" id="commentsGroup">
          <b-form-textarea
              id="commentsEntry"
              :rows="3"
              :max-rows="12"
              v-model="commentsInput"></b-form-textarea>
        </b-form-group>
      </b-col>
    </b-row>
    <!-- <b-row>
      <b-col cols="12" sm="6"> -->

          <b-form-checkbox id="alternativeSpecsCheckbox"
                v-model="alternativeSpecsSubmittedInput"
                :value="true"
                :unchecked-value="false">
            Alternative specs submitted (if required)
          </b-form-checkbox>
      <!-- </b-col>
    </b-row> -->
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    comments: String,
    alternativeSpecsSubmitted: null,
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
  fields: {
    commentsInput: 'comments',
    alternativeSpecsSubmittedInput: 'alternativeSpecsSubmitted'
  },
  data () {
    return {
      status: 'False'
    }
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
