<template>
  <fieldset>
    <legend :id="id">Comments</legend>
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
                value="True"
                unchecked-value="False">
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
    alternativeSpecsSubmitted: String,
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
