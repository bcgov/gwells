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
      <p>{{file}}</p>
    </b-modal>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { mapActions, mapGetters } from 'vuex'

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
      fileType: ''
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
    loadFiles () {
      ApiService.query('wells/' + this.well + '/files').then((response) => {
        this.files = response.data
      }).catch((e) => {
        console.error(e)
        this.error = 'Unable to retrieve file list.'
      }).finally(() => {
        this.loading = false
      })
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
