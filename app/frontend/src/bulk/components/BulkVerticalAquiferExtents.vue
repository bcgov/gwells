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
  <div>
    <b-card class="container p-1" v-if="perms.wellAquiferCorrelation">
      <api-error v-if="apiError" :error="apiError"/>

      <b-container>
        <b-row class="border-bottom mb-3 pb-2 pt-2">
          <b-col><h4>Vertical Aquifer Extents Bulk Upload</h4></b-col>
        </b-row>

        <b-alert show v-if="showSaveSuccess" variant="success" >
          All vertical aquifer extents successfully changed
        </b-alert>

        <b-card v-if="!file" title="Instructions">
          <b-card-text>
            <p>Choose a CSV file below that is the following <strong>exact</strong> format:</p>
            <ol>
              <li>Only four columns</li>
              <li>The first row must contain “well_tag_number” in column “A”, “aquifer_id” in column “B”, “from_depth” in column “C”, “to_depth” in column “D”.</li>
              <li>The first column “A” must be only numeric well tag numbers</li>
              <li>The second column “B” must be only numeric aquifer ids</li>
              <li>The second column “C” must be only numeric values in meters</li>
              <li>The second column “D” must be only numeric values in meters</li>
            </ol>
          </b-card-text>

          <b-form-file
            v-model="file"
            :disabled="isSaving"
            accept="text/csv"
            placeholder="Choose a file or drop it here…"
            drop-placeholder="Drop file here…"/>
        </b-card>

        <b-alert show v-if="showBuildingTable" variant="success" >
          Building table ...
        </b-alert>

        <b-alert show v-if="tooManyCSVRows" variant="danger" >
          The CSV file has too many records ({{numberOfCSVRows}}).
          Performance will be an issue and your bulk upload may not work
          for more than {{maxNumberOfRows}}.
          Please break up the CSV file into smaller files.
        </b-alert>

        <b-card v-if="hasCSVErrors">
          <b-alert show variant="danger" >
            There were problems parsing the CSV file. Below are the list of errors encountered.
          </b-alert>

          <b-table
            v-if="hasCSVErrors"
            class="csv-errors"
            striped
            hover
            :items="csvErrorsTableData"
            :fields="csvErrorTableFields">
          </b-table>
        </b-card>

        <b-card v-if="!hasCSVErrors && hasDataToProcess" title="Data to process">
          <b-alert show v-if="hasBeenValidated && !noUpdatesToPerform" variant="success">
            All {{numVerticalAquiferExtents}} wells and aquifers are valid. Review the changes below and then click “Submit” to really update.
          </b-alert>
          <b-alert show v-if="hasBeenValidated && noUpdatesToPerform" variant="warning">
            There are no updates to perform. Double check your CSV and try again.
          </b-alert>
          <div v-if="hasAPIValidationErrors" id="api-errors">
            <b-alert show variant="danger">
              The wells and aquifers listed below can not be found in the GWELLS database.
            </b-alert>

            <b-table
              class="errors"
              :tbody-tr-class="rowClass"
              striped
              hover
              :items="errorsTableData"
              :fields="errorTableFields">
              <template slot="aquiferId" slot-scope="row">
                <span :class="{ error: isUnknownAquifer(row.item.aquiferId) }">
                  {{row.item.aquiferId}}
                </span>
              </template>
              <template slot="wellTagNumber" slot-scope="row">
                <span :class="{ error: isUnknownWell(row.item.wellTagNumber) }">
                  {{row.item.wellTagNumber}}
                </span>
              </template>
            </b-table>
          </div>

          <div v-if="!hasAPIValidationErrors">
            <div v-if="hasBeenValidated && !noUpdatesToPerform">
              <strong>Note:</strong>
              <ol>
                <li><span class="change-color">orange</span> wells are being updated from a previous aquifer id (in <span class="remove-color">red</span>)</li>
                <li><span class="new-color">green</span> wells are new correlations</li>
                <li><span class="no-change-color">un-coloured</span> wells have no changes to their aquifer correlations</li>
              </ol>
            </div>

            <div id="summary">
              <strong>Summary:</strong>
              <ul>
                <li v-if="numVerticalAquiferExtentsToUpdate > 0">{{numVerticalAquiferExtentsToUpdate}} to be changed</li>
                <li v-if="numVerticalAquiferExtentsToAdd > 0">{{numVerticalAquiferExtentsToAdd}} to add</li>
                <li v-if="numVerticalAquiferExtentsUnchanged > 0">{{numVerticalAquiferExtentsUnchanged}} unchanged</li>
              </ul>
            </div>

            <b-table
              id="vertical-aquifer-extents"
              :tbody-tr-class="rowClass"
              striped
              hover
              :items="tableData"
              :fields="tableFields">
              <template slot="fromDepth" slot-scope="row">
                {{row.item.fromDepth.toFixed(2)}}
              </template>
              <template slot="toDepth" slot-scope="row">
                {{row.item.toDepth === null ? '\u2014' : row.item.toDepth.toFixed(2)}}
              </template>
            </b-table>
          </div>
        </b-card>

        <b-button-group class="mt-3">
          <b-button
            v-if="showSubmitButton"
            :disabled="isSaveButtonDisabled"
            variant="primary"
            @click="save">
            <b-spinner v-if="isSaving" small label="Loading…"/>
            {{hasBeenValidated ? 'Submit' : 'Validate Data'}}
          </b-button>
          <b-button
            v-if="showResetButton"
            variant="default"
            @click="restart">
            {{showSaveSuccess ? 'Upload another CSV' : 'Reset'}}
          </b-button>
        </b-button-group>
      </b-container>
    </b-card>
    <div class="card container" v-else-if="!$keycloak.authenticated">
      <div class="card-body">
        <p>Please log in to continue.</p>
      </div>
    </div>
    <div class="card container" v-else>
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
import { mapGetters } from 'vuex'

