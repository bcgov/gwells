<template>
<div>
  <div class="container mb-4 !px-0" v-if="breadcrumbs && breadcrumbs.length">
    <Breadcrumb class="p-0" :model="breadcrumbs">
      <template #item="{ item }">
        <router-link v-if="!item.active" :to="item.route">{{ item.label }}</router-link>
        <span v-else>{{ item.label }}</span>
      </template>
    </Breadcrumb>
  </div>
  <Card v-if="commonStore.userRoles.wells.edit || commonStore.userRoles.submissions.edit" class="container p-1">
    <template #title>Activity Report Summary</template>
    <template #content>
      <div v-if="loading">
        <div class="fa-2x text-center">
          <i class="fa fa-circle-o-notch fa-spin"></i>
        </div>
      </div>
      <div v-else>
        <div v-if="submission.create_date">Filed: {{ moment(submission.create_date, "MMMM Do YYYY [at] LT") }}</div>
        <div>By: {{submission.create_user}} </div>
        <dl class="mt-12">
          <!-- TODO: Look into these old bootstrap classes -->
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
    </template>
  </Card>
</div>

</template>

<script>
import { useCommonStore } from '@/stores/common.js'
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
          label: `Well Search`,
          route: { name: 'wells-home' }
        },
        {
          label: `Well ${this.$route.params.id} Summary`,
          route: {
            name: 'wells-detail',
            params: { id: this.$route.params.id }
          }
        },
        {
          label: `Edit Well`,
          route: {
            name: 'SubmissionsEdit',
            params: { id: this.$route.params.id }
          }
        },
        {
          label: `Activity Report Summary`,
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
    commonStore () { return useSubmissionStore() },
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
