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
  <div id="bulk-well-aquifer-correlation-screen">
    <div class="container mb-4 !px-0">
      <Breadcrumb class="p-0" :model="breadcrumbs">
        <template #item="{ item }">
          <router-link v-if="!item.active" :to="item.route">{{ item.label }}</router-link>
          <span v-else>{{ item.label }}</span>
        </template>
      </Breadcrumb>
    </div>
    <Card class="mx-8" v-if="perms.wellAquiferCorrelation">
      <template #content>
        <api-error v-if="apiError" :error="apiError"/>

        <div>
          <h4>Well Aquifer Correlation Bulk Upload</h4>

          <Message
            class="my-3"
            severity="info"
            v-if="showSaveSuccess"
            :key="`survey ${index}`">
            <p class="m-0">
              All wells updated with aquifer correlation
            </p>
          </Message>

          <div v-if="!file" title="Instructions">

            <div>
              <p>Choose a CSV file below that is the following <strong>exact</strong> format:</p>
              <ul class="list-disc my-4 ml-8">
                <li>Only two columns</li>
                <li>The first column “A” must be only numeric well tag numbers</li>
                <li>The second column “B” must be only numeric aquifer ids</li>
                <li>The first row must contain “well_tag_number” in column “A”</li>
                <li>The first row must contain “aquifer_id” in column “B”</li>
              </ul>
            </div>

            <div class="card flex flex-wrap gap-6 items-center justify-between">
              <FileUpload accept="text/csv" :disabled="isSaving" ref="file" mode="basic" name="fileUpload" customUpload @select="onFileSelect" />
            </div>
          </div>

          <Message
            class="my-3"
            severity="error"
            v-if="tooManyCSVRows"
            :key="`survey ${index}`">
            <p class="m-0">
              The CSV file has too many records ({{numberOfCSVRows}}).
              Performance will be an issue and your bulk upload may not work
              for more than {{maxNumberOfRows}}.
              Please break up the CSV file into smaller files.
            </p>
          </Message>

          <div v-if="hasCSVErrors">
            <Message
              class="my-3"
              severity="error"
              v-if="tooManyCSVRows"
              :key="`survey ${index}`">
              <p class="m-0">
                There were problems parsing the CSV file. Below are the list of errors encountered.
              </p>
            </Message>

            <DataTable
              v-if="hasCSVErrors"
              :value="csvErrorsTableData"
              tableStyle="min-width: 50rem"
              stripedRows
            >
              <Column field="rowNum" header="Row Number"></Column>
              <Column field="errorMessage" header="Error"></Column>
            </DataTable>
          </div>

          <div v-if="!hasCSVErrors && hasDataToProcess" title="Data to process">
            <Message
              class="my-3"
              severity="success"
              v-if="hasBeenValidated && !noUpdatesToPerform && !hasAPIValidationWarnings"
            >
              <p class="m-0">
                All {{numWells}} wells and aquifers are valid. Review the changes below and then click “Submit” to perform update.
              </p>
            </Message>
            <Message
              class="my-3"
              severity="warn"
              v-if="hasBeenValidated && !noUpdatesToPerform && hasAPIValidationWarnings"
            >
              <p class="m-0">
                All {{numWells}} wells and aquifers are valid, but warnings exist. Review changes below and verify warnings. Click “Ignore warnings and submit” to perform update.
              </p>
            </Message>
            <Message
              class="my-3"
              severity="warn"
              v-if="hasBeenValidated && noUpdatesToPerform" variant="warning"
            >
              <p class="m-0">
                There are no updates to perform. Verify your CSV and try again.
              </p>
            </Message>
            <div v-if="hasAPIValidationErrors" id="api-errors">
              <Message
                class="my-3"
                severity="error"
                v-if="hasCSVErrors"
              >
                <p class="m-0">
                  The wells and aquifers listed below can not be found in the GWELLS database.
                </p>
              </Message>

              <DataTable
                v-if="hasCSVErrors"
                :value="errorsTableData"
                stripedRows
              >
                <Column field="aquiferId" header="Aquifer ID">
                  <template #body="slotProps">
                    <span :class="{ error: isUnknownAquifer(slotProps.data.aquiferId) }">
                      {{slotProps.data.aquiferId}}
                    </span>
                  </template>
                </Column>
                <Column field="wellTagNumber" header="Well Tag Number">
                  <template #body="slotProps">
                    <span :class="{ error: isUnknownWell(slotProps.data.wellTagNumber) }">
                      {{slotProps.data.wellTagNumber}}
                    </span>
                  </template>
                </Column>
              </DataTable>
            </div>

            <div v-else>
              <div v-if="hasBeenValidated && !noUpdatesToPerform">
                <strong>Note:</strong>
                <ul class="list-disc my-4 ml-8">
                  <li><span class="change-color">orange</span> wells are being updated from a previous aquifer id (in <span class="remove-color">red</span>)</li>
                  <li><span class="new-color">green</span> wells are new correlations</li>
                  <li><span class="no-change-color">un-coloured</span> wells have no changes to their aquifer correlations</li>
                </ul>
              </div>

              <div id="summary">
                <strong>Summary:</strong>
                <ul class="list-disc my-4 ml-8">
                  <li v-if="numWellsToUpdate > 0">{{numWellsToUpdate}} to be changed</li>
                  <li v-if="numWellsToAdd > 0">{{numWellsToAdd}} to add</li>
                  <li v-if="numWellsUnchanged > 0">{{numWellsUnchanged}} unchanged</li>
                </ul>
              </div>

              <DataTable
                :value="tableData"
                stripedRows
              >
                <Column field="aquiferId" header="Aquifer ID">
                  <template #body="slotProps">
                    <span>
                      {{slotProps.data.aquiferId}}
                    </span>
                  </template>
                </Column>
                <Column field="wellTagNumber" header="Well Tag Number">
                  <template #body="slotProps">
                    <span>
                      {{slotProps.data.wellTagNumber}}
                    </span>
                  </template>
                </Column>
                <Column field="warnings" header="Warnings">
                  <template #body="slotProps">
                    <ul v-if="slotProps.data.warnings.length > 0">
                      <li v-for="(warning, index) in slotProps.data.warnings" :key="index">
                        {{ warning }}
                      </li>
                    </ul>
                  </template>
                </Column>
              </DataTable>
            </div>
          </div>

          <div class="mt-4">
            <Button
              v-if="showSubmitButton"
              :disabled="isSaving || !Boolean(file)"
              @click="save"
              class="mr-2"
            >
              {{saveButtonLabel}}
            </Button>
            <Button
              v-if="showResetButton"
              severity="secondary"
              @click="restart"
            >
              {{showSaveSuccess ? 'Upload another CSV' : 'Reset'}}
            </Button>
          </div>
        </div>
      </template>
    </Card>
    <div class="card container" v-else-if="!commonStore.keycloak.authenticated">
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
import { useCommonStore } from '@/stores/common.js'
import Papa from 'papaparse'

