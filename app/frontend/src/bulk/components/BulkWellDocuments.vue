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
  <div id="bulk-well-documents-upload-screen">
    <b-card no-body class="mb-3 container d-print-none">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"/>
    </b-card>
    <b-card class="container p-1" v-if="perms.wellDocuments">
      <api-error v-if="apiError" :error="apiError"/>

      <b-container>
        <b-row class="border-bottom mb-3 pb-2 pt-2">
          <b-col><h4>Well Documents Bulk Upload</h4></b-col>
        </b-row>

        <div v-if="showSaveSuccess">
          <b-alert show variant="success" >
            All documents uploaded for wells.
          </b-alert>

          <b-button
            variant="default"
            @click="restart">
            Upload more documents
          </b-button>
        </div>
        <div v-else>
          <div id="instructions" class="mb-3" title="Instructions">
            <ol>
              <li :class="{active: keyedActiveStep === 'one'}">
                Use the file picker below to choose one or more documents keyed by well tag number
                (e.g. well_construction_0001.pdf, well_construction_0002.pdf).
              </li>
              <li :class="{active: keyedActiveStep === 'two'}">
                Click “Submit” to upload the
                <plural :count="upload_files.length">
                  <template #zero>
                    documents
                  </template>
                  <template #singular="{ count }">
                    {{count}} document
                  </template>
                  <template #plural="{ count }">
                    {{count}} documents
                  </template>
                </plural>
                <plural :count="numWellDocuments">
                  <template #zero>
                    <!-- needs a zero-width-word-joiner on purpose to force zero case to be empty -->
                    &#8203;
                  </template>
                  <template #singular="{ count }">
                    for {{count}} well
                  </template>
                  <template #plural="{ count }">
                    for {{count}} wells
                  </template>
                </plural>
              </li>
            </ol>
          </div>

          <b-form @submit.prevent="save()" @reset.prevent="reset()">
            <b-row>
              <b-col md="6" id="documents">
                <h5>Documents</h5>
                <b-row class="align-items-center mb-3">
                  <b-col md="3">
                    <b-form-file
                      multiple
                      :key="`file-upload-${upload_files.length}`"
                      @input="filesPicked"/>
                  </b-col>
                  <b-col md="9">
                    <div>
                      <b-form-checkbox
                        id="private-documents-checkbox"
                        v-model="privateDocument">Are these documents private?</b-form-checkbox>
                    </div>
                  </b-col>
                </b-row>
                <table id="files-to-upload">
                  <tbody>
                    <tr v-for="(file, index) in upload_files" :key="index" :class="{ error: fileIsInvalid(file) }">
                      <td><input type="button" value="remove" @click.prevent="removeFile(file)"/></td>
                      <td>{{file.name}}</td>
                      <td>{{formatFileSize(file.size)}}</td>
                    </tr>
                  </tbody>
                </table>
              </b-col>
              <b-col md="6" id="wells">
                <h5>Wells</h5>
                <b-alert show variant="warning" v-if="unknonwnWellIdsExist">
                  Wells in <span style="color:red">red</span> do not exist
                </b-alert>

                <b-table
                  :items="wellTableData"
                  :fields="wellTableFields"
                  v-if="upload_files.length > 0"
                  :show-empty="wellTableData.length === 0"
                  empty-text="No documents with well tag numbers"
                  striped>
                  <template slot="wellTagNumber" slot-scope="row">
                    <span :class="{ unknown: checkWellIsUnknown(row.item.wellTagNumber) }">
                      {{row.item.wellTagNumber}}
                    </span>
                  </template>
                  <template slot="documents" slot-scope="row">
                    <ul>
                      <li v-for="(file, index) in row.item.documents" :key="index">
                        {{ file.name }}
                      </li>
                    </ul>
                  </template>
                </b-table>
              </b-col>
            </b-row>

            <b-button-group class="mt-3">
              <b-button
                v-if="showSubmitButton"
                :disabled="submitButtonIsDisabled"
                variant="primary"
                @click="save">
                <b-spinner v-if="isSaving" small label="Loading…"/>
                Submit
              </b-button>
              <b-button
                v-if="showResetButton"
                variant="default"
                @click="reset">
                Reset
              </b-button>
            </b-button-group>
          </b-form>
        </div>
      </b-container>
    </b-card>
    <div class="card container" v-else-if="!$keycloak.authenticated">
      <div class="card-body">
        <p>Please log in to continue.</p>
      </div>
    </div>
    <div class="card container" v-else>
      <div class="card-body">
        <p>You do not have permission to bulk upload well data.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapState, mapActions } from 'vuex'

