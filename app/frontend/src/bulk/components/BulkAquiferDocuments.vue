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
  <div id="bulk-aquifer-documents-upload-screen">
    <div class="container mb-4 !px-0">
      <Breadcrumb class="p-0" :model="breadcrumbs">
        <template #item="{ item }">
          <router-link v-if="!item.active" :to="item.route">{{ item.label }}</router-link>
          <span v-else>{{ item.label }}</span>
        </template>
      </Breadcrumb>
    </div>
    <b-card class="container p-1" v-if="perms.aquiferDocuments">
      <api-error v-if="apiError" :error="apiError"/>

      <div>
        <div class="border-bottom mb-4 pb-2 pt-2">
          <h3>Aquifer Documents Bulk Upload</h3>
        </div>
        <div class="w-full border-gray-300 border-1 border-solid h-0 mb-5" >&nbsp;</div>
        <div v-if="showSaveSuccess">
          <Message
            class="my-3"
            severity="success"
          >
            <p class="m-0">
              All documents uploaded for aquifers.
            </p>
          </Message>
          <Button
            @click="restart">
            Upload more documents
          </Button>
        </div>
        <div v-else>
          <div class="flex mb-8">
            <Card @click="behaviour = 'multi'" :class="[ 'w-1/2', behaviour == 'keyed' ? 'chosen' : '' ]">
              <template #title>
                <h3>Multiple documents for multiple aquifers</h3>
              </template>
              <template #content>
                <div>
                  If you have one or more documents that you want to upload for one or more aquifers.
                </div>
              </template>
              <template #footer>
                <Button>
                  Multiple Uploads
                </Button>
              </template>
            </Card>
            <Card @click="behaviour = 'keyed'" :class="[ 'w-1/2', behaviour == 'multi' ? 'chosen' : '' ]">
              <template #title>
                <h3>Documents for specific aquifers</h3>
              </template>
              <template #content>
                <div>
                  If you have many documents that are each named for their respective aquifers (e.g. factsheet_0001.pdf and factsheet_0002.pdf)
                </div>
              </template>
              <template #footer>
                <Button>
                  Aquifer Keyed Files
                </Button>
              </template>
            </Card>
          </div>

          <div v-if="behaviourPicked">
            <Card id="instructions" class="mb-4" title="Instructions">
              <template #content>
                <div class="flex p-5">
                  <div class="w-1/3">
                    <ol>
                      <li v-if="multiBehaviourPicked" :class="{active: multiActiveStep === 'one'}">Use the file picker below to choose one or more documents.</li>
                      <li v-else :class="{active: keyedActiveStep === 'one'}">Use the file picker below to choose one or more documents keyed by aquifer ID (e.g. factsheet_0001.pdf, factsheet_0002.pdf).</li>
                      <li v-if="multiBehaviourPicked" :class="{active: multiActiveStep === 'two'}">Search for the aquifer in the dropdown list to the right.</li>
                      <li v-if="multiBehaviourPicked" :class="{active: multiActiveStep === 'three'}">Add more aquifers as needed.</li>
                      <li :class="{active: multiActiveStep === 'four' || keyedActiveStep === 'two'}">
                        Click “Submit” to upload the
                        <plural :count="multiBehaviourPicked ? commonStore.uploadFiles.length : numAquiferDocuments">
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
                        <plural :count="multiBehaviourPicked ? aquiferIds.length : Object.keys(aquiferDocuments).length">
                          <template #zero>
                            <!-- needs a zero-width-word-joiner on purpose to force zero case to be empty -->
                            &#8203;
                          </template>
                          <template #singular="{ count }">
                            for {{count}} aquifer
                          </template>
                          <template #plural="{ count }">
                            for {{count}} aquifers
                          </template>
                        </plural>
                      </li>
                    </ol>
                  </div>
                  <div v-if="multiBehaviourPicked" class="w-2/3">
                    <div style="color: red;">
                      <p>
                        NOTE: When selecting files, ensure name does <u>not</u> include the aquifer number,
                        as this information is automatically added when uploaded (AQ_XXXXX).
                      </p>
                      <p>e.g., File name -> "Factsheet.pdf" and then selecting "Aquifer 123" - will upload as "AQ_00123_Factsheet.pdf"</p>
                    </div>
                    <br>
                    <div>Aquifer attachment naming conventions guidance:</div>
                    <div class="ml-4">
                      <div>
                        Standard file names (before upload to GWELLS) include:
                        <div class="ml-4 mb-4">
                          <div>Aquifer_Factsheet.pdf</div>
                          <div>Aquifer_Mapping_Report.pdf</div>
                          <div>Hydrogeologic_Map_1.jpg (if more than one continue numbering)</div>
                          <div>CrossSection_YY_XofX.jpg (where YY is the cross-section line, and x is number of parts of the cross-section)
                            <div class="ml-4">E.g., “CrossSection_2L2L’_1of2”, “CrossSection_AA’_1of1”</div>
                          </div>
                          <div>Hydrogeologic_Schematic_XX (where XX is direction, e.g., EW or NS)
                            <div class="ml-4">E.g., “Hydrogeologic_Schematic_NS”</div>
                          </div>
                        </div>
                      </div>
                      <div>
                        If file name does not fit one of the standards above, consider the following when creating a file name:
                        <div class="ml-4">
                          <div>Do not include aquifer number in file name, it is added to the file name automatically when the aquifer number is selected from the search bar.</div>
                          <div>No spaces in the name – use underscores.</div>
                          <div>If name is identical to older version, older version will be overwritten (please check spelling).</div>
                          <div>Name must be as succinct but as clear as possible as to what the attachment includes.</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </Card>
            <div class="flex">
              <div class="w-1/2 p-2">
                <h5>Documents</h5>
                <div class="mb-3 flex items-center">
                  <FileUpload
                    ref="fileUpload"
                    name="files[]"
                    mode="basic"
                    :showUploadButton="false"
                    :showCancelButton="false"
                    :disabled="isSaving"
                    auto
                    @select="filesPicked($event.files)"
                    class="mr-4"
                  />
                  <Checkbox id="private-documents-checkbox" v-model="privateDocument" binary class="mr-3"/>Are these documents private?
                </div>
                <div>
                  <DataTable
                    v-if="commonStore.uploadFiles.length > 0"
                    :value="commonStore.uploadFiles"
                    stripedRows
                    class="mb-4"
                  >
                    <Column header="" class="max-w-22">
                      <template #body="slotProps">
                        <Button
                          size="small"
                          severity="danger"
                          @click="commonStore.removeFile(slotProps.data)"
                          :disabled="isSaving">
                          Remove
                        </Button>
                      </template>
                    </Column>
                    <Column field="name" header="File name"></Column>
                    <Column field="size" header="Size">
                      <template #body="slotProps">
                        {{ formatFileSize(slotProps.data.size) }}
                      </template>
                    </Column>
                  </DataTable>
                  <div class="mt-4">
                    <Button
                      class="mr-4"
                      v-if="showSubmitButton"
                      :disabled="submitButtonIsDisabled"
                      @click="save">
                      Submit
                    </Button>
                    <Button
                      v-if="showResetButton"
                      severity="secondary"
                      @click="reset">
                      Reset
                    </Button>
                  </div>
                </div>

              </div>
              <div class="w-1/2" v-if="multiBehaviourPicked">
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
                      <template v-slot:no-options>
                        Search for an aquifer by name or id number
                      </template>
                      <template v-slot:cell(option)="option">
                        <div>{{ option.description }}</div>
                      </template>
                      <template v-slot:cell(selected-option)="option">
                        <div>{{ option.description }}</div>
                      </template>
                    </v-select>
                  </li>
                </ul>
              </div>
              <div v-else>
                <Message
                  v-if="unknonwnAquiferIdsExist"
                  class="my-3"
                  severity="error"
                >
                  <p class="m-0">
                    Aquifers in <span style="color:red">red</span> do not exist
                  </p>
                </Message>
                <DataTable
                  :value="aquiferTableData"
                  stripedRows
                  class="mb-12"
                >
                  <template #empty>No documents with keyed aquifer IDs</template>
                  <Column field="aquiferId" header="Aquifer">
                    <template #body="slotProps">
                      <span :class="{ unknown: checkAquiferIsUnknown(slotProps.data.aquiferId) }">
                        {{slotProps.data.aquiferId}}
                      </span>
                    </template>
                  </Column>
                  <Column field="documents" header="Documents">
                    <template #body="slotProps">
                      <ul class="list-disc m-4">
                        <li v-for="(doc, index) in slotProps.data.documents" :key="index" :class="{overwrite: doc.exists}">
                          {{ doc.name }}
                        </li>
                      </ul>
                    </template>
                  </Column>
                </DataTable>
                <div v-if="!multiBehaviourPicked">
                  <div>
                    <div style="color: red;">
                      <p>
                        NOTE: When selecting files, ensure the file name includes aquifer number as "_XXXX", as the upload process
                        looks for this number to assign the file to the correct aquifer page (AQ_XXXXX)
                      </p>
                      <p>e.g., File name -> "Factsheet_0123.pdf" will upload as "AQ_00123_Factsheet.pdf" on the Aquifer 123 page.</p>
                    </div>
                    <br>
                    <div>Aquifer attachment naming conventions guidance:</div>
                    <div class="ml-4 mb-4">
                      <div>
                        Standard file names (before upload to GWELLS) include:
                        <div class="ml-4 mb-4">
                          <div>Aquifer_Factsheet_XXXX.pdf</div>
                          <div>Aquifer_Mapping_Report_XXXX.pdf</div>
                          <div>Hydrogeologic_Map_1_XXXX.jpg (if more than one, continue numbering)</div>
                          <div>CrossSection_YY_XofX_XXXX.jpg (where YY is the cross-section line, and x is number of parts of the cross-section)
                            <div class="ml-4">E.g., “CrossSection_2L2L’_1of2_XXXX”, “CrossSection_AA’_1of1_XXXX”</div>
                          </div>
                          <div>Hydrogeologic_Schematic_XX (where XX is direction, e.g., EW or NS)
                            <div class="ml-4">E.g., “Hydrogeologic_Schematic_NS_XXXX”</div>
                          </div>
                        </div>
                      </div>
                      <div>
                        If file name does not fit one of the standards above, consider the following when creating a file name:
                        <div class="ml-4 mb-4">
                          <div>No spaces in the name – use underscores.</div>
                          <div>If name is identical to older version, older version will be overwritten (please check spelling).</div>
                          <div>Name must be as succinct but as clear as possible as to what the attachment includes.</div>
                          <div>Add aquifer number as 4 digits in front of the file type to let application know what aquifer to assign the attachment,<br/>
                            E.g., Aquifer_Factsheet_0001.pdf or Aquifer_Mapping_Report_0456.pdf
                            <div class="ml-4">It will automatically be renamed. E.g., “AQ_0001_Aquifer_Factsheet.pdf” or “AQ_0456_ Aquifer_Mapping_Report.pdf”</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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
