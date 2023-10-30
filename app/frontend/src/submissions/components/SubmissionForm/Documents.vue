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
            <th class="font-weight-normal">File Name</th>
            <th class="font-weight-normal">File</th>
            <th class="font-weight-normal">Private?</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(attachment, index) in attachmentsData" :key="index">
            <td class="p-3">
                {{ attachment.well_tag_number = wellTagNumber }}
            </td>
            <td>
              <!-- Label Selector -->
              <b-form-group
                :id="'attachmentLabel_' + index"
                class="mt-1 mb-0"
                :aria-describedby="`attachmentLabelInvalidFeedback${index}`">
                <b-form-select
                    @change="setFileName(index)"
                    v-model="attachment.document_label_code"
                    :options="codes.document_label_codes"
                    value-field="code"
                    text-field="description"
                    :state="getAttachmentError(index).document_label_code ? false : null">
                  <template slot="first">
                    <option :value="null" enabled>Select a label</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback :id="`attachmentCodeInvalidFeedback${index}`">
                  <div v-for="(error, error_index) in getAttachmentError(index).document_label_code" :key="`Label input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td class="p-2">
              <!-- Date -->
              {{ new Date(attachment.upload_date).toLocaleDateString() }}<br />{{ new Date(attachment.upload_date).toLocaleTimeString() }}
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
            <td>
              <!-- File Upload -->
              <b-form-file
                @input="setFileName(index)"
                class="mt-1 mb-0"
                v-model="attachment.file"
                :errors="getAttachmentError(index).file"
                :loaded="getFieldsLoaded(index).file"
              />
            </td>
            <td>
              <b-form-checkbox
                class="mt-2 ml-3"
                id="checkbox"
                v-model="attachment.private"
                name="checkbox"
                value="private"
                unchecked-value="public"
              />
            </td>
            <td class="pt-1 py-0">
              <b-btn size="sm" variant="primary" :id="`removeAttachmentRowBtn${index}`" @click="removeRowIfOk(attachment)" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { omit } from 'lodash'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
// import ApiService from '@/common/services/ApiService.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

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
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      attachmentsData: [],
    }
  },
  computed: {
    ...mapGetters(['codes', 'userRoles']),
    computedAttachments () {
      return [...this.attachmentsData]
    }
  },
  watch: {
    computedAttachments: {
      deep: true,
      handler: function (n, o) {
        const attachments = this.attachmentsData.filter((d) => !this.attachmentIsEmpty(d))
        this.$emit('update:attachments', attachments)
      }
    }
  },
  created () {
    // When component created, add an initial row of attachments.
    if(this.attachments.length > 0){
      this.attachments.forEach((attachment) => {
        this.attachmentsData.push({ ...attachment })
      })
    }
    this.addRow()
  },
  methods: {
    setFileName(index) {
      console.log("Filename called")
      try {
        let file_name = ""
        let entry = this.attachmentsData[index];
        if (entry.document_label_code &&
            entry.upload_date &&
            entry.file){
          file_name =  `WTN ${entry.well_tag_number}_${entry.document_label_code}_${entry.upload_date}.${entry.file.name.split('.')[1]}`;
        }
        this.attachmentsData[index].file_name = file_name;
      } catch (ex) {
        console.log(ex);
      }
    },
    addRow () {
      console.log('attachmentsData --->', this.attachmentsData)

      this.attachmentsData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        well_tag_number: null,
        document_label_code: null,
        upload_date: Date.now(),
        file_name: null,
        file: null,
        private: false,
      }
    },
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
      if (this.errors && 'attachment_set' in this.errors && index in this.errors['attachment_set']) {
        return this.errors['attachment_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'attachment_set' in this.fieldsLoaded && index in this.fieldsLoaded['attachment_set']) {
        return this.fieldsLoaded['attachment_set'][index]
      }
      return {}
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      if (keys.length === 0) return false
      // Check that all fields are not empty.
      return !this.attachmentIsEmpty(row)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    attachmentIsEmpty (attachment) {
      const fieldsToTest = omit(attachment, 'length_required')
      return Object.values(fieldsToTest).every((x) => !x)
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
