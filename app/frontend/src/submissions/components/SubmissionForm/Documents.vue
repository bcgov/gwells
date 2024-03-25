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
    <div v-if="uploadedFiles && uploadedFiles.private && uploadedFiles.public" class="table-responsive">
      <b-table
          hover
          :fields="['well_number', 'document_type', 'date_of_upload', 'document_status', 'uploaded_document', 'delete']"
          striped
          :items="[...uploadedFiles.public, ...uploadedFiles.private]"
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
          <template v-slot:cell(delete)="data">
            <a
              class="fa fa-trash fa-lg"
              variant="primary"
              style="margin-left: .5em"
              href="#"
              @click="handleFileDelete(data.item.name, data.item.document_status, $event)"></a>
          </template>
      </b-table>
    </div>
    <div v-else>
      No documents available
    </div>
    <div class="table-responsive" id="attachmentsTable" v-if="attachmentsData">
      <table class="table table-sm" aria-describedby="attachmentsDetails">
        <thead>
          <tr>
            <th class="font-weight-normal">Well Number</th>
            <th class="font-weight-normal">Document Type</th>
            <th class="font-weight-normal">File</th>
            <th class="font-weight-normal">Private Document?</th>
            <th class="font-weight-normal">New File Name</th>
            <th class="font-weight-normal">Date of Upload</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(attachment, index) in attachmentsData" :key="index">
            <td class="p-3">
                {{ attachment.well_tag_number = wellTagNumber }}
            </td>
            <td>
              <!-- Document Selector -->
              <b-form-group
                :id="'attachmentLabel_' + index"
                class="mt-1 mb-0"
                :aria-describedby="`attachmentLabelInvalidFeedback${index}`">
                <b-form-select
                    @change="setFileName(index)"
                    v-model="attachment.document_code"
                    :options="WELL_TAGS"
                    :state="getAttachmentError(index).document_code ? false : null"
                    size="med"   
                >    
                </b-form-select>
                <b-form-invalid-feedback :id="`attachmentCodeInvalidFeedback${index}`">
                  <div v-for="(error, error_index) in getAttachmentError(index).document_code" :key="`Document Type input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td>
              <!-- File Upload -->
              <b-form-file
                @input="setFileName(index)"
                accept=".jpg, .png, .jpeg, .pdf, .docx, .csv"
                class="mt-1 mb-0"
                v-model="attachment.file"
                :errors="getAttachmentError(index).file"
                :loaded="getFieldsLoaded(index).file"
              />
            </td>
           <!-- Privacy Flag  -->
           <td>
              <b-form-checkbox
                class="mt-2 ml-3"
                v-model="attachment.private"
                :loaded="getFieldsLoaded(index).private"
              />
            </td>
            <td>
              <!-- File Name -->
              <b-form-input
                class="mt-1 mb-0"
                v-model="attachment.file_name"
                placeholder="File_Name"
                :errors="getAttachmentError(index).file_name"
                :loaded="getFieldsLoaded(index).file_name"
                disabled
              />
            </td>
            <!-- Date -->
            <td class="p-2">
              {{ new Date().toLocaleDateString() }}
            </td>
            <td class="pt-1 py-0">
              <b-btn size="sm" variant="primary" :id="`removeAttachmentRowBtn${index}`" @click="removeRowIfOk(attachment)" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i>&nbsp;Remove</b-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" id="addAttachmentRowBtn" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i>&nbsp;Add file</b-btn>
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
  </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex'
import { omit } from 'lodash'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'
import { WELL_TAGS } from '@/common/constants.js'
import getLongFormLabel from '@/common/helpers/getLongFormLabel.js';

