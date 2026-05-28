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
  <div id="bulk-vertical-aquifer-extents-screen">
    <div class="container mb-4 !px-0">
      <Breadcrumb class="p-0" :model="breadcrumbs">
        <template #item="{ item }">
          <router-link v-if="!item.active" :to="item.route">{{ item.label }}</router-link>
          <span v-else>{{ item.label }}</span>
        </template>
      </Breadcrumb>
    </div>
    <div class="container p-1" v-if="perms.verticalAquiferExtents">
      <api-error v-if="apiError" :error="apiError"/>

      <div class="border-bottom mb-4 pb-2 pt-2">
        <h3>Aquifer Documents Bulk Upload</h3>
      </div>
      <div class="w-full border-gray-300 border-1 border-solid h-0 mb-5" >&nbsp;</div>
      <Message
        v-if="showSaveSuccess"
        class="my-3"
        severity="success"
      >
        All documents uploaded for aquifers.
      </Message>

      <Card v-if="!file" id="instructions">
        <template #header>
          <h3 class="pt-4 px-4">Instructions</h3>
        </template>
        <template #content>
          <div class="p-0 mb-4">
            <p>
              Please note that the data in the CSV must be for <strong>new</strong> vertical aquifer
              extents.
            </p>
            <p>
              If you want to modify existing vertical aquifer extents you will need to first find
              your well and edit it. At the bottom of the well edit screen is a table which shows
              the existing vertical aquifer extents. Click the “Edit” button to load a form where
              you can alter the information.
            </p>
            <p>Choose a CSV file below that is the following <strong>exact</strong> format:</p>
            <ol>
              <li>Only four columns</li>
              <li>
                The first column “A”
                <ol type="a">
                  <li>have “well_tag_number” in row one</li>
                  <li>only contain numeric well tag numbers</li>
                </ol>
              </li>
              <li>
                The second column “B”
                <ol type="a">
                  <li>have “aquifer_id” in row one</li>
                  <li>only contain numeric aquifer IDs</li>
                </ol>
              </li>
              <li>
                The third column “C”
                <ol type="a">
                  <li>have “from_depth” in row one</li>
                  <li>only contain numeric values in metres</li>
                </ol>
              </li>
              <li>
                The fourth column “D”
                <ol type="a">
                  <li>have “to_depth” in row one</li>
                  <li>only contain numeric values in metres</li>
                </ol>
              </li>
            </ol>
          </div>
          <FileUpload
            v-model="file"
            name="fileUpload"
            mode="basic"
            :showUploadButton="false"
            :showCancelButton="false"
            :disabled="isSaving"
            @select="filePicked($event.files[0])"
            class="items-center"
          />
        </template>
      </Card>

      <Message
        v-if="showBuildingTable"
        class="my-3"
        severity="success"
      >
        Building table ...
      </Message>

      <Message
        v-if="tooManyCSVRows"
        class="my-3"
        severity="error"
      >
        <p class="m-0">
          The CSV file has too many records ({{numberOfCSVRows}}).
          Performance will be an issue and your bulk upload may not work
          for more than {{maxNumberOfRows}}.
          Please break up the CSV file into smaller files.
        </p>
      </Message>

      <Card v-if="hasCSVErrors">
        <template #content>
          <Message
            v-if="showBuildingTable"
            class="my-3"
            severity="error"
          >
            There were problems parsing the CSV file. Below are the list of errors encountered.
          </Message>

          <DataTable
            :value="csvErrorsTableData"
            stripedRows
            class="mb-4"
          >
            <Column field="rowNum" header="Row"></Column>
            <Column field="errorMessage" header="Error"></Column>
          </DataTable>
        </template>
      </Card>

      <div v-if="!hasCSVErrors && hasDataToProcess">
        <h4 class="mb-4">Data to process</h4>
        <Message
          class="my-3"
          severity="success"
        >
          All {{numVerticalAquiferExtents}} vertical aquifer extents are valid. Review the changes below and then click “Submit” to create {{numVerticalAquiferExtents}} records.
        </Message>
        <div v-if="hasUnknownWellsOrAquifers" id="unknown-wells-or-aquifers">
          <Message
            class="my-3"
            severity="error"
          >
            The wells and aquifers listed below can not be found in the GWELLS database.
          </Message>

          <DataTable
            class="errors"
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
          <Message
            v-if="hasConflicts"
            class="my-3"
            severity="error"
          >
            <div>The CSV data conflits with existing vertical aquifer extents in the GWELLS database.</div>
            <div>You can resolve the conflicts by either:</div>
            <ol>
              <li>Editing the CSV and re-uploading it</li>
              <li>Click the well tag numbers below to edit the existing data</li>
            </ol>
          </Message>

          <!-- // One table showing no conflicts -->
          <!-- // Table below this one showing conflicts -->
          <DataTable
            v-if="!hasConflicts"
            id="vertical-aquifer-extents"
            :value="tableData"
            stripedRows
          >
            <Column field="rowNum" header="Row Number">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.rowNum}}
                </span>
              </template>
            </Column>
            <Column field="wellTagNumber" header="Well Tag Number">
              <template #body="slotProps">
                <router-link :to="{ name: 'well-aquifers', params: {wellTagNumber: slotProps.data.wellTagNumber} }" target="_blank">
                  {{slotProps.data.wellTagNumber}}
                </router-link>
              </template>
            </Column>
            <Column field="aquiferId" header="Aquifer ID">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.aquiferId}}
                </span>
              </template>
            </Column>
            <Column field="fromDepth" header="From Depth">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.fromDepth.toFixed(2)}}
                </span>
              </template>
            </Column>
            <Column field="toDepth" header="To Depth">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.toDepth === null ? '\u2014' : slotProps.data.toDepth.toFixed(2)}}
                </span>
              </template>
            </Column>
          </DataTable>
          <DataTable
            v-if="hasConflicts"
            id="vertical-aquifer-extents"
            :value="tableData"
            stripedRows
          >
            <Column field="rowNum" header="Row Number">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.rowNum}}
                </span>
              </template>
            </Column>
            <Column field="wellTagNumber" header="Well Tag Number">
              <template #body="slotProps">
                <router-link :to="{ name: 'well-aquifers', params: {wellTagNumber: slotProps.data.wellTagNumber} }" target="_blank">
                  {{slotProps.data.wellTagNumber}}
                </router-link>
              </template>
            </Column>
            <Column field="aquiferId" header="Aquifer ID">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.aquiferId}}
                </span>
              </template>
            </Column>
            <Column field="fromDepth" header="From Depth">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.fromDepth.toFixed(2)}}
                </span>
              </template>
            </Column>
            <Column field="toDepth" header="To Depth">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.toDepth === null ? '\u2014' : slotProps.data.toDepth.toFixed(2)}}
                </span>
              </template>
            </Column>
            <Column field="conflictMessage" header="Error">
              <template #body="slotProps">
                <span>
                  {{slotProps.data.conflictMessage}}
                </span>
              </template>
            </Column>
          </DataTable>
        </div>
      </div>

      <div class="mt-4">
        <Button
          v-if="showSubmitButton"
          class="mr-4"
          :disabled="isSaveButtonDisabled"
          @click="save">
          {{submitButtonLabel}}
        </Button>
        <Button
          v-if="showResetButton"
          severity="secondary"
          @click="restart">
          {{showSaveSuccess ? 'Upload another CSV' : 'Reset'}}
        </Button>
      </div>
    </div>
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
import ApiService from '@/common/services/ApiService.js'
import Papa from 'papaparse'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import { useCommonStore } from '@/stores/common.js'

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
    class: 'to-depth text-right pr-6'
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
      isSaving: false,
      showSaveSuccess: false,
      hasBeenValidated: false,
      tooManyCSVRows: false,
      numberOfCSVRows: null,
      maxNumberOfRows: MAX_NUMBER_OF_ROWS,
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
          class: 'aquifer-id',
          sortable: false
        }
      ],
      breadcrumbs: [
        {
          label: 'Bulk Upload',
          route: { name: 'bulk-home' }
        },
        {
          label: 'Vertical Aquifer Extents Bulk Upload',
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
    hasCSVErrors () {
      return this.csvErrors.length > 0
    },
    unknownAquifers () {
      return (this.apiValidationErrors || {}).unknownAquifers || []
    },
    unknownWells () {
      return (this.apiValidationErrors || {}).unknownWells || []
    },
    conflicts () {
      return (this.apiValidationErrors || {}).conflicts || []
    },
    hasDataToProcess () {
      return this.verticalAquiferExtents.length > 0
    },
    hasUnknownWellsOrAquifers () {
      return this.unknownAquifers.length > 0 || this.unknownWells.length > 0
    },
    hasConflicts () {
      return this.conflicts.length > 0
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
    tableData () {
      const vae = this.verticalAquiferExtents
        .map((val) => {
          const data = { ...val }

          const conflict = this.conflicts.find((conflict) => {
            return (
              conflict.wellTagNumber === val.wellTagNumber &&
              conflict.aquiferId === val.aquiferId &&
              conflict.fromDepth === val.fromDepth &&
              conflict.toDepth === val.toDepth
            )
          })

          if (conflict) {
            data.conflictMessage = conflict.message
          }

          return data
        })

      return vae
    },
    tableFields () {
      if (this.hasConflicts) {
        return BASE_TABLE_FIELDS.concat([
          {
            key: 'conflictMessage',
            label: 'Error',
            class: 'conflict-msg',
            sortable: false
          }
        ])
      }

      return BASE_TABLE_FIELDS
    },
    showSubmitButton () {
      if (this.hasCSVErrors) {
        return false
      } else if (this.hasUnknownWellsOrAquifers) {
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
    },
    submitButtonLabel () {
      if (this.hasBeenValidated) {
        return 'Submit'
      } else if (this.hasConflicts) {
        return 'Validate Data Again'
      }

      return 'Validate Data'
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
    floatPrecision (val) {
      if (!isFinite(val)) return 0
      let e = 1
      let p = 0
      while (Math.round(val * e) / e !== val) { e *= 10; p++ }
      return p
    },
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
          console.log('error', error)
          console.log('data', data)
          console.log('meta', meta)

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
      } else if (toDepth !== null && (fromDepth > toDepth)) {
        return this.logCSVError(rowNumLabel, `from_depth "${fromDepth}" is below "${toDepth}"`)
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

      if (item.conflictMessage) {
        classes.push('has-conflict')
      }
      return classes.join(' ')
    }
  }
}
</script>
<style lang="scss">
#bulk-vertical-aquifer-extents-screen {
  .conflict-color {
    color: #ec3838;
  }

  p {
    margin-bottom: 1.5rem;
  }

  #instructions {
    ol {
      margin: 0;
      padding: 0 0 0 1.1em;

      li {
        margin: 0.2rem 0;
      }
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

  #vertical-aquifer-extents {
    tr.has-conflict {
      @extend .conflict-color;
    }
  }
}
</style>
