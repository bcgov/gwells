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
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive" id="attachmentsTable">
      <table class="table table-sm" aria-describedby="attachmentsDetails">
        <thead>
          <tr>
            <th class="font-weight-normal">Well Number</th>
            <th class="font-weight-normal">Well Label/Type</th>
            <th class="font-weight-normal">Date</th>
            <th class="font-weight-normal">File Upload Name</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(attachment, index) in upload_files" :key="index">
            <td>
              <b-form-input
                disabled
                inline
                class="mr-0 mt-2"/>
                Well Number
            </td>
            <td>
              Well Label/Type
            </td>
            <td>
              Date
            </td>
            <td>
              {{attachment.name}}
            </td>
            <td class="pt-1 py-0">
              <b-btn size="sm" variant="primary" :id="`removeAttachmentRowBtn${index}`" @click="removeUploadFile(attachment, $event)" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" id="addAttachmentRowBtn" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i> Add file</b-btn>
    <b-modal
        v-model="confirmRemoveModal"
        centered
        title="Confirm remove"
        @shown="focusRemoveModal">
      Are you sure you want to remove this row?
      <div slot="modal-footer">
        <b-btn variant="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn">
          Cancel
        </b-btn>
        <b-btn variant="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)">
          Remove
        </b-btn>
      </div>
    </b-modal>
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

import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
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
      fileType: '',
      rowIndexToRemove: null,
      confirmRemoveModal: false,
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
      'setPrivate',
      'removeFile'
    ]),
    showModal () {
      this.$refs.deleteModal.show()
    },
    hideModal () {
      this.$refs.deleteModal.hide()
    },
    removeUploadFile (file, e) {
      e.preventDefault()
      this.removeFile(file)
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

      let tag = this.form.well && isNaN(this.form.well) ? this.form.well.well_tag_number : this.form.well

      let encodedFileName = encodeURIComponent(this.file)

      ApiService.deleteFile(`wells/${tag}/delete_document?filename=${encodedFileName}&private=${isPrivate}`)
        .then(() => {
          this.$emit('fetchFiles')
        })
    },

    addRow () {
      console.log('add row')
      // this.files.push(emptyObject())
    },
    removeRowByIndex (index) {
      // this.casingsData.splice(index, 1)
      // this.rowIndexToRemove = null
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    }
  }
}
</script>

<style>

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

</style>
