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
  <b-card no-body class="p-3 mb-4">
    <api-error v-if="error" :error="error"/>
    <b-alert show v-if="files_uploading">File Upload In Progress...</b-alert>
    <b-alert show v-if="!files_uploading && file_upload_error" variant="warning" >
      There was an error uploading the files
    </b-alert>
    <b-alert show v-if="!files_uploading && file_upload_success" variant="success" >
      Successfully uploaded all files
    </b-alert>
    <b-alert variant="success" :show="showSaveSuccess" id="aquifer-success-alert">
      Record successfully updated.
    </b-alert>
    <b-container>
      <b-row v-if="loading" class="border-bottom mb-3 pb-2">
        <b-col><h5>Loading...</h5></b-col>
      </b-row>

      <b-row v-if="editMode && !loading" class="border-bottom mb-3 pb-2">
        <b-col><h4>Aquifer {{record.aquifer_id}} Summary - Edit</h4></b-col>
      </b-row>

      <b-row v-if="viewMode" class="border-bottom mb-3 pb-2">
        <b-col><h4 class="pt-2">Aquifer Summary</h4></b-col>
        <b-col cols="auto">
          <b-button
            variant="default"
            v-if="userRoles.aquifers.edit"
            v-on:click.prevent="navigateToEdit">
            <span title="Edit" class="fa fa-edit"/> Edit
          </b-button>
          <a class="ml-2 print fa fa-print fa-lg d-print-none"
            href="#"
            title="Print"
            v-on:click.prevent="print"
           />
        </b-col>
      </b-row>

      <aquifer-form
        v-on:save="save"
        v-on:cancel="navigateToView"
        :fieldErrors="fieldErrors"
        :record="record"
        showId
        v-if="editMode"
        />

      <dl v-if="viewMode" class="row">
        <dt class="col-sm-2">Aquifer number</dt>
        <dd class="col-sm-4" id="aquifer-view-number">{{record.aquifer_id}}</dd>
        <dt class="col-sm-2">Year of mapping</dt>
        <dd class="col-sm-4">{{record.mapping_year}}</dd>

        <dt class="col-sm-2">Aquifer name</dt>
        <dd class="col-sm-4" id="aquifer-view-name">{{record.aquifer_name}}</dd>
        <dt class="col-sm-2">Litho stratigraphic unit</dt>
        <dd class="col-sm-4">{{record.litho_stratographic_unit}}</dd>

        <dt class="col-sm-2">Descriptive location</dt>
        <dd class="col-sm-4">{{record.location_description}}</dd>
        <dt class="col-sm-2">Vulnerability</dt>
        <dd class="col-sm-4">{{record.vulnerability_description}}</dd>

        <dt class="col-sm-2">Material type</dt>
        <dd class="col-sm-4">{{record.material_description}}</dd>
        <dt class="col-sm-2">Subtype</dt>
        <dd class="col-sm-4">{{record.subtype_description}}</dd>

        <dt class="col-sm-2">Quality concerns</dt>
        <dd class="col-sm-4">{{record.quality_concern_description}}</dd>
        <dt class="col-sm-2">Productivity</dt>
        <dd class="col-sm-4">{{record.productivity_description}}</dd>

        <dt class="col-sm-2">Size (km²)</dt>
        <dd class="col-sm-4">{{record.area}}</dd>
        <dt class="col-sm-2">Demand</dt>
        <dd class="col-sm-4">{{record.demand_description}}</dd>
      </dl>
      <h5 class="mt-3 border-bottom">Documentation</h5>
      <aquifer-documents :files="aquiferFiles"
        :editMode="editMode"
        :id="this.id"
        v-on:fetchFiles="fetchFiles"></aquifer-documents>
      <change-history v-if="userRoles.aquifers.edit" class="mt-5" :id="id" resource="aquifers" ref="aquiferHistory"/>
    </b-container>
  </b-card>
</template>

<style>
.print, .print:hover {
  color: black;
  text-decoration: none;
}
</style>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import AquiferForm from './Form'
import Documents from './Documents.vue'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm,
    'aquifer-documents': Documents,
    ChangeHistory
  },
  props: {
    'edit': Boolean
  },
  created () {
    this.fetch()
    this.fetchFiles()
  },
  data () {
    return {
      error: undefined,
      fieldErrors: {},
      loading: false,
      record: {},
      showSaveSuccess: false,
      aquiferFiles: {}
    }
  },
  computed: {
    id () { return this.$route.params.id },
    editMode () { return this.edit },
    viewMode () { return !this.edit },
    ...mapGetters(['userRoles']),
    ...mapState('documentState', [
      'files_uploading',
      'file_upload_error',
      'file_upload_success',
      'upload_files'
    ])
  },
  watch: {
    id () {
      this.fetch()
    }
  },
  methods: {
    ...mapActions('documentState', [
      'uploadFiles',
      'fileUploadSuccess'
    ]),
    handleSaveSuccess () {
      this.fetch()
      this.navigateToView()
      if (this.$refs.aquiferHistory) {
        this.$refs.aquiferHistory.update()
      }
      this.showSaveSuccess = true

      if (this.upload_files.length > 0) {
        this.uploadFiles({
          documentType: 'aquifers',
          recordId: this.id
        }).then(() => {
          this.fileUploadSuccess()
          this.fetchFiles()
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    handlePatchError (error) {
      if (error.response) {
        if (error.response.status === 400) {
          this.fieldErrors = error.response.data
        } else {
          this.error = error.response
        }
      } else {
        this.error = error.message
      }
    },
    save () {
      this.showSaveSuccess = false
      this.fieldErrors = {}

      ApiService.patch('aquifers', this.id, this.record)
        .then(this.handleSaveSuccess)
        .catch(this.handlePatchError)
    },
    navigateToView () {
      this.$router.push({ name: 'view', params: { id: this.id } })
    },
    navigateToEdit () {
      this.showSaveSuccess = false
      this.$router.push({ name: 'edit', params: { id: this.id } })
    },
    print () {
      window.print()
    },
    fetch (id = this.id) {
      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        })
    },
    fetchFiles (id = this.id) {
      ApiService.query(`aquifers/${id}/files`)
        .then((response) => {
          this.aquiferFiles = response.data
        })
    }
  }
}
</script>