import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'

import { AQUIFER_ID_FOR_UNCORRELATED_WELLS } from '@/common/constants.js'

const MAX_NUMBER_OF_ROWS = 4000

const BASE_TABLE_FIELDS = [
  {
    key: 'wellTagNumber',
    label: 'Well Tag Number',
    class: 'well',
    sortable: false
  },
  {
    key: 'aquiferId',
    label: 'New Aquifer ID',
    class: 'aquifer-id text-right',
    sortable: false
  }
]

const OLD_AQUIFER_FIELD = {
  key: 'oldAquiferId',
  label: 'Old Aquifer ID',
  sortable: true,
  class: 'old-aquifer-id text-right pr-6'
}

const WARNINGS_FIELD = {
  key: 'warnings',
  label: 'Warnings',
  sortable: true,
  class: 'warnings pr-6'
}

export default {
  data () {
    return {
      csvErrors: [],
      apiError: null,
      file: null,
      apiValidationErrors: {},
      wells: {},
      wellUpdates: null,
      isSaving: false,
      showSaveSuccess: false,
      hasBeenValidated: false,
      tooManyCSVRows: false,
      numberOfCSVRows: null,
      maxNumberOfRows: MAX_NUMBER_OF_ROWS,
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
          class: 'aquifer-id text-right pr-6',
          sortable: false
        }
      ],
      breadcrumbs: [
        {
          label: 'Bulk Upload',
          route: { name: 'bulk-home' }
        },
        {
          label: 'Well Aquifer Correlation Bulk Upload',
          active: true
        }
      ]
    }
  },
  components: {
    'api-error': APIErrorMessage
  },
  computed: {
    commonStore () { return useCommonStore() },
    perms () {
      return this.commonStore.userRoles.bulk || {}
    },
    unknownAquifers () {
      return (this.apiValidationErrors || {}).unknownAquifers || []
    },
    unknownWells () {
      return (this.apiValidationErrors || {}).unknownWells || []
    },
    unpublishedAquifers () {
      return (this.apiValidationErrors || {}).unpublishedAquifers || []
    },
    retiredAquifers () {
      return (this.apiValidationErrors || {}).retiredAquifers || []
    },
    unpublishedWells () {
      return (this.apiValidationErrors || {}).unpublishedWells || []
    },
    wellsOutsideAquifer () {
      return (this.apiValidationErrors || {}).wellsNotInAquifer || {}
    },
    aquifersWithoutGeometry () {
      return (this.apiValidationErrors || {}).aquiferHasNoGeom || []
    },
    hasCSVErrors () {
      return this.csvErrors.length > 0
    },
    hasDataToProcess () {
      return Object.keys(this.wells).length > 0
    },
    hasAPIValidationErrors () {
      return this.unknownWells.length > 0 || this.unknownAquifers.length > 0
    },
    hasAPIValidationWarnings () {
      return (
        this.unpublishedAquifers.length > 0 ||
        this.retiredAquifers.length > 0 ||
        this.unpublishedWells.length > 0 ||
        Object.keys(this.wellsOutsideAquifer).length > 0 ||
        this.aquifersWithoutGeometry.length > 0
      )
    },
    csvErrorsTableData () {
      return this.csvErrors
    },
    errorsTableData () {
      const wells = Object.keys(this.wells)
        .filter((wellTagNumber) => {
          const wtn = parseInt(wellTagNumber)
          const aquiferId = this.wells[wellTagNumber]
          return this.unknownWells.indexOf(wtn) >= 0 || this.unknownAquifers.indexOf(aquiferId) >= 0
        })
        .map((wellTagNumber) => {
          return {
            aquiferId: this.wells[wellTagNumber],
            wellTagNumber: parseInt(wellTagNumber)
          }
        })

      return wells
    },
    numWells () {
      return Object.keys(this.wells).length
    },
    listOfChanges () {
      return this.wellUpdates !== null ? Object.values(this.wellUpdates) : []
    },
    numWellsToAdd () {
      return this.listOfChanges.filter((change) => change.action === 'new').length
    },
    numWellsToUpdate () {
      return this.listOfChanges.filter((change) => change.action === 'update').length
    },
    numWellsUnchanged () {
      return this.listOfChanges.filter((change) => change.action === 'same').length
    },
    tableData () {
      const wells = Object.keys(this.wells)
        .map((wellTagNumber) => {
          wellTagNumber = parseInt(wellTagNumber, 10)
          const warnings = []
          const aquiferId = this.wells[wellTagNumber]
          const data = {
            aquiferId,
            wellTagNumber,
            warnings
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

            if (this.unpublishedAquifers.indexOf(aquiferId) !== -1) {
              warnings.push('Aquifer is unpublished')
            }

            if (this.retiredAquifers.indexOf(aquiferId) !== -1) {
              warnings.push('Aquifer is retired')
            }

            if (this.aquifersWithoutGeometry.indexOf(aquiferId) !== -1) {
              warnings.push('Aquifer has no geometry / shapefile')
            }

            if (aquiferId === AQUIFER_ID_FOR_UNCORRELATED_WELLS) {
              warnings.push('This aquifer number is a placeholder for tracking wells that can not be correlated to a mapped aquifer unit and does not have an associated spatial extent.')
            }

            if (this.unpublishedWells.indexOf(wellTagNumber) !== -1) {
              warnings.push('Well is unpublished')
            }

            if (this.wellsOutsideAquifer[wellTagNumber]) {
              const distance = this.wellsOutsideAquifer[wellTagNumber].distance
              warnings.push(`Well is located ~${distance.toFixed(0)}m outside aquifer`)
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

      if (this.hasAPIValidationWarnings) {
        baseTableFieldsCopy.push(WARNINGS_FIELD)
      }

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
    saveButtonLabel () {
      if (!this.hasBeenValidated) {
        return 'Validate data'
      } else if (this.hasAPIValidationWarnings) {
        return 'Ignore warnings and submit'
      }

      return 'Submit'
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
    onFileSelect (event) {
      const file = event.files[0]
      this.file = file
    },
    isInteger (value) {
      return typeof value === 'number' &&
        isFinite(value) &&
        Math.floor(value) === value
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
    },
    parseCSV (file) {
      this.wells = {}

      Papa.parse(file, {
        dynamicTyping: true,
        header: true,
        complete: (results) => {
          const { error, data, meta } = results

          if (error) {
            this.logCSVError(null, error.message)
            return
          }

          if (meta.fields && (meta.fields[0] !== 'well_tag_number' || meta.fields[1] !== 'aquifer_id')) {
            this.logCSVError(null, 'CSV missing header columns: A "well_tag_number" and B "aquifer_id"')
            return
          }

          if (data.length > MAX_NUMBER_OF_ROWS) {
            this.tooManyCSVRows = true
          }

          this.numberOfCSVRows = data.length
          const wells = {}

          data.forEach((row, rowNum) => {
            // skip the last row in the CSV that is usually empty
            if (row.well_tag_number === null && row.aquifer_id === undefined) {
              return
            }

            rowNum += 2 // add one for the skipped csv header row

            const len = Object.keys(row).length
            if (len !== 2) {
              this.logCSVError(rowNum, `Skipping row with "${Object.values(row).join(', ')}" as it has ${len} columns when only 2 were expected`)
              return
            }

            const { well_tag_number: wellTagNumber, aquifer_id: aquiferId } = row

            if (!aquiferId || !wellTagNumber) { return }

            if (!this.isInteger(aquiferId)) {
              this.logCSVError(rowNum, `Skipping a non-numeric aquifer id of "${aquiferId}"`)
              return
            }

            if (!this.isInteger(wellTagNumber)) {
              this.logCSVError(rowNum, `Skipping a non-numeric well id "${wellTagNumber}"`)
              return
            }

            if (wellTagNumber in wells) {
              this.logCSVError(rowNum, `Skipping duplicate well ids ${wellTagNumber}`)
            }

            wells[wellTagNumber] = aquiferId
          })

          if (this.csvErrors.length === 0) {
            this.wells = wells
          }
        }
      })
    },
    save () {
      this.apiError = null
      const aquiferIds = Object.keys(this.aquifers)
      const data = aquiferIds.map((aquiferId) => {
        return {
          aquiferId: parseInt(aquiferId),
          wellTagNumbers: this.aquifers[aquiferId]
        }
      })
      this.apiValidationErrors = {}
      this.isSaving = true
      const options = {}
      if (this.hasBeenValidated) {
        options.params = {
          commit: true
        }
      }
      ApiService.post('bulk/well-aquifer-correlation', data, options)
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
          this.wellUpdates = error.response.data.changes

          if (!this.hasAPIValidationErrors) {
            this.hasBeenValidated = true
          }
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
      this.wells = {}
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
#bulk-well-aquifer-correlation-screen {
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

      &:not(:only-child)::after {
        content: ", ";
      }

      &:last-child:not(:first-child) {
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
    td {
      vertical-align: middle;
    }

    .new td:not(.warnings) {
      @extend .new-color;
    }

    .update td:not(.warnings) {
      @extend .change-color;

      &.old-aquifer-id {
        @extend .remove-color;
      }
    }

    .warnings {
      ul {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      li {
        margin: 2px 0;
        padding: 0;
      }
    }
  }
}
</style>
