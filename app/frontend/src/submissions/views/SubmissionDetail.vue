<template>
<div>
    <b-card v-if="submission && breadcrumbs && breadcrumbs.length" no-body class="mb-3 container container-wide d-print-none">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <b-card v-if="userRoles.wells.edit || userRoles.submissions.edit" class="container p-1 container-wide">
    <b-card-body>
      <div v-if="submission">
        <h1>Activity Report Summary</h1>
        <div>Filed: {{submission.create_date | moment("MMMM Do YYYY [at] LT") }}</div>
        <div>By: {{submission.create_user}} </div>
        <dl class="mt-5">
          <template v-for="(value, key, i) in submission">
            <div
              :key="`submission data row ${i} value`"
              class="row"
              v-if="
                value !== null &&
                (Array.isArray(value) && value.length > 0 || !Array.isArray(value)) &&
                key !== 'create_user' && // we will display these fields separately
                key !== 'create_date'
            ">
              <dt class="col-12 col-md-6 col-xl-2">{{key | readable}}</dt><dd class="col-12 col-md-6 col-xl-10">{{value}}</dd>
            </div>
          </template>
        </dl>
      </div>
    </b-card-body>
  </b-card>
</div>

</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'

// adds 'readable' filter
import inputFormatMixin from '@/common/inputFormatMixin.js'

export default {
  name: 'SubmissionDetail',
  mixins: [inputFormatMixin],
  data () {
    return {
      breadcrumbs: [
        {
          text: `Well Search`,
          to: { name: 'wells-home' }
        },
        {
          text: `Well ${this.$route.params.id} Summary`,
          to: { name: 'wells-detail', params: { id: this.$route.params.id } }
        },
        {
          text: `Edit Well`,
          to: { name: 'SubmissionsEdit', params: { id: this.$route.params.id } }
        },
        {
          text: `Activity Report Summary`,
          active: true
        }
      ],
      submission: {}
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
