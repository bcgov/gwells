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
      <ul v-else-if="files && files.public && files.public.length">
        <li v-for="(file, index) in files.public" :key="index">
          <a :href="file.url" :download="file.name" target="_blank" @click="handleDownloadEvent(file.name)">{{file.name}}</a>
        </li>
      </ul>
      <div v-else>
        No additional documentation available for this well.
      </div>
        <b-table
            hover
            :fields="['well_number', 'well_label', 'date_of_action', 'private', 'file']"
            striped
            :items="[...files.public, ...files.private]"
          >
            <template v-slot:cell(well_label)="data">
              {{ getLongFormLabel(data.item.well_label) }}
            </template>
            <template v-slot:cell(date_of_action)="data">
              {{ data.item.date_of_action !== -1 ? new Date(data.item.date_of_action).toLocaleDateString() : "Date Unknown" }}
            </template>
            <template v-slot:cell(file)="data">
              <a :href="data.item.url" target="_blank" @click="handleDownloadEvent(data.item.name)">{{ data.item.name }}</a>
            </template>
            <template v-slot:cell(private)="data">
              <p v-if="data.item.private">Private Document</p>
              <p v-else>Public Document</p>
            </template>
        </b-table>
      <div class="internal-documents mt-5" v-if="userRoles.wells.view">
        <h5>Internal documentation - authorized access only</h5>
        <div v-if="error">
          {{error}}
        </div>
        <ul v-else-if="files && files.private && files.private.length">
          <li v-for="(file, index) in files.private" :key="index">
            <a :href="file.url" :download="file.name" target="_blank" @click="handleDownloadEvent(file.name)">{{file.name}}</a>
          </li>
        </ul>
        <div v-else>
          No additional private documentation available for this well.
        </div>
      </div>
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
import { WELL_TAGS_PRIVATE, WELL_TAGS_PUBLIC } from '../../common/constants.js'
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
      WELL_TAGS: [...WELL_TAGS_PUBLIC, ...WELL_TAGS_PRIVATE],
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
    handleDownloadEvent (file) {
      if (window.ga) {
        // ga('send', 'event', 'Attachment', 'Accessed', 'Original Well Record')
        window.ga('send', {
          hitType: 'event',
          eventCategory: 'Attachment',
          eventAction: 'Accessed',
          eventLabel: `Original Well Record ${file}`
        })
      }
    },
    displayFileFormat() {
      const arr = [];
    },
    getLongFormLabel(shortFormLabel) {
      try {
        return this.WELL_TAGS.filter((item) => item.value === shortFormLabel)[0].text;
      } catch (ex) {
        return "Unknown"
      }
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
      this.hideModal()
      let isPrivate = false
      if (this.fileType === 'private') {
        isPrivate = true
      }

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

<style lang="scss">
</style>
