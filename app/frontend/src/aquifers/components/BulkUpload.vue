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

// wellTagNumber = well_tag_number

<template>
  <div>
    <b-card class="container p-1" v-if="userRoles.aquifers.edit">
      <api-error v-if="apiError" :error="apiError"/>

      <b-container>
        <b-row class="border-bottom mb-3 pb-2 pt-2">
          <b-col><h4>Bulk Upload</h4></b-col>
        </b-row>

        <b-alert show v-if="errors.length > 0" variant="danger">
          <ul>
            <li v-for="(error, index) in errors" :key="index">
              {{error}}
            </li>
          </ul>
        </b-alert>
        <b-alert show v-if="showSaveSuccess" variant="success" >
          All wells updated with aquifer correlation
        </b-alert>

        <b-card class="mb-3" title="Instructions" v-if="!file">
          <b-card-text>
            <p>Choose a CSV file below that is the following <strong>exact</strong> format:</p>
            <ol>
              <li>Only two columns</li>
              <li>The first column “A” must be only numeric well tag numbers</li>
              <li>The second column “B” must be only numeric aquifer ids</li>
              <li>The first row must contain “well_tag_number” in column “A”</li>
              <li>The first row must contain “aquifer_id” in column “A”</li>
            </ol>
          </b-card-text>

          <b-form-file
            v-model="file"
            :disabled="isSaving"
            accept="text/csv"
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here..."/>
        </b-card>

        <b-card v-if="hasDataToProcess" title="Data to process" class="mb-3">
          <b-alert show v-if="hasFieldErrors" variant="danger">
            Some aquifer and wells (highlighted in red below) can not be found.
          </b-alert>
          <b-alert show v-if="hasBeenValidated && !noUpdatesToPerform" variant="success">
            All wells and aquifers are valid. Review the changes below and then click "Submit" to really update.
          </b-alert>
          <div v-if="hasBeenValidated && !noUpdatesToPerform">
            <strong>Note:</strong>
            <ol>
              <li><span style="color:orange">orange</span> wells are being updated from a previous aquifer id (in <span style="color:red">red</span>)</li>
              <li><span style="color:green">green</span> wells are new correlations</li>
            </ol>
          </div>
          <b-alert show v-if="noUpdatesToPerform" variant="warning">
            There are no updates to perform. Double check your CSV and try again.
          </b-alert>

          <b-table
            class="correlations"
            :tbody-tr-class="rowClass"
            striped
            hover
            :items="tableData"
            :fields="tableFields">
            <template slot="aquiferId" slot-scope="row">
              <span :class="{ error: isUnknownAquifer(row.item.aquiferId) }">
                {{row.item.aquiferId}}
              </span>
            </template>
            <template slot="oldAquiferId" slot-scope="row">
              <span>
                {{formatOldAquifer(row)}}
              </span>
            </template>
            <template slot="wellTagNumber" slot-scope="row">
              <span :class="{ error: isUnknownWell(row.item.wellTagNumber) }">
                {{row.item.wellTagNumber}}
              </span>
            </template>
          </b-table>
        </b-card>

        <b-button-group>
          <b-button
            v-if="showSubmitButton"
            :disabled="isSaving || !Boolean(file)"
            variant="primary"
            @click="save">
            <b-spinner v-if="isSaving" small label="Loading..."/>
            {{hasBeenValidated ? 'Submit' : 'Validate Data'}}
          </b-button>
          <b-button
            v-if="csvParsedSuccessfully || showSaveSuccess"
            variant="default"
            @click="restart">
            {{showSaveSuccess ? 'Start again' : 'Reset'}}
          </b-button>
        </b-button-group>
      </b-container>
    </b-card>
    <div class="card" v-else-if="!$keycloak.authenticated">
      <div class="card-body">
        <p>Please log in to continue.</p>
      </div>
    </div>
    <div class="card" v-else>
      <div class="card-body">
        <p>You do not have permission to bulk upload aquifer data.</p>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import Papa from 'papaparse'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { mapActions, mapState, mapGetters } from 'vuex'

