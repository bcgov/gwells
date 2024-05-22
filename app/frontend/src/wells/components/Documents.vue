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
    <div v-else class="mt-3">
      <!-- public documents -->
      <div v-if="error">
        {{error}}
      </div>
        <b-table
            hover
            :fields="['well_number', 'document_type', 'date_of_upload', 'document_status', 'uploaded_document']"
            striped
            :items="files.private ? [...files.public, ...files.private] : [...files.public]"
          >
            <template v-slot:cell(document_type)="data">
              {{ callLongFormLabel(data.item.document_type) }}
            </template>
            <template v-slot:cell(date_of_upload)="data">
              {{ data.item.date_of_upload !== -1 ? new Date(data.item.date_of_upload).toLocaleDateString() : "Date Unknown" }}
            </template>
            <template v-slot:cell(uploaded_document)="data">
              <a :href="data.item.url" :download="data.item.name" target="_blank">{{ data.item.name }}</a>
            </template>
            <template v-slot:cell(document_status)="data">
              <p v-if="data.item.document_status">Private Document</p>
              <p v-else>Public Document</p>
            </template>
        </b-table>
    </div>
    <b-modal
      ok-variant="primary"
      cancel-variant="default"
      v-on:ok="deleteFile"
      ref="deleteModal" >
      <p>Are you sure you would like to delete this file?</p>
      <p>{{ file }}</p>
    </b-modal>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { mapActions, mapGetters } from 'vuex'
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
    ...mapGetters(['userRoles', 'keycloak'])
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

    ...mapActions('documentState',
      ['removeFileFromStore']
    ),
    callLongFormLabel(shortFormLabel) {
      return getLongFormLabel(shortFormLabel);
    },
    showModal () {
      this.$refs.deleteModal.show()
    },
    hideModal () {
      this.$refs.deleteModal.hide()
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
        .then(() => {
          this.removeFileFromStore(this.file)
        })
    }
  },
  created () {
    this.loadFiles()
  }
}
</script>

<style lang="scss" scoped>
</style>
