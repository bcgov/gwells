<template>
  <b-card v-if="userRoles.wells.edit || userRoles.submissions.edit">
    <b-card-body>
      <div v-if="submission">
        <dl>
          <template v-for="(value, key, i) in submission">
            <div :key="`submission data row ${i} value`" class="row" v-if="value !== null && (Array.isArray(value) && value.length > 0 || !Array.isArray(value))">
              <dt class="col-12 col-md-6 col-xl-2">{{key}}</dt><dd class="col-12 col-md-6 col-xl-10">{{value}}</dd>
            </div>
          </template>
        </dl>
      </div>
    </b-card-body>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'SubmissionDetail',
  data () {
    return {
      submission: null
    }
  },
  computed: {
    ...mapGetters(['codes', 'userRoles'])
  },
  methods: {
    fetchSubmission () {
      ApiService.get('submissions', this.$route.params.submissionId).then((response) => {
        this.submission = response.data
      }).catch((e) => {

      })
    }
  },
  created () {
    this.fetchSubmission()
  }
}
</script>

<style>

</style>