import { useCommonStore } from '@/stores/common.js'
import { debounce } from 'lodash-es'

import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage.vue'
import Plural from '@/common/components/Plural.vue'

const AQUIFER_ID_RE = /([_ -]+)(\d+)(\.[a-zA-Z0-9]+)$/

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
      ],
      breadcrumbs: [
        {
          label: 'Bulk Upload',
          route: { name: 'bulk-home' }
        },
        {
          label: 'Aquifer Documents Bulk Upload',
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
    commonStore () { return useCommonStore() },
    perms () {
      return this.commonStore.userRoles.bulk || {}
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
    privateDocument: {
      get: function () {
        return this.commonStore.isPrivate
      },
      set: function (value) {
        this.commonStore.setPrivate(value)
      }
    },
    aquiferIds () {
      return this.aquifersList.filter((aquiferId) => Boolean(aquiferId))
    },
    hasAPIValidationErrors () {
      return Object.keys(this.apiValidationErrors).length > 0
    },
    aquiferDocuments () {
      const docs = {}

      this.commonStore.uploadFiles.forEach((file) => {
        const aquiferId = this.parseAquiferIdFromFileName(file.name)
        if (aquiferId) {
          docs[aquiferId] = docs[aquiferId] || []
          docs[aquiferId].push(file)
        }
      })

      return docs
    },
    aquiferTableData () {
      return Object.keys(this.aquiferDocuments).map((aquiferId) => {
        return {
          aquiferId: parseInt(aquiferId, 10),
          documents: this.aquiferDocuments[aquiferId]
        }
      })
    },
    numAquiferDocuments () {
      return Object.keys(this.aquiferDocuments).reduce((count, key) => {
        return count + this.aquiferDocuments[key].length
      }, 0)
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
    submitButtonIsDisabled () {
      if (this.isSaving) {
        return true
      } else if (this.commonStore.uploadFiles.length === 0) {
        return true
      } else if (this.unknonwnAquiferIdsExist) {
        return true
      }

      return false
    },
    showResetButton () {
      return true
    },
    multiActiveStep () {
      if (!this.multiBehaviourPicked) { return null }

      if (this.commonStore.uploadFiles.length === 0) {
        return 'one'
      } else if (this.aquiferIds.length === 0) {
        return 'two'
      } else if (this.aquiferIds.length === 1) {
        return 'three'
      }

      return 'four'
    },
    keyedActiveStep () {
      if (!this.keyedBehaviourPicked) { return null }

      if (this.commonStore.uploadFiles.length === 0) {
        return 'one'
      }

      return 'two'
    }
  },
  watch: {
    uploadFiles () {
      this.checkAquiferIds()
    }
  },
  methods: {
    save () {
      this.commonStore.clearUploadFilesMessage()

      this.showSaveSuccess = false
      this.apiError = null
      this.apiValidationErrors = {}
      this.isSaving = true

      let promise = null
      if (this.multiBehaviourPicked) {
        promise = this.uploadAllFilesForAllAquifers()
      } else {
        promise = this.uploadAquiferFiles()
      }

      promise.then(() => {
        this.commonStore.fileUploadSucceeded()
        this.handleSaveSuccess()
      }).catch((error) => {
        this.commonStore.fileUploadFail()
        this.handleApiError(error)
        throw error
      })
    },
    uploadAllFilesForAllAquifers () {
      return this.aquiferIds.reduce((previousPromise, aquiferId) => {
        return this.commonStore.uploadTheFiles({
          documentType: 'aquifers',
          recordId: aquiferId
        })
      }, Promise.resolve())
    },
    uploadAquiferFiles () {
      const documents = this.aquiferDocuments
      const aquiferIds = Object.keys(documents)
        .map((key) => parseInt(key, 10))
        .filter((aquiferId) => {
          return (this.unknonwnAquiferIds || []).indexOf(aquiferId) === -1
        })

      return aquiferIds.reduce((previousPromise, aquiferId) => {
        return previousPromise.then(() => {
          const files = documents[aquiferId]
          if (files.length === 0) {
            return Promise.resolve()
          }

          const fileNames = files.map((file) => this.fileNameWithoutPrefix(file.name))

          return this.commonStore.uploadTheFiles({
            documentType: 'aquifers',
            recordId: aquiferId,
            files,
            fileNames
          })
        })
      }, Promise.resolve())
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
        ApiService.query(`aquifers/names?aquifer_ids=${aquiferIds.join(',')}`)
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
    },
    parseAquiferIdFromFileName (fileName) {
      const matches = fileName.match(AQUIFER_ID_RE)
      if (matches) {
        return parseInt(matches[2], 10) || null
      }
      return null
    },
    fileNameWithoutPrefix (fileName) {
      // Strips aquifer ID from file name.
      return fileName.replace(AQUIFER_ID_RE, '$3')
    },
    fileIsInvalid (file) {
      if (this.keyedBehaviourPicked) {
        const aquiferId = this.parseAquiferIdFromFileName(file.name)

        if (aquiferId) {
          if (this.unknonwnAquiferIdsExist && this.unknonwnAquiferIds.indexOf(aquiferId) !== -1) {
            return true
          }

          return false
        }

        return true
      }

      return false
    },
    filesPicked (files) {
      // Only setFiles when files > 0 because setFiles will empty the
      // uploadFiles collection if sent an empty array.
      if (files.length > 0) {
        this.commonStore.setFiles(files)
      }
    }
  }
}
</script>
<style scoped lang="scss">
.p-card.chosen {
  opacity: 0.2;
}
.p-card-body {
  padding: 0 !important;

  .p-card-caption {
    padding-top: 1.5rem;
  }
  .p-card-footer {
    padding-bottom: 1.5rem;
  }
  > * {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  .p-card-footer {
    padding: 1.5rem;
    background-color: #f6f6f6 !important;
  }
}
#bulk-aquifer-documents-upload-screen {
  #instructions {
    ol {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    li {
      margin: 0 0 0.5rem 0;
      padding: 0;

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
