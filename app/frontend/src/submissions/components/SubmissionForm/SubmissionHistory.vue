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
  <form-subsection class="mt-12" title="Activity Reports" :id="id" :hideSave="true">
    <div class="flex">
      <div>
        <p>
          There {{ filteredSubmissions.length !== 1 ? 'are' : 'is' }} {{ filteredSubmissions.length }} activity {{ filteredSubmissions.length !== 1 ? 'reports' : 'report' }} for well {{ $route.params.id }}.
        </p>
        <DataTable :value="filteredSubmissions" ref="submissionHistoryTable" scrollable paginator :rows="submissionsPerPage">
          <template #empty>
            There is currently no submission report history for this well. Scanned copies of paper reports may be available as an attachment.
          </template>
          <Column header="Report">
            <template #body="slotProps">
              <router-link :to="{ name: 'SubmissionDetail', params: { id: $route.params.id, submissionId: slotProps.data.filing_number }}">{{ slotProps.data.well_activity_description }}</router-link>
            </template>
          </Column>
          <Column header="Date Entered">
            <template #body="slotProps">
              <span v-if="slotProps.data.create_date">{{ moment(slotProps.data.create_date, "MMMM Do YYYY [at] LT") }}</span>
            </template>
          </Column>
          <Column field="create_user" header="Entered By"/>
        </DataTable>
      </div>
    </div>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

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
  components: {
    FormSubsection
  },
  data () {
    return {
      submissionStore: null,
      submissionsPerPage: 5,
      submissionsPage: 1,
      submissionsBusy: false,
      submissionsRecordsCount: 0,
      tableHeaders: [
        {
          label: 'Report',
          thStyle: {
            width: '33%'
          }
        },
        {
          label: 'Date Entered',
          thStyle: {
            width: '33%'
          }
        },
        {
          label: 'Entered By',
          thStyle: {
            width: '33%'
          }
        }
      ]
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
  },
  computed: {
    filteredSubmissions () {
      return this.submissionsHistory.filter((i) => {
        return i.well_activity_type !== 'STAFF_EDIT'
      })
    },
    codes () {
      return this.submissionStore.codes
    }
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
