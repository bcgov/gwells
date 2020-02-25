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
          <b-col><h4>Aquifer Documents Bulk Upload</h4></b-col>
        </b-row>

        <div v-if="showSaveSuccess">
          <b-alert show variant="success" >
            All documents uploaded for aquifers.
          </b-alert>

          <b-button
            variant="default"
            @click="restart">
            Upload more documents
          </b-button>
        </div>
        <div v-else>
          <b-card-group id="upload-behaviour" class="mb-3">
            <b-card title="Multiple documents for multiple aquifers" :class="{ chosen: behaviourPicked, active: multiBehaviourPicked}">
              <b-card-text>
                If you have one or more documents that you want to upload for one or more aquifers.
              </b-card-text>
              <template v-slot:footer>
                <b-btn variant="primary" @click="behaviour = 'multi'" :disabled="behaviourPicked">
                  Multiple Uploads
                </b-btn>
              </template>
            </b-card>
            <b-card title="Documents for specific aquifers" :class="{ chosen: behaviourPicked, active: behaviour === 'keyed'}">
              <b-card-text>
                If you have many documents that are each named for their respective aquifers (e.g. factsheet_01.pdf and factsheet_02.pdf)
              </b-card-text>
              <template v-slot:footer>
                <b-btn variant="primary" @click="behaviour = 'keyed'" :disabled="behaviourPicked">
                  Aquifer Keyed Files
                </b-btn>
              </template>
            </b-card>
          </b-card-group>

          <div v-if="behaviourPicked">
            <b-card id="instructions" class="mb-3" title="Instructions">
              <div v-if="multiBehaviourPicked">
                <ol>
                  <li :class="{active: this.multiActiveStep === 'one'}">Use the file picker below to choose one or more documents.</li>
                  <li :class="{active: this.multiActiveStep === 'two'}">Search for the aquifer in the dropdown list to the right.</li>
                  <li :class="{active: this.multiActiveStep === 'three'}">Add more aquifers as needed.</li>
                  <li :class="{active: this.multiActiveStep === 'four'}">Click “Submit” to upload the {{this.documents.length}} documents for {{this.aquiferIds.length}} aquifers</li>
                </ol>
              </div>
              <div v-else>
                <ol>
                  <li :class="{active: this.keyedActiveStep === 'one'}">Use the file picker below to choose one or more documents keyed by aquifer ID. E.g. (factsheet_01.pdf, factsheet_02.pdf).</li>
                  <li :class="{active: this.keyedActiveStep === 'two'}">Click “Submit” to upload the {{this.documents.length}} documents for {{Object.keys(this.aquiferDocuments).length}} aquifers</li>
                </ol>
              </div>
            </b-card>

            <b-form @submit.prevent="save()" @reset.prevent="reset()">
              <b-row>
                <b-col md="6" id="documents">
                  <h5>Documents</h5>
                  <b-row class="align-items-center mb-3">
                    <b-col md="6">
                      <b-form-file v-model="documents" multiple plain/>
                    </b-col>
                    <b-col md="6">
                      <div>
                        <b-form-checkbox
                          id="private-documents-checkbox"
                          v-model="privateDocument">Are these documents private?</b-form-checkbox>
                      </div>
                    </b-col>
                  </b-row>
                  <table id="files-to-upload">
                    <tbody>
                      <tr v-for="(file, index) in upload_files" :key="index">
                        <td>{{file.name}}</td>
                        <td>{{formatFileSize(file.size)}}</td>
                        <td><input type="button" value="remove" @click.prevent="removeFile(file)"/></td>
                      </tr>
                    </tbody>
                  </table>
                </b-col>
                <b-col md="6" id="aquifers">
                  <h5>Aquifers</h5>
                  <div v-if="multiBehaviourPicked">
                    <ul>
                      <li v-for="(aquiferId, index) in aquifersList" :key="index">
                        <v-select
                          :id="`aquifer_${index}`"
                          v-model="aquifersList[index]"
                          :filterable="false"
                          :options="aquiferSearchResults"
                          :reduce="aquifer => aquifer.aquifer_id"
                          label="description"
                          index="aquifer_id"
                          :key="aquiferId"
                          @search="onAquiferSearch"
                          @input="onAquiferSelected(index)">
                          <template slot="no-options">
                            Search for an aquifer by name or id number
                          </template>
                          <template slot="option" slot-scope="option">
                            <div>{{ option.description }}</div>
                          </template>
                          <template slot="selected-option" slot-scope="option">
                            <div>{{ option.description }}</div>
                          </template>
                        </v-select>
                      </li>
                    </ul>
                  </div>
                  <div v-else>
                    <b-alert show variant="danger" v-if="unknonwnAquiferIdsExist">
                      Aquifers in <span style="color:red">red</span> do not exist
                    </b-alert>

                    <b-table
                      :items="aquiferTableData"
                      :fields="aquiferTableFields"
                      v-if="upload_files.length > 0"
                      striped>
                      <template slot="aquiferId" slot-scope="row">
                        <span :class="{ unknown: checkAquiferIsUnknown(row.item.aquiferId) }">
                          {{row.item.aquiferId}}
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
                  </div>
                </b-col>
              </b-row>

              <b-button-group class="mt-3">
                <b-button
                  v-if="showSubmitButton"
                  :disabled="isSaving || upload_files.length === 0"
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
        <p>You do not have permission to bulk upload aquifer data.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapState, mapActions } from 'vuex'
