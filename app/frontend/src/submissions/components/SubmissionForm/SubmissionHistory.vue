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
  <fieldset class="mt-5">
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Activity Reports</legend>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <p v-if="submissionsRecordsCount > 0">
          There {{ submissionsRecordsCount > 1 ? 'are' : 'is' }} {{ submissionsRecordsCount }} activity {{ submissionsRecordsCount > 1 ? 'reports' : 'report' }} for well {{ $route.params.id }}.
        </p>
        <b-table
            id="submissionHistoryTable"
            ref="submissionHistoryTable"
            :busy.sync="submissionsBusy"
            :items="fetchReports"
            :fields="['report', 'date_entered', 'entered_by']"
            responsive
            :per-page="submissionsPerPage"
            :current-page="submissionsPage"
          >
          <template slot="report" slot-scope="data">
            <router-link :to="{ name: 'SubmissionDetail', params: { id: $route.params.id, submissionId: data.item.filing_number }}">{{ data.item.well_activity_type }}</router-link>
          </template>
          <template slot="date_entered" slot-scope="data">
            {{ data.item.create_date | moment("MMMM Do YYYY [at] LT") }}
          </template>
          <template slot="entered_by" slot-scope="data">
            {{ data.item.create_user }}
          </template>
        </b-table>
        <b-pagination v-if="!!submissionsRecordsCount && submissionRecordsCount > submissionsPerPage" size="md" :total-rows="submissionsRecordsCount" v-model="submissionsPage" :per-page="submissionsPerPage" :disabled="submissionsBusy" />
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import querystring from 'querystring'
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'

export default {
  props: {
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
  data () {
    return {
      submissionsPerPage: 5,
      submissionsPage: 1,
      submissionsBusy: false,
      submissionsRecordsCount: 0
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    fetchReports (ctx = { perPage: this.perPage, currentPage: this.submissionsPage }) {
      /**
      * table items provider function
      * https://bootstrap-vue.js.org/docs/components/table/
      *
      * a refresh can be triggered by this.$root.$emit('bv::refresh::table', 'submissionHistoryTable')
      */
      const params = {
        limit: ctx.perPage,
        offset: ctx.perPage * (ctx.currentPage - 1)
      }
      // add other search parameters into the params object.
      // these will be urlencoded and the API will filter on these values.
      Object.assign(params, this.searchParams)
      return ApiService.query(`wells/${this.$route.params.id}/submissions` + '?' + querystring.stringify(params)).then((response) => {
        let results = response.data.results || []
        results = response.data.results.filter((item) => {
          return item.well_activity_type !== 'STAFF_EDIT'
        })

        this.submissionsRecordsCount = results.length
        return results
      }).catch((e) => {
        return []
      })
    }
  }
}
</script>

<style>

</style>
