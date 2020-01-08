<template>
  <div id="aquifer-documents">
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
          <a :href="file.url" :download="file.name" target="_blank">{{file.name}}</a>
          <a class="fa fa-trash fa-lg"
            variant="primary"
            v-if="editMode"
            style="margin-left: .5em"
            href="#"
            v-on:click="confirmDeleteFile(file.name, 'public', $event)" />
        </li>
      </ul>
      <div v-else>
        No additional documentation available for this aquifer.
      </div>
      <div class="internal-documents mt-5" v-if="userRoles.aquifers.edit">
        <h5>Internal documentation - authorized access only</h5>
        <div v-if="error">
          {{error}}
        </div>
        <ul v-else-if="files && files.private && files.private.length">
          <li v-for="(file, index) in files.private" :key="index">
            <a :href="file.url" :download="file.name" target="_blank">{{file.name}}</a>
            <a class="fa fa-trash fa-lg"
              variant="primary"
              v-if="editMode"
              style="margin-left: .5em"
              href="#"
              v-on:click="confirmDeleteFile(file.name, 'private', $event)" />
          </li>
        </ul>
        <div v-else>
          No additional private documentation available for this aquifer.
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
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'AquiferDocuments',
  props: {
    files: {
      type: Object,
      default: null
    },
    id: {
      type: [String, Number],
      default: null
    },
    editMode: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      error: null,
      file: '',
      fileType: ''
    }
  },
  computed: {
    ...mapGetters(['userRoles'])
  },
  methods: {
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
      const url = `aquifers/${this.id}/delete_document?filename=${this.file}&private=${isPrivate}`
      ApiService.deleteFile(url).then(() => this.$emit('fetchFiles'))
    }
  }
}
</script>

<style lang="scss">
</style>
