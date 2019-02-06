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
    <fieldset>
      <b-row>
        <b-col cols="12" lg="6">
          <legend :id="id">Attachments</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <b-row class="mt-3">
        <b-col cols="12">
          <b-form-group
            label="Attachments"
            id="attachmentGroup">
            <b-form-file
              v-model="files"
              id="files"
              multiple
              plain/>
            <div class="mt-3">
              <b-form-checkbox
               id="isPrivateCheckbox"
               v-model="privateDocument">Are these documents private?</b-form-checkbox>
            </div>
            <div class="mt-3" v-if="upload_files.length > 0">
              <b-list-group>
                <b-list-group-item v-for="(f, index) in upload_files" :key="index">{{f.name}}</b-list-group-item>
              </b-list-group>
            </div>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row v-if="showDocuments">
        <b-col cols="12">
          <div class="row no-gutters mt-3">
            <div class="col-md-12">
              <!-- public documents -->
              <ul v-if="uploadedFiles && uploadedFiles.public && uploadedFiles.public.length">
                <li v-for="(file, index) in uploadedFiles.public" :key="index">
                  <a :href="file.url" :download="file.name" target="_blank">{{file.name}}</a>
                  <a class="fa fa-trash fa-lg"
                  variant="primary"
                  style="margin-left: .5em"
                  href="#"
                  v-on:click="confirmDeleteFile(file.name, 'public', $event)" />
                </li>
              </ul>
              <div v-else>
                  No additional documentation currently available for this well.
              </div>
            </div>
          </div>
          <div class="row no-gutters" v-if="userRoles.submissions.edit">
            <div class="col-md-12">
              <h4>Internal documentation - authorized access only</h4>
              <ul v-if="uploadedFiles && uploadedFiles.private && uploadedFiles.private.length">
                <li v-for="(file, index) in uploadedFiles.private" :key="index">
                  <a :href="file.url" :download="file.name" target="_blank">{{file.name}}</a>
                  <a class="fa fa-trash fa-lg"
                  variant="primary"
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
        </b-col>
      </b-row>
    </fieldset>
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
import { mapGetters, mapMutations, mapState } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'

export default {
  mixins: [inputBindingsMixin],
  props: {
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: String,
      isInput: false
    },
    form: {
      type: Object,
      isInput: null
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    },
    uploadedFiles: {
      type: Object,
      isInput: false
    },
    showDocuments: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      status: 'False',
      file: '',
      fileType: ''
    }
  },
  computed: {
    ...mapGetters(['codes', 'userRoles']),
    ...mapState('documentState', [
      'isPrivate',
      'upload_files'
    ]),
    files: {
      get: function () {
        return this.upload_files
      },
      set: function (value) {
        this.setFiles(value)
        this.$emit('setFormValueChanged')
      }
    },
    privateDocument: {
      get: function () {
        return this.isPrivate
      },
      set: function (value) {
        this.setPrivate(value)
      }
    }
  },
  methods: {
    ...mapMutations('documentState', [
      'setFiles',
      'setPrivate'
    ]),
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

      console.log(this.form)
      console.log(this.form.well)
      console.log(this.form.well.well_tag_number)

      let tag = this.form.well && isNaN(this.form.well) ? this.form.well.well_tag_number : this.form.well

      ApiService.deleteFile(`wells/${tag}/delete_document?filename=${this.file}&private=${isPrivate}`)
        .then(() => {
          this.$emit('fetchFiles')
        })
    }
  }
}
</script>

<style>

</style>
