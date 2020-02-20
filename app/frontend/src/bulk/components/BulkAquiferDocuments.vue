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

        <b-alert show v-if="showSaveSuccess" variant="success" >
          All documents uploaded for aquifers {{this.aquiferIds.join(', ')}}
        </b-alert>

        <b-card id="instructions" class="mb-3" title="Instructions">
          <ol>
            <li :class="{active: this.activeStep === 'one'}">Use the file picker below to choose one or more documents.</li>
            <li :class="{active: this.activeStep === 'two'}">Search for the aquifer in the dropdown list to the right.</li>
            <li :class="{active: this.activeStep === 'three'}">Add more aquifers as needed.</li>
            <li :class="{active: this.activeStep === 'four'}">Click “Save” to upload the selected documents for aquifers: {{this.aquiferIds.join(', ')}}</li>
          </ol>
        </b-card>

        <b-form @submit.prevent="save()" @reset.prevent="restart()">
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
              @click="restart">
              Reset
            </b-button>
          </b-button-group>
        </b-form>
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
      apiError: null,
      files: null,
      apiValidationErrors: {},
      isSaving: false,
      showSaveSuccess: false,
      aquifersList: [null],
      aquiferSearchResults: []
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
    showSubmitButton () {
      if (this.hasAPIValidationErrors) {
        return false
      } else if (this.showSaveSuccess) {
        return false
      }

      return true
    },
    showResetButton () {
      if (this.upload_files.length > 0) {
        return true
      } else if (this.aquiferIds.length > 0) {
        return true
      } else if (this.showSaveSuccess) {
        return true
      }

      return false
    },
    activeStep () {
      if (this.upload_files.length === 0) {
        return 'one'
      } else if (this.aquiferIds.length === 0) {
        return 'two'
      } else if (this.aquiferIds.length === 1) {
        return 'three'
      }

      return 'four'
    },
    stepTwoActive () {
      return this.upload_files.length > 0 && this.aquiferIds.length === 0
    },
    stepThreeActive () {
      return this.aquiferIds.length > 0
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

      const promises = this.aquiferIds.map((aquiferId) => {
        return this.uploadFiles({
          documentType: 'aquifers',
          recordId: aquiferId
        })
      })

      return Promise.all(promises)
        .then(() => {
          this.fileUploadSuccess()
          this.handleSaveSuccess()
        }).catch((error) => {
          this.fileUploadFail()
          this.handleSaveError(error)
          throw error
        })
    },
    handleSaveSuccess () {
      this.isSaving = false
      this.showSaveSuccess = true
      this.reset()
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
      this.apiValidationErrors = {}
      this.isSaving = false
      this.setFiles([])
      this.aquifersList = [null]
      this.aquiferSearchResults = []
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
    }
  }
}
</script>
<style lang="scss">
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