const BASE_TABLE_FIELDS = [
  {
    key: 'wellTagNumber',
    label: 'Well',
    class: 'well',
    sortable: false
  },
  {
    key: 'aquiferId',
    label: 'New Aquifer',
    sortable: true,
    class: 'aquifer-id text-right pr-4',
    sortDirection: 'desc'
  }
]

const OLD_AQUIFER_FIELD = {
  key: 'oldAquiferId',
  label: 'Old Aquifer',
  sortable: true,
  class: 'old-aquifer-id text-right pr-4'
}

export default {
  data () {
    return {
      errors: [],
      apiError: null,
      file: null,
      fieldErrors: {},
      wells: {},
      wellUpdates: null,
      changes: {},
      csvParsedSuccessfully: false,
      isSaving: false,
      showSaveSuccess: false,
      hasBeenValidated: false
    }
  },
  components: {
    'api-error': APIErrorMessage
  },
  computed: {
    ...mapGetters(['userRoles', 'keycloak']),
    ...mapState('documentState', [
      'upload_files'
    ]),
    unknownAquifers () {
      return (this.fieldErrors || {}).unknownAquifers || []
    },
    unknownWells () {
      return (this.fieldErrors || {}).unknownWells || []
    },
    hasDataToProcess () {
      return Object.keys(this.wells).length > 0
    },
    hasFieldErrors () {
      return Object.keys(this.fieldErrors).length > 0
    },
    tableData () {
      const wells = Object.keys(this.wells)
        .map((wellTagNumber) => {
          const data = {
            aquiferId: this.wells[wellTagNumber],
            wellTagNumber: parseInt(wellTagNumber)
          }
          if (this.wellUpdates !== null) {
            const change = this.wellUpdates[wellTagNumber]
            if (change) {
              switch (change.action) {
                case 'new':
                  data.isNew = true
                  break
                case 'update':
                  data.oldAquiferId = change.existingAquiferId
                  data.isUpdate = true
                  break
                case 'same':
                  data.isSame = true
                  break
                default:
                  console.warn(`Unknown change action of ${change.action}`)
              }
            }
          }
          return data
        })

      wells.sort((a, b) => a.aquiferId - b.aquiferId)

      return wells
    },
    tableFields () {
      if (this.wellUpdates === null) {
        return BASE_TABLE_FIELDS
      }

      const baseTableFieldsCopy = BASE_TABLE_FIELDS.slice()
      baseTableFieldsCopy.splice(1, 0, OLD_AQUIFER_FIELD)
      return baseTableFieldsCopy
    },
    aquifers () {
      const aquifers = {}
      const wellTagNumbers = Object.keys(this.wells)
      wellTagNumbers.forEach((wellTagNumber) => {
        const aquiferId = this.wells[wellTagNumber]
        aquifers[aquiferId] = aquifers[aquiferId] || []
        aquifers[aquiferId].push(parseInt(wellTagNumber))
      })
      return aquifers
    },
    noUpdatesToPerform () {
      if (this.wellUpdates) {
        return Object.values(this.wellUpdates).every((change) => {
          return change.action === 'same'
        })
      }
      return false
    },
    showSubmitButton () {
      if (!this.csvParsedSuccessfully) {
        return false
      } else if (this.hasBeenValidated && this.noUpdatesToPerform) {
        return false
      } else if (this.hasFieldErrors) {
        return false
      }

      return true
    }
  },
  watch: {
    file (newFile) {
      if (newFile) {
        this.reset()
        this.filePicked(newFile)
      }
    }
  },
  methods: {
    ...mapActions('documentState', [
      'uploadFiles',
      'fileUploadSuccess',
      'fileUploadFail'
    ]),
    isInteger (value) {
      return typeof value === 'number' &&
        isFinite(value) &&
        Math.floor(value) === value
    },
    filePicked (file) {
      this.errors = []
      this.showSaveSuccess = false

      this.parseCSV(file)
    },
    parseCSV (file) {
      this.wells = {}

      Papa.parse(file, {
        dynamicTyping: true,
        header: true,
        complete: (results) => {
          const { error, data, meta } = results

          if (error) {
            this.errors.push(error.message)
            return
          }

          if (meta.fields && (meta.fields[0] !== 'well_tag_number' || meta.fields[1] !== 'aquifer_id')) {
            this.errors.push('CSV missing header columns: A "well_tag_number" and B "aquifer_id"')
            return
          }

          const wells = {}

          const cleanedData = data.filter((row) => {
            return row.well_tag_number !== null && row.aquifer_id !== null
          })

          cleanedData.forEach((row) => {
            const len = Object.keys(row).length
            if (len !== 2) {
              this.errors.push(`Skipping row with "${Object.values(row).join(', ')}" as it has ${len} columns when only 2 were expected`)
              return
            }

            const { well_tag_number: wellTagNumber, aquifer_id: aquiferId } = row

            if (!aquiferId || !wellTagNumber) { return }

            if (!this.isInteger(aquiferId)) {
              this.errors.push(`Skipping a non-numeric aquifer id of "${aquiferId}"`)
              return
            }

            if (!this.isInteger(wellTagNumber)) {
              this.errors.push(`Skipping a non-numeric well id "${wellTagNumber}"`)
              return
            }

            if (wellTagNumber in wells) {
              this.errors.push(`Skipping duplicate well ids ${wellTagNumber}`)
            }

            wells[wellTagNumber] = aquiferId
          })

          this.wells = wells

          this.csvParsedSuccessfully = true
        }
      })
    },
    save () {
      this.apiError = null
      const aquiferIds = Object.keys(this.aquifers)
      const data = aquiferIds.map((aquiferId) => {
        return {
          aquiferId: aquiferId,
          wellTagNumbers: this.aquifers[aquiferId]
        }
      })
      this.fieldErrors = {}
      this.isSaving = true
      const options = {}
      if (this.hasBeenValidated) {
        options.params = {
          commit: true
        }
      }
      ApiService.post('aquifers/bulk', data, options)
        .then(this.handleSaveSuccess)
        .catch(this.handleSaveError)
    },
    handleSaveSuccess ({ data }) {
      this.isSaving = false
      if (this.hasBeenValidated) { // Update happened
        this.showSaveSuccess = true
        this.reset()
      } else {
        this.wellUpdates = data
        this.hasBeenValidated = true
      }
    },
    handleSaveError (error) {
      this.isSaving = false
      if (error.response) {
        if (error.response.status === 400) {
          this.fieldErrors = error.response.data
        } else {
          this.apiError = error.response
        }
      } else {
        this.apiError = error.message
      }
    },
    reset () {
      this.errors = []
      this.fieldErrors = {}
      this.wells = {}
      this.wellUpdates = null
      this.isSaving = false
      this.csvParsedSuccessfully = null
      this.hasBeenValidated = false
    },
    restart () {
      this.file = null
      this.showSaveSuccess = false
      this.reset()
    },
    isUnknownAquifer (aquiferId) {
      return this.unknownAquifers.indexOf(aquiferId) !== -1
    },
    isUnknownWell (wellTagNumber) {
      return this.unknownWells.indexOf(wellTagNumber) !== -1
    },
    formatOldAquifer (row) {
      if (row.item.isSame) {
        return row.item.aquiferId
      } else if (row.item.isNew) {
        return '\u2014'
      }
      return row.item.oldAquiferId
    },
    rowClass (item, type) {
      if (!item || type !== 'row') return
      const classes = []

      if (item.isUpdate) {
        classes.push('update')
      } else if (item.isNew) {
        classes.push('new')
      }
      return classes.join(' ')
    }
  }
}
</script>
<style>
ol {
  margin: 0;
  padding: 0 0 0 1.1em;
}
ol li {
  margin: 0.5rem 0;
}
.alert ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
.alert ul li {
  margin: 0;
  padding: 0.5rem;
}
.correlations .error {
  font-weight: bold;
  color: red;
}
.correlations .new {
  font-weight: bold;
  color: green;
}
.correlations .update {
  font-weight: bold;
  color: orange;
}
.correlations .update .old-aquifer-id {
  color: red;
}
</style>
