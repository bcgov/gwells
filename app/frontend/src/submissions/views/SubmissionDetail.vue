<template>
<div>
  <b-card v-if="breadcrumbs && breadcrumbs.length" no-body class="mb-3 container d-print-none">
    <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
  </b-card>
  <b-card v-if="userRoles.wells.edit || userRoles.submissions.edit" class="container p-1">
    <b-card-body>
      <h1>Activity Report Summary</h1>
      <div v-if="loading">
        <div class="fa-2x text-center">
          <i class="fa fa-circle-o-notch fa-spin"></i>
        </div>
      </div>
      <div v-else>
        <div v-if="submission.create_date">Filed: {{ moment(submission.create_date, "MMMM Do YYYY [at] LT") }}</div>
        <div>By: {{submission.create_user}} </div>
        <dl class="mt-5">
          <template v-for="(value, key, i) in submission" :key="`submission data row ${i} value`">
            <div
              class="row record"
              v-if="showRow(key, value)">
              <dt class="col-12 col-md-6 col-xl-2">{{ readable(key) }}</dt>
              <dd class="col-12 col-md-6 col-xl-10">{{value}}</dd>
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
import { useSubmissionStore } from '@/stores/submission.js'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'SubmissionDetail',
  data () {
    return {
      loading: false,
      submissionStore: null,
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
      submission: null,

      // we don't need to display audit fields (we display them elsewhere on the page) or
      // the submission's id.
      excluded_fields: [
        'create_user',
        'update_user',
        'filing_number'
      ]
    }
  },
  computed: {
    codes () { return this.submissionStore ? this.submissionStore.codes : {} },
    ...mapGetters(['userRoles'])
  },
  methods: {
    fetchSubmission () {
      this.loading = true
      ApiService.get('submissions', this.$route.params.submissionId).then((response) => {
        this.loading = false
        this.submission = response.data
      }).catch((e) => {
        this.loading = false

        this.$noty.info('Error retrieving activity report summary. Please try again later.', { killer: true })
        throw e
      })
    },
    showRow (key, value) {
      if (value === null) {
        return false
      } else if (Array.isArray(value) && value.length === 0) {
        return false
      } else if (this.excluded_fields.indexOf(key) !== -1) {
        return false
      }

      return true
    },
    readable (val) {
      return val ? val.charAt(0).toUpperCase() + val.split('_').join(' ').substring(1) : ''
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
    this.fetchSubmission()
  }
}
</script>

<style>
.record {
  margin: 10px 0
}
.record dt {
  line-height: 1.2
}
</style>