import { debounce } from 'lodash'

import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'

export default {
  data () {
    return {
      behaviour: null,
      apiError: null,
      files: null,
      apiValidationErrors: {},
      isSaving: false,
      showSaveSuccess: false,
      aquifersList: [null],
      aquiferSearchResults: [],
      unknonwnAquiferIds: null,
      aquiferTableFields: [
        {
          key: 'aquiferId',
          label: 'Aquifer',
          sortable: true
        },
        {
          key: 'documents',
          label: 'Documents'
        }
      ]
    }
  },
  components: {
    'api-error': APIErrorMessage
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
    behaviourPicked () {
      return this.behaviour !== null
    },
    multiBehaviourPicked () {
      return this.behaviour === 'multi'
    },
    keyedBehaviourPicked () {
      return this.behaviour === 'keyed'
    },
    documents: {
      get: function () {
        return this.upload_files
      },
      set: function (value) {
        this.setFiles(value)
      }
    },
    privateDocument: {
      get: function () {
        return this.isPrivate
      },
      set: function (value) {
        this.setPrivate(value)
      }
    },
    aquiferIds () {
      return this.aquifersList.filter((aquiferId) => Boolean(aquiferId))
    },
    hasAPIValidationErrors () {
      return Object.keys(this.apiValidationErrors).length > 0
    },
    aquiferDocuments () {
      const list = []

      this.upload_files.forEach((file) => {
        const matches = file.name.match(/[_ -](\d+)\.[a-zA-Z0-9]+$/)
        if (matches) {
          const aquiferId = parseInt(matches[1], 10) || null

          if (aquiferId) {
            list[aquiferId] = list[aquiferId] || []
            list[aquiferId].push(file)
          }
        }
      })

      return list
    },
    aquiferTableData () {
      return Object.keys(this.aquiferDocuments).map((aquiferId) => {
        return {
          aquiferId: parseInt(aquiferId, 10),
          documents: this.aquiferDocuments[aquiferId]
        }
      })
    },
    unknonwnAquiferIdsExist () {
      return this.unknonwnAquiferIds !== null && this.unknonwnAquiferIds.length > 0
    },
    showSubmitButton () {
      if (this.hasAPIValidationErrors) {
        return false
      } else if (this.showSaveSuccess) {
        return false
      }

      return true
    },
    showResetButton () {
      return true
    },
    multiActiveStep () {
      if (this.upload_files.length === 0) {
        return 'one'
      } else if (this.aquiferIds.length === 0) {
        return 'two'
      } else if (this.aquiferIds.length === 1) {
        return 'three'
      }

      return 'four'
    },
    keyedActiveStep () {
      if (this.upload_files.length === 0) {
        return 'one'
      }

      return 'two'
    },
    stepTwoActive () {
      return this.upload_files.length > 0 && this.aquiferIds.length === 0
    },
    stepThreeActive () {
      return this.aquiferIds.length > 0
    }
  },
  watch: {
    upload_files () {
      this.checkAquiferIds()
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
      'clearUploadFilesMessage',
      'resetUploadFiles'
    ]),
    save () {
      this.clearUploadFilesMessage()

      this.showSaveSuccess = false
      this.apiError = null
      this.apiValidationErrors = {}
      this.isSaving = true

      let promises = []
      if (this.multiBehaviourPicked) {
        promises = this.uploadAllFilesForAllAquifers()
      } else {
        promises = this.uploadAquiferFiles()
      }

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
    uploadAllFilesForAllAquifers () {
      return this.aquiferIds.map((aquiferId) => {
        return this.uploadFiles({
          documentType: 'aquifers',
          recordId: aquiferId
        })
      })
    },
    uploadAquiferFiles () {
      return Object.keys(this.aquiferDocuments)
        .filter((key) => {
          return (this.unknonwnAquiferIds || []).indexOf(parseInt(key, 10)) === -1
        }).map((key) => {
          const aquiferId = parseInt(key, 10)
          return this.uploadFiles({
            documentType: 'aquifers',
            recordId: aquiferId,
            files: this.aquiferDocuments[aquiferId]
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
      this.apiValidationErrors = {}
      this.isSaving = false
      this.setFiles([])
      this.aquifersList = [null]
      this.aquiferSearchResults = []
      this.behaviour = null
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
    onAquiferSelected (index) {
      if (this.aquifersList[this.aquifersList.length - 1] !== null) {
        this.aquifersList.push(null) // add a new empty aquifer dropdown at the bottom
      } else {
        for (var i = this.aquifersList.length - 2; i >= 0; i--) { // leave the last null in place
          if (this.aquifersList[i] === null) {
            this.aquifersList.splice(i, 1)
          } else {
            break
          }
        }
      }
      this.aquiferSearchResults = []
    },
    aquiferSearch: debounce((loading, search, vm) => {
      if (search === '') {
        loading(false)
        return
      }

      ApiService.query(`aquifers/names?search=${encodeURIComponent(search)}`)
        .then((response) => {
          // filter out any already selected aquiferIds from the options in the list
          vm.aquiferSearchResults = response.data.filter((aquifer) => vm.aquiferIds.indexOf(aquifer.aquifer_id) === -1)
          loading(false)
        })
        .catch((err) => {
          loading(false)
          throw err
        })
    }, 500),
    onAquiferSearch (search, loading) {
      loading(true)
      this.aquiferSearch(loading, search, this)
    },
    checkAquiferIds () {
      const aquiferIds = Object.keys(this.aquiferDocuments).map((id) => parseInt(id, 10))
      this.unknonwnAquiferIds = null
      if (aquiferIds.length > 0) {
        ApiService.query(`aquifers/slim?aquifer_ids=${aquiferIds.join(',')}`)
          .then(({ data }) => {
            this.unknonwnAquiferIds = aquiferIds.filter((aquiferId) => !data.find((aquifer) => aquiferId === aquifer.aquifer_id))
          })
          .catch(this.handleApiError)
      }
    },
    checkAquiferIsUnknown (aquiferId) {
      if (this.unknonwnAquiferIds === null) {
        return false
      }

      return this.unknonwnAquiferIds.indexOf(aquiferId) !== -1
    }
  }
}
</script>
<style lang="scss">
#upload-behaviour {
  .card.chosen {
    &:not(.active) {
      opacity: 0.2;
    }
  }

  .card.active {
    opacity: 1;
    border-left: 1px solid rgba(0,0,0,.125) !important;
  }
}

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

#aquifers {
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
}
</style>
