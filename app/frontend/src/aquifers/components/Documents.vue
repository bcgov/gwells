<template>
  <div id="aquifer-documents">
    <div v-if="loading" class="row no-gutters">
      <div class="col-md-12">
        Loading documents...
        <div class="fa-2x text-center">
          <i class="fa fa-circle-o-notch fa-spin"></i>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="row no-gutters mt-3">
        <div class="col-md-12">
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
              No additional documentation currently available for this aquifer.
          </div>
        </div>
        <div class="row no-gutters">
          <div class="col-md-12">
            <h4>Internal documentation - authorized access only</h4>
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
                No additional private documentation currently available for this well.
              </div>
          </div>
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
    }
  },
  data () {
    return {
      loading: false,
      error: null,
      file: '',
      fileType: ''
    }
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
      ApiService.deleteFile(`aquifers/${this.id}/delete_document?filename=${this.file}&private=${isPrivate}`)
        .then(() => {
          this.$emit('fetchFiles')
        })
    }
  }
}
</script>

<style lang="scss">
</style>
