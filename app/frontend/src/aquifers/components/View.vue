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
  <b-card class="container container-wide p-1">
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

      <b-row v-if="viewMode">
        <b-col class="aquifer-detail" cols="12" md="4">
          <dt class="col-sm-6">Aquifer number</dt>
          <dd class="col-sm-5" id="aquifer-view-number">{{record.aquifer_id}}</dd>
          <dt class="col-sm-6">Year of mapping</dt>
          <dd class="col-sm-5">{{record.mapping_year}}</dd>

          <dt class="col-sm-6">Aquifer name</dt>
          <dd class="col-sm-5" id="aquifer-view-name">{{record.aquifer_name}}</dd>
          <dt class="col-sm-6">Litho stratigraphic unit</dt>
          <dd class="col-sm-5">{{record.litho_stratographic_unit}}</dd>

          <dt class="col-sm-6">Descriptive location</dt>
          <dd class="col-sm-5">{{record.location_description}}</dd>
          <dt class="col-sm-6">Vulnerability</dt>
          <dd class="col-sm-5">{{record.vulnerability_description}}</dd>

          <dt class="col-sm-6">Material type</dt>
          <dd class="col-sm-5">{{record.material_description}}</dd>
          <dt class="col-sm-6">Subtype</dt>
          <dd class="col-sm-5">{{record.subtype_description}}</dd>

          <dt class="col-sm-6">Quality concerns</dt>
          <dd class="col-sm-5">{{record.quality_concern_description}}</dd>
          <dt class="col-sm-6">Productivity</dt>
          <dd class="col-sm-5">{{record.productivity_description}}</dd>

          <dt class="col-sm-6">Size (km²)</dt>
          <dd class="col-sm-5">{{record.area}}</dd>
          <dt class="col-sm-6">Demand</dt>
          <dd class="col-sm-5">{{record.demand_description}}</dd>
        </b-col>
        <b-col cols="12" md="8">
          <single-aquifer-map v-bind:geom="record.geom"/>
        </b-col>
      </b-row>

      <b-row v-if="viewMode">
        <b-col>
          <h5 class="mt-3 border-bottom">Licensing Information</h5>
          <h5 class="mt-3 border-bottom">Well Information</h5>
        </b-col>
        <b-col>
          <h5 class="mt-3 border-bottom">Knowledge Indicators</h5>
          <div :key="section.id" v-for="(section, index) in aquifer_resource_sections">
            <div class="artesian-conditions" v-if="index === 1">
              <h6 class="mt-2 font-weight-bold">Artesian Conditions</h6>
              <a @click="handleArtesianSearch">[#] artesian wells in aquifer</a>
            </div>
            <div class="observational-wells" v-if="index === 2">
              <h6 class="mt-2 font-weight-bold">Observational Wells</h6>
              <a :href="getWellLink()">Observation Well 20402</a>
              <p>Water Level Analysis: <a :href="getAnalysisLink()">Increasing</a></p>
            </div>
            <h6 class="mt-4">{{ section.name }}</h6>
            <ul :key="resource.id" v-for="resource in bySection(record.resources, section)">
              <li><a :href="resource.url">{{ resource.name }}</a></li>
            </ul>
            <p v-if="!bySection(record.resources, section).length">No information available.</p>
          </div>
          <div>
          </div>
        </b-col>
        <b-col>
          <aquifer-map/>
        </b-col>
      </b-row>
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
.aquifer-detail dt,
.aquifer-detail dd {
  display: inline-block;
  vertical-align: top;
  margin-bottom: 9px;
}
.artesian-search {
  cursor: pointer;
}

a {
  text-decoration-skip-ink: none;
}
</style>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import AquiferForm from './Form'
import Documents from './Documents.vue'
import SingleAquiferMap from './SingleAquiferMap.vue'
import AquiferMap from './AquiferMap.vue'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import { mapActions, mapGetters, mapState } from 'vuex'
export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm,
    'aquifer-documents': Documents,
    'aquifer-map': AquiferMap,
    ChangeHistory
  },
  props: {
    'edit': Boolean
  },
  created () {
    this.fetch()
    this.fetchFiles()
    this.fetchResourceSections()
  },
  data () {
    return {
      error: undefined,
      fieldErrors: {},
      loading: false,
      record: {},
      showSaveSuccess: false,
      aquiferFiles: {},
      aquifer_resource_sections: [],
      wells: []
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
      'upload_files',
      'shapeFile'
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
      'uploadShapeFile',
      'fileUploadSuccess',
      'fileUploadFail'
    ]),
    fetchWells (id = this.id) {
      ApiService.query(`aquifers/${id}/details`)
        .then((response) => {
          this.wells = response.data
        }).catch((error) => {
          console.error(error)
        })
      this.wells = [{id: 20402}]
    },
    handleArtesianSearch () {
      this.$router.push({
        name: 'wells-home',
        query: {
          'match_any': false,
          'aquifer': this.id,
          'artesian_flow_has_value': true,
          'artesian_pressure_has_value': true
        },
        hash: '#advanced'
      })
    },
    bySection (resources, section) {
      return (resources || []).filter(function (resource) {
        return resource.section_code === section.code
      })
    },
    handleArtesianSearch () {
      this.$router.push({
        name: 'wells-home',
        query: {
          'match_any': false,
          'aquifer': this.id,
          'artesian_flow_has_value': true,
          'artesian_pressure_has_value': true
        },
        hash: '#advanced'
      })
    },
    handleSaveSuccess (response) {
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
          this.fileUploadFail()
          console.log(error)
        })
      }

      if (this.shapeFile) {
        console.log('Shape File Exists')
        console.log(this.shapeFile)
        this.uploadShapeFile({
          documentType: 'aquifers',
          recordId: this.id
        })
      } else {
        console.log('Shape file does not exist')
        console.log(this.shapeFile)
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
      console.log('Attempt to get file from child')
      console.log(AquiferForm.data())
      this.showSaveSuccess = false
      this.fieldErrors = {}
      ApiService.patch('aquifers', this.id, this.record)
        .then(this.handleSaveSuccess)
        .catch(this.handlePatchError)
    },
    navigateToView () {
      this.$router.push({ name: 'aquifers-view', params: { id: this.id } })
    },
    navigateToEdit () {
      this.showSaveSuccess = false
      this.$router.push({ name: 'aquifers-edit', params: { id: this.id } })
    },
    print () {
      window.print()
    },
    fetch (id = this.id) {
      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        }).catch((error) => {
          console.error(error)
        })
    },
    fetchFiles (id = this.id) {
      ApiService.query(`aquifers/${id}/files`)
        .then((response) => {
          this.aquiferFiles = response.data
        })
    },
    fetchResourceSections () {
      ApiService.query('aquifers/sections').then((response) => {
        this.aquifer_resource_sections = response.data.results
      })
    },
    getWellLink () {
      return 'https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20402'
    },
    getAnalysisLink () {
      return 'http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html'
    }
  }
}
</script>