const MAX_NUMBER_OF_ROWS = 4000

const BASE_TABLE_FIELDS = [
  {
    key: 'rowNum',
    label: 'Row Number',
    class: 'row-num',
    sortable: true,
    sortDirection: 'desc'
  },
  {
    key: 'wellTagNumber',
    label: 'Well Tag Number',
    class: 'well',
    sortable: true
  },
  {
    key: 'aquiferId',
    label: 'Aquifer ID',
    class: 'aquifer-id',
    sortable: true
  },
  {
    key: 'fromDepth',
    label: 'From Depth',
    class: 'from-depth'
  },
  {
    key: 'toDepth',
    label: 'To Depth',
    class: 'to-depth text-right pr-4'
  }
]

export default {
  data () {
    return {
      csvErrors: [],
      apiError: null,
      file: null,
      apiValidationErrors: {},
      verticalAquiferExtents: [],
      wellUpdates: null,
      isSaving: false,
      showSaveSuccess: false,
      hasBeenValidated: false,
      tooManyCSVRows: false,
      numberOfCSVRows: null,
      maxNumberOfRows: MAX_NUMBER_OF_ROWS,
      tableFields: BASE_TABLE_FIELDS,
      showBuildingTable: false,
      csvErrorTableFields: [
        {
          key: 'rowNum',
          label: 'Row Number',
          class: 'row-number',
          sortable: false
        },
        {
          key: 'errorMessage',
          label: 'Error',
          class: 'error',
          sortable: false
        }
      ],
      errorTableFields: [
        {
          key: 'wellTagNumber',
          label: 'Well Tag Number',
          class: 'well',
          sortable: false
        },
        {
          key: 'aquiferId',
          label: 'Aquifer ID',
          class: 'aquifer-id text-right pr-4',
          sortable: false
        }
      ]
    }
  },
  components: {
    'api-error': APIErrorMessage
  },
  computed: {
    ...mapGetters(['userRoles', 'keycloak']),
    perms () {
      return this.userRoles.bulk || {}
    },
    unknownAquifers () {
      return (this.apiValidationErrors || {}).unknownAquifers || []
    },
    unknownWells () {
      return (this.apiValidationErrors || {}).unknownWells || []
    },
    hasCSVErrors () {
      return this.csvErrors.length > 0
    },
    hasDataToProcess () {
      return this.verticalAquiferExtents.length > 0
    },
    hasAPIValidationErrors () {
      return Object.keys(this.apiValidationErrors).length > 0
    },
    csvErrorsTableData () {
      return this.csvErrors
    },
    errorsTableData () {
      const data = this.verticalAquiferExtents
        .filter((vae) => {
          const wtn = vae.wellTagNumber
          const aquiferId = vae.aquiferId
          return this.unknownWells.indexOf(wtn) >= 0 || this.unknownAquifers.indexOf(aquiferId) >= 0
        })

      return data
    },
    numVerticalAquiferExtents () {
      return this.verticalAquiferExtents.length
    },
    listOfChanges () {
      return this.wellUpdates !== null ? Object.values(this.wellUpdates) : []
    },
    numVerticalAquiferExtentsToAdd () {
      return this.listOfChanges.filter((change) => change.action === 'new').length
    },
    numVerticalAquiferExtentsToUpdate () {
      return this.listOfChanges.filter((change) => change.action === 'update').length
    },
    numVerticalAquiferExtentsUnchanged () {
      return this.listOfChanges.filter((change) => change.action === 'same').length
    },
    tableData () {
      const vae = this.verticalAquiferExtents
        .map((val) => {
          const data = { ...val }
          if (this.wellUpdates !== null) {
            const change = this.wellUpdates[val.wellTagNumber]
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

      return vae
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
      if (this.hasCSVErrors) {
        return false
      } else if (this.hasBeenValidated && this.noUpdatesToPerform) {
        return false
      } else if (this.hasAPIValidationErrors) {
        return false
      } else if (this.showSaveSuccess) {
        return false
      }

      return true
    },
    showResetButton () {
      if (this.hasCSVErrors) {
        return true
      } else if (this.showSaveSuccess) {
        return true
      } else if (this.hasDataToProcess) {
        return true
      }
      return false
    },
    isSaveButtonDisabled () {
      if (this.isSaving) {
        return true
      } else if (!this.file) {
        return true
      }

      return false
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
    isBlank (value) {
      return value === '' || value === null || value === undefined
    },
    isInteger (value) {
      return typeof value === 'number' &&
        isFinite(value) &&
        Math.floor(value) === value
    },
    isDecimal (value) {
      return typeof value === 'number' &&
        value !== null &&
        isFinite(value)
    },
    filePicked (file) {
      this.csvErrors = []
      this.showSaveSuccess = false

      this.parseCSV(file)
    },
    logCSVError (rowNum, errorMessage) {
      this.csvErrors.push({
        rowNum,
        errorMessage
      })
      return false
    },
    parseCSV (file) {
      this.verticalAquiferExtents = []

      Papa.parse(file, {
        dynamicTyping: true,
        header: true,
        complete: (results) => {
          const { error, data, meta } = results

          if (error) {
            this.logCSVError(null, error.message)
            return
          }

          if (meta.fields) {
            if (meta.fields[0] !== 'well_tag_number') {
              this.logCSVError(null, 'CSV is missing header column A: "well_tag_number"')
              return
            } else if (meta.fields[1] !== 'aquifer_id') {
              this.logCSVError(null, 'CSV is missing header column B: "aquifer_id"')
              return
            } else if (meta.fields[2] !== 'from_depth') {
              this.logCSVError(null, 'CSV is missing header column C: "from_depth"')
              return
            } else if (meta.fields[3] !== 'to_depth') {
              this.logCSVError(null, 'CSV is missing header column D: "to_depth"')
              return
            }
          }

          if (data.length > MAX_NUMBER_OF_ROWS) {
            this.tooManyCSVRows = true
          }

          this.numberOfCSVRows = data.length

          const cleanedData = []

          data.forEach((row, i) => {
            // skip the last row in the CSV that is usually empty
            if (row.well_tag_number === null && row.aquifer_id === undefined && row.from_depth === undefined && row.to_depth === undefined) {
              return
            }

            const rowNumLabel = i + 2 // add one for the skipped csv header row

            const len = Object.keys(row).length
            if (len !== 4) {
              this.logCSVError(rowNumLabel, `Skipping row with "${Object.values(row).join(', ')}" as it has ${len} columns when only 2 were expected`)
              return
            }

            const {
              well_tag_number: wellTagNumber,
              aquifer_id: aquiferId,
              from_depth: fromDepth,
              to_depth: toDepth
            } = row

            if (this.validateCSVRow(wellTagNumber, aquiferId, fromDepth, toDepth, rowNumLabel)) {
              cleanedData.push({
                rowNum: rowNumLabel,
                wellTagNumber,
                aquiferId,
                fromDepth: parseFloat(fromDepth),
                toDepth: toDepth !== null ? parseFloat(toDepth) : toDepth
              })
            }
          })

          if (this.csvErrors.length === 0) {
            this.showBuildingTable = true
            setTimeout(() => { // wait a bit so the "building table" message can be rendered
              this.verticalAquiferExtents = cleanedData
              this.showBuildingTable = false
            }, 50)
          }
        }
      })
    },
    validateCSVRow (wellTagNumber, aquiferId, fromDepth, toDepth, rowNumLabel) {
      if (this.isBlank(wellTagNumber)) {
        return this.logCSVError(rowNumLabel, `well_tag_number is required`)
      } else if (!this.isInteger(wellTagNumber)) {
        return this.logCSVError(rowNumLabel, `well_tag_number "${wellTagNumber}" is not a number`)
      } else if (this.isBlank(aquiferId)) {
        return this.logCSVError(rowNumLabel, `aquifer_id is required`)
      } else if (!this.isInteger(aquiferId)) {
        return this.logCSVError(rowNumLabel, `aquifer_id "${aquiferId}" is not a number`)
      } else if (this.isBlank(fromDepth)) {
        return this.logCSVError(rowNumLabel, `from_depth is required`)
      } else if (!this.isDecimal(fromDepth)) {
        return this.logCSVError(rowNumLabel, `from_depth "${fromDepth}" is not a number`)
      } else if (fromDepth < 0) {
        return this.logCSVError(rowNumLabel, `from_depth "${fromDepth}" must not be a negative number`)
      } else if (!this.isBlank(toDepth) && !this.isDecimal(toDepth)) {
        return this.logCSVError(rowNumLabel, `to_depth "${toDepth}" is not a number`)
      } else if (toDepth < 0) {
        return this.logCSVError(rowNumLabel, `to_depth "${toDepth}" must not be a negative number`)
      }
      return true
    },
    save () {
      const data = this.verticalAquiferExtents
      this.apiError = null
      this.apiValidationErrors = {}
      this.isSaving = true
      const options = {}
      if (this.hasBeenValidated) {
        options.params = {
          commit: true
        }
      }
      ApiService.post('bulk/vertical-aquifer-extents', data, options)
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
          this.apiValidationErrors = error.response.data
        } else {
          this.apiError = error.response
        }
      } else {
        this.apiError = error.message
      }
    },
    reset () {
      this.tooManyCSVRows = false
      this.numberOfCSVRows = null
      this.csvErrors = []
      this.apiValidationErrors = {}
      this.verticalAquiferExtents = []
      this.wellUpdates = null
      this.isSaving = false
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
<style lang="scss">
.change-color {
  font-weight: bold;
  color: #eca013;
}

.remove-color {
  font-weight: bold;
  color: #ec3838;
}

.new-color {
  font-weight: bold;
  color: #057513;
}

.no-change-color {
  color: inherit;
}

ol {
  margin: 0;
  padding: 0 0 0 1.1em;

  li {
    margin: 0.5rem 0;
  }
}

.alert ul {
  margin: 0;
  padding: 0;
  list-style: none;

  li {
    margin: 0;
    padding: 0.5rem;
  }
}
.errors .error {
  font-weight: bold;
  color: red;
}

#summary {
  ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  li {
    list-style: none;
    margin: 0;
    padding: 0;
    display: inline;

    &::after {
      content: ", ";
    }

    &:last-child {
      &::before {
        content: " and ";
      }

      &::after {
        content: ".";
      }
    }
  }
}

.correlations {
  .new {
    @extend .new-color;
  }

  .update {
    @extend .change-color;

    .old-aquifer-id {
      @extend .remove-color;
    }
  }
}
</style>
