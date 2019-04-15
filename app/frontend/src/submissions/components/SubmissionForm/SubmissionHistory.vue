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
        <p>
          There {{ filteredSubmissions.length !== 1 ? 'are' : 'is' }} {{ filteredSubmissions.length }} activity {{ filteredSubmissions.length !== 1 ? 'reports' : 'report' }} for well {{ $route.params.id }}.
        </p>
        <b-table
            id="submissionHistoryTable"
            ref="submissionHistoryTable"
            :busy.sync="submissionsBusy"
            :items="filteredSubmissions"
            :fields="tableHeaders"
            responsive
            show-empty
            empty-text="There is currently no submission report history for this well. Scanned copies of paper reports may be available as an attachment."
            :per-page="submissionsPerPage"
            :current-page="submissionsPage"
          >
          <template slot="report" slot-scope="data">
            <div>
              <router-link :to="{ name: 'SubmissionDetail', params: { id: $route.params.id, submissionId: data.item.filing_number }}">{{ data.item.well_activity_description }}</router-link>
            </div>
          </template>
          <template slot="date_entered" slot-scope="data">
            <div>
              <span v-if="data.item.create_date">{{ data.item.create_date | moment("MMMM Do YYYY [at] LT") }}</span>
            </div>
          </template>
          <template slot="entered_by" slot-scope="data">
            <div>
              {{ data.item.create_user }}
            </div>
          </template>
        </b-table>
        <b-pagination v-if="!!filteredSubmissions.length && filteredSubmissions.length > submissionsPerPage" size="md" :total-rows="filteredSubmissions.length" v-model="submissionsPage" :per-page="submissionsPerPage" :disabled="submissionsBusy" />
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
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
    },
    submissionsHistory: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      submissionsPerPage: 5,
      submissionsPage: 1,
      submissionsBusy: false,
      submissionsRecordsCount: 0,
      tableHeaders: {
        report: {
          label: 'Report',
          thStyle: {
            width: '33%'
          }
        },
        date_entered: {
          label: 'Date Entered',
          thStyle: {
            width: '33%'
          }
        },
        entered_by: {
          label: 'Entered By',
          thStyle: {
            width: '33%'
          }
        }
      }
    }
  },
  computed: {
    filteredSubmissions () {
      return this.submissionsHistory.filter((i) => {
        return i.well_activity_type !== 'STAFF_EDIT'
      })
    },
    ...mapGetters(['codes'])
  }
}
</script>

<style>
.skeleton {
  color: transparent !important;
  pointer-events: none;
  user-select: none;
  border-color: rgb(240, 240, 240) !important;
  border-radius: 4px;
  -moz-border-radius: 4px;
  background: rgb(240, 240, 240);
}
</style>