import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import Plural from '@/common/components/Plural'

export default {
  data () {
    return {
      apiError: null,
      files: null,
      apiValidationErrors: {},
      isSaving: false,
      showSaveSuccess: false,
      wellsList: [null],
      unknonwnWellIds: null,
      wellTableFields: [
        {
          key: 'wellTagNumber',
          label: 'Well',
          sortable: true
        },
        {
          key: 'documents',
          label: 'Documents'
        }
      ],
      breadcrumbs: [
        {
          text: 'Bulk Upload',
          to: { name: 'bulk-home' }
        },
        {
          text: 'Well Documents Bulk Upload',
          active: true
        }
      ]
    }
  },
  components: {
    'api-error': APIErrorMessage,
    plural: Plural
  },
  computed: {
    ...mapState('documentState', [
      'isPrivate',
      'upload_files'
    ]),
    ...mapGetters(['userRoles', 'keycloak']),
    perms () {
      return this.userRoles.bulk || {}
    },
    privateDocument: {
      get: function () {
        return this.isPrivate
      },
      set: function (value) {
        this.setPrivate(value)
      }
    },
    wellTagNumbers () {
      return this.wellsList.filter((wellTagNumber) => Boolean(wellTagNumber))
    },
    hasAPIValidationErrors () {
      return Object.keys(this.apiValidationErrors).length > 0
    },
    wellDocuments () {
      const list = []

      this.upload_files.forEach((file) => {
        const wellTagNumber = this.parseWellIdFromFileName(file.name)
        if (wellTagNumber) {
          list[wellTagNumber] = list[wellTagNumber] || []
          list[wellTagNumber].push(file)
        }
      })

      return list
    },
    numWellDocuments () {
      return Object.keys(this.wellDocuments).reduce((count, key) => {
        return count + this.wellDocuments[key].length
      }, 0)
    },
    wellTableData () {
      return Object.keys(this.wellDocuments).map((wellTagNumber) => {
        return {
          wellTagNumber: parseInt(wellTagNumber, 10),
          documents: this.wellDocuments[wellTagNumber]
        }
      })
    },
    unknonwnWellIdsExist () {
      return this.unknonwnWellIds !== null && this.unknonwnWellIds.length > 0
    },
    showSubmitButton () {
      if (this.hasAPIValidationErrors) {
        return false
      } else if (this.showSaveSuccess) {
        return false
      }

      return true
    },
    submitButtonIsDisabled () {
      if (this.isSaving) {
        return true
      } else if (this.numWellDocuments === 0) {
        return true
      } else if (this.unknonwnWellIdsExist) {
        return true
      }

      return false
    },
    showResetButton () {
      return true
    },
    keyedActiveStep () {
      if (this.upload_files.length === 0) {
        return 'one'
      }

      return 'two'
    }
  },
  watch: {
    upload_files () {
      this.checkWellIds()
    }
  },
  methods: {
    ...mapMutations('documentState', [
      'setFiles',
      'setPrivate',
      'removeFile'
    ]),
    ...mapActions('documentState', [
      'uploadFiles',
      'fileUploadSuccess',
      'fileUploadFail',
      'clearUploadFilesMessage'
    ]),
    save () {
      this.clearUploadFilesMessage()

      this.showSaveSuccess = false
      this.apiError = null
      this.apiValidationErrors = {}
      this.isSaving = true

      const promises = this.uploadWellFiles()

      return Promise.all(promises)
        .then(() => {
          this.fileUploadSuccess()
          this.handleSaveSuccess()
        }).catch((error) => {
          this.fileUploadFail()
          this.handleApiError(error)
          throw error
        })
    },
    uploadWellFiles () {
      return Object.keys(this.wellDocuments)
        .filter((key) => {
          return (this.unknonwnWellIds || []).indexOf(parseInt(key, 10)) === -1
        }).map((key) => {
          const wellTagNumber = parseInt(key, 10)
          return this.uploadFiles({
            documentType: 'wells',
            recordId: wellTagNumber,
            files: this.wellDocuments[wellTagNumber]
          })
        })
    },
    handleSaveSuccess () {
      this.isSaving = false
      this.showSaveSuccess = true
      this.reset()
    },
    handleApiError (error) {
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
      this.apiError = null
      this.apiValidationErrors = {}
      this.isSaving = false
      this.setFiles([])
      this.wellsList = [null]
    },
    restart () {
      this.showSaveSuccess = false
      this.reset()
    },
    formatFileSize (sizeInBytes) {
      if (sizeInBytes / 1024 / 1024 > 1) {
        return `${(sizeInBytes / 1024 / 1024).toFixed(2)} MiB`
      } else if (sizeInBytes / 1024 > 1) {
        return `${(sizeInBytes / 1024).toFixed(2)} KiB`
      }

      return `${sizeInBytes} bytes`
    },
    checkWellIds () {
      const wellTagNumbers = Object.keys(this.wellDocuments).map((id) => parseInt(id, 10))
      this.unknonwnWellIds = null
      if (wellTagNumbers.length > 0) {
        ApiService.query(`wells/locations?well_tag_numbers=${wellTagNumbers.join(',')}`)
          .then(({ data: { results } }) => {
            this.unknonwnWellIds = wellTagNumbers.filter((wellTagNumber) => !results.find((well) => wellTagNumber === well.well_tag_number))
          })
          .catch(this.handleApiError)
      }
    },
    checkWellIsUnknown (wellTagNumber) {
      if (this.unknonwnWellIds === null) {
        return false
      }

      return this.unknonwnWellIds.indexOf(wellTagNumber) !== -1
    },
    parseWellIdFromFileName (fileName) {
      const matches = fileName.match(/WTN\s+(\d+)/i)
      if (matches) {
        return parseInt(matches[1], 10) || null
      }
      return null
    },
    fileIsInvalid (file) {
      const wellTagNumber = this.parseWellIdFromFileName(file.name)

      if (wellTagNumber) {
        if (this.unknonwnWellIdsExist && this.unknonwnWellIds.indexOf(wellTagNumber) !== -1) {
          return true
        }

        return false
      }

      return true
    },
    filesPicked (files) {
      // Only setFiles when files > 0 because setFiles will empty the
      // upload_files collection if sent an empty array.
      if (files.length > 0) {
        this.setFiles(files)
      }
    }
  }
}
</script>
<style lang="scss">
#bulk-well-documents-upload-screen {
  #instructions {
    ol {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    li {
      margin: 0 0 0.5rem 0;
      padding: 0;

      &:before {
        display: inline-block;
        width: 16px;
        height: 16px;
        vertical-align: middle;
        margin-top: -2px;
        margin-right: 5px;
        content: "";
      }

      &.active {
        color: #5c35f9;

        &:before {
          background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' fill='%235c35f9' viewBox='0 0 640 640' width='16' height='16'><path d='M128 0L0 128L192 320L0 512L128 640L448 320L128 0Z'/></svg>") no-repeat center center;
        }
      }

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  #files-to-upload {
    tr {
      &.error {
        color: red;
      }
    }

    td {
      padding: 0.3rem 0.5rem;
      border-bottom: 1px solid #EEE;

      &:first-child {
        padding-left: 0;
      }

      &:last-child {
        padding-right: 0;
      }
    }

    tr:last-child {
      td {
        border-bottom: none;
      }
    }
  }

  #wells {
    ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    li {
      margin: 0 0 0.5rem 0;
      padding: 0;

      &:last-child {
        margin-bottom: 0;
      }
    }

    table {
      .unknown {
        color: red;
      }
    }
  }

  #documents {
    ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    li {
      margin: 0 0 0.5rem 0;
      padding: 0;
    }

    input[type="button"] {
      background-color: #d8292f;
      padding: 2px 5px;
      font-size: 10px;
      color: white;
      border: 1px solid #d8292f;
      border-radius: 2px;

      &:hover {
        background-color: #b92227;
        border-color: #ae2025;
      }
    }

    .custom-file-label {
      color: transparent;
      overflow: hidden;

      &:after {
        left: 0;
        border-left: none;
        content: "Pick files";
      }
    }
  }
}
</style>
