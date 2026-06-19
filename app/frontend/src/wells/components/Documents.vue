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
  <div id="well-documents">
    <div v-if="loading">
      Loading documents...
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"/>
      </div>
    </div>
    <div v-else class="mt-4">
      <!-- public documents -->
      <div v-if="error">
        {{error}}
      </div>
      <DataTable rowHover stripedRows :value="files.private ? [...files.public, ...files.private] : [...files.public]">
        <Column field="well_number"/>
        <Column field="document_type">
          <template #body="{ data }">{{ callLongFormLabel(data.document_type) }}</template>
        </Column>
        <Column field="date_of_upload">
          <template #body="{ data }">{{ data.date_of_upload !== -1 ? new Date(data.date_of_upload).toLocaleDateString() : "Date Unknown" }}</template>
        </Column>
        <Column field="document_status">
          <template #body="{ data }">
            <a :href="data.url" :download="data.name" target="_blank">{{ data.item.name }}</a>
          </template>
        </Column>
        <Column field="uploaded_document">
          <template #body="{ data }">
            <p v-if="data.document_status">Private Document</p>
            <p v-else>Public Document</p>
          </template>
        </Column>
      </DataTable>
    </div>
    <Dialog v-model:visible="isDeleteModalVisible" modal header="Confirmation">
      <p>Are you sure you would like to delete this file?</p>
      <p>{{file}}</p>
      <template #footer>
        <Button label="Cancel" text @click="isDeleteModalVisible = false" />
        <Button label="OK" severity="primary" @click="deleteFile" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { useCommonStore } from '@/stores/common'
import getLongFormLabel from '@/common/helpers/getLongFormLabel'

export default {
  props: {
    well: {
      required: true
    }
  },
  data () {
    return {
      loading: true,
      files: null,
      error: null,
      file: '',
      fileType: '',
      splitFiles: [],
      isDeleteModalVisible: false
    }
  },
  watch: {
    // This is not ideal. If you are authorized, we need to show you a different set of wells, however,
    // auth is happening asynchronously somewhere else on the page.
    keycloak: function () {
      if (this.well) {
        this.loadFiles()
      }
    }
  },
  computed: {
    commonStore () { return useCommonStore() }
  },
  methods: {
    // If file download is unsuccessful will retry up to 5 times or untill successful
    // and refresh component with the response
    async loadFiles () {
      let response
      let retryAttempt
      for (retryAttempt = 0; retryAttempt < 5; retryAttempt++) {
        try {
          response = await ApiService.query('wells/' + this.well + '/files')
          if (response) {
            this.files = response.data
            this.error = null
            break
          }
        } catch (e) {
          console.log(`Attempting retry: ${retryAttempt + 1}`)
          this.error = 'Document download failure. Attempting Retry'
          console.error(e)
        }
      }
      if (retryAttempt === 5) {
        this.error = 'Unable to retrieve files'
      }
      this.loading = false
    },

    callLongFormLabel (shortFormLabel) {
      return getLongFormLabel(shortFormLabel)
    },
    showModal () {
      this.isDeleteModalVisible = true
    },
    hideModal () {
      this.isDeleteModalVisible = false
    },
    confirmDeleteFile (file, fileType, e) {
      e.preventDefault()
      this.file = file
      this.fileType = fileType
      this.showModal()
    },
    deleteFile () {
      const isPrivate = this.fileType === 'private'

      ApiService.deleteFile(`wells/${this.wellTag}/delete_document?filename=${this.file}&private=${isPrivate}`)
    }
  },
  created () {
    this.loadFiles()
  }
}
</script>

<style lang="scss" scoped>
</style>