export default {
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    wellTagNumber: null,
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
      isInput: false,
      default: {},
    },
    showDocuments: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      status: 'False',
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      attachmentsData: [],
      WELL_TAGS: WELL_TAGS,
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
    },
    computedAttachments () {
      return this.attachmentsData || [];
    },
  },
  watch: {
    computedAttachments: {
      deep: true,
      handler: function (newAttachments, oldAttachments) {
        let jsonNewAttachments = newAttachments;
        // We have at least one new attachment
        if (jsonNewAttachments[0].file) {
          jsonNewAttachments.forEach((newAttachment, index) => {

            // Add the new attachment
            const newFile = newAttachment.file;
            if (newAttachment.file_name) {
              const uploadName = newAttachment.file_name.replace(/^WTN\s\d+_/,'');
              const newFileAdded = new File([newFile], uploadName, { type: newFile.type });
              this.files[index] = { file: newFileAdded, private: this.attachmentsData[index].private };
            }
          });
        }
      },
    },
  },
  created () {
    // When component created, add an initial row of attachments.
    if(this.attachments && this.attachments.length > 0){
      this.attachments.forEach((attachment) => {
        this.attachmentsData.push({ ...attachment })
      })
    }
    this.addRow()
  },
  methods: {
    ...mapMutations('documentState', [
      'setFiles',
      'setPrivate',
      'removeFile'
    ]),
    handleFileDelete(value, doc_status, e) {
      e.preventDefault()
      let tag = this.form.well && isNaN(this.form.well) ? this.form.well.well_tag_number : this.form.well;
      let encodedFileName = encodeURIComponent(value);
      if(confirm(`Are you sure you want to delete file: \n${value}`)){
        ApiService.deleteFile(`wells/${tag}/delete_document?filename=${encodedFileName}&private=${doc_status}`)
          .then(() => {
            const splitFile = value.split("_");
            const splitFileName = splitFile.length > 3 ? `${splitFile[1]}_${splitFile[2]}` : splitFile[1];
            ApiService.decrementFileCount(`wells/${tag}`, splitFileName);
            this.$emit('fetchFiles');
          })
      }
    },
    /**
     * @desc Updated the filename of an upload object if the user has filled in all the fields
     * @param {number} index of the item being modified
     */
    setFileName(index) {
      try {
        let file_name = null
        let WTN = this.wellTagNumber ? `WTN ${this.wellTagNumber}_` : ''
        let entry = this.attachmentsData[index];
        if (entry.document_code &&
            entry.upload_date &&
            entry.file){
          file_name =  `${WTN}${entry.document_code}_${entry.upload_date}.${entry.file.name.split('.')[1]}`;
        }
        this.attachmentsData[index].file_name = file_name;
        if(this.attachmentsData[index].file_name !== null){ this.$emit('setFormValueChanged'); }
      } catch (ex) {
        console.log(ex);
      }
    },
    callLongFormLabel(label){
      return getLongFormLabel(label);
    },
    /**
     * @desc Add new entry to the users list of uploaded files
     */
    addRow () {
      this.attachmentsData.push(this.emptyObject())
    },
    /**
     * @desc Object factory for uploaded files
     */
    emptyObject () {
      return {
        well_tag_number: null,
        document_code: null,
        upload_date: Date.now(),
        file_name: null,
        file: null,
        private: false,
      }
    },
    /**
     * @desc remove an uploaded file entry from the attachmentsData array
     * @param {number} index of the row to remove
     */
    removeRowByIndex (index) {
      this.attachmentsData.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (instance) {
      const index = this.attachmentsData.findIndex(item => item === instance)
      if (this.rowHasValues(this.attachmentsData[index])) {
        this.rowIndexToRemove = index
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(index)
      }
    },
    toggleAttachmentLengthRequired (index) {
      const instance = this.attachmentsData[index]
      instance.length_required = !instance.length_required
      Vue.set(this.attachmentsData, index, instance)
    },
    getAttachmentError (index) {
      return this.errors && 'attachment_set' in this.errors && index in this.errors['attachment_set']
        ? this.errors['attachment_set'][index]
        : {}
    },
    getFieldsLoaded (index) {
      return this.fieldsLoaded && 'attachment_set' in this.fieldsLoaded && index in this.fieldsLoaded['attachment_set']
        ? this.fieldsLoaded['attachment_set'][index]
        : {}
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      return keys.length === 0 ? false : !this.attachmentIsEmpty(row);
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    attachmentIsEmpty (attachment) {
      const fieldsToTest = omit(attachment, 'length_required')
      return Object.values(fieldsToTest).every((x) => !x)
    },
  }
}
</script>

<style scoped>

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
  #attachmentsTable { 
    overflow-x: visible !important;
  }
</style>
