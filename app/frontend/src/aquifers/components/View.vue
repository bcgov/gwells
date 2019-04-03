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
  <b-card class="container container-wide p-0 card-container pb-3" :class="{ 'p-4': editMode }">
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
    <b-container fluid>
      <b-row v-if="loading" class="border-bottom mb-3 pb-2">
        <b-col><h5>Loading...</h5></b-col>
      </b-row>

      <b-row v-if="editMode && !loading" class="border-bottom mb-3 pb-2">
        <b-col><h4>Aquifer {{record.aquifer_id}} Summary - Edit</h4></b-col>
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
        <b-col class="aquifer-detail" cols="12" md="5">
          <b-row>
            <b-col class="p-4">
              <div class="d-flex justify-content-between align-items-center">
              <h4 class="color-grey main-title mt-4">Aquifer {{ id }} Summary</h4>
                <div>
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
                </div>
              </div>
              <hr class="m-0 mt-2"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" sm="12" class="pl-4 pr-4">
              <ul class="m-0 p-0 aquifer-information-list">
              <div class="aquifer-information-list-divider"></div>
              <li>
                <dt>Aquifer number</dt>
                <dd id="aquifer-view-number">{{record.aquifer_id}}</dd>
              </li>
              <li>
                <dt>Year of mapping</dt>
                <dd>{{record.mapping_year}}</dd>
              </li>
              <li>
                <dt>Aquifer name</dt>
                <dd id="aquifer-view-name">{{record.aquifer_name}}</dd>
              </li>
              <li>
                <dt>Litho stratigraphic unit</dt>
                <dd>{{record.litho_stratographic_unit}}</dd>
              </li>
              <li>
                <dt>Descriptive location</dt>
                <dd>{{record.location_description}}</dd>
              </li>
              <li>
                <dt>Vulnerability</dt>
                <dd>{{record.vulnerability_description}}</dd>
              </li>
              <li>
                <dt>Material type</dt>
                <dd>{{record.material_description}}</dd>
              </li>
              <li>
                <dt>Subtype</dt>
                <dd>{{record.subtype_description}}</dd>
              </li>
              <li>
                <dt>Quality concerns</dt>
                <dd>{{record.quality_concern_description}}</dd>
              </li>
              <li>
                <dt>Productivity</dt>
                <dd>{{record.productivity_description}}</dd>
              </li>
              <li>
                <dt>Size (km²)</dt>
                <dd>{{record.area}}</dd>
              </li>
              <li>
                <dt>Demand</dt>
                <dd>{{record.demand_description}}</dd>
              </li>
              </ul>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="12" md="7" class="p-0">
          <single-aquifer-map v-bind:geom="record.geom"/>
        </b-col>
      </b-row>

      <b-row v-if="viewMode" class="mt-5">
        <b-col cols="4" >
          <h5 class="mt-3 border-bottom pb-4 main-title">Well Information</h5>
          <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li>
              <dt>Number of wells associated to the aquifer</dt>
              <dd><a @click="handleWellSearch()">{{ licence_details.num_wells }}</a></dd>
            </li>
          </ul>
          <h5 class="mt-5 border-bottom pb-4 main-title">Documentation</h5>
          <aquifer-documents :files="aquiferFiles"
            :editMode="editMode"
            :id="this.id"
            v-on:fetchFiles="fetchFiles">
          </aquifer-documents>
        </b-col>
        <b-col cols="4">
          <h5 class="mt-3 border-bottom pb-4 main-title">Licensing Information</h5>
          <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li>
              <dt>Number of groundwater licenses</dt>
              <dd>{{ licence_details.licence_count }}</dd>
            </li>
          </ul>
        </b-col>
        <b-col cols="4">
          <h5 class="mt-3 border-bottom pb-4 main-title">Knowledge Indicators</h5>
          <ul class="ml-0 mr-0 mb-0 mt-4 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
          <li :key="section.id" v-for="(section, index) in aquifer_resource_sections">
              <div class="artesian-conditions" v-if="index === 1">
                <dt>Artesian Conditions</dt>
                <dd @click="handleArtesianSearch()">{{ licence_details.num_artesian_wells }} artesian wells in aquifer</dd>
              </div>
              <div class="observational-wells" v-if="index === 2">
                <dt>Observational Wells</dt>
                <dd><p>Observation Well 20402<br/>Water Level Analysis: Increasing</p></dd>
              </div>
              <dt>{{ section.name }}</dt>
              <dd>
                <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                  <li><a :href="resource.url">{{ resource.name }}</a></li>
                </ul>
                <p v-if="!bySection(record.resources, section).length">No information available.</p>
              </dd>
          </li>
            
          </ul>
        </b-col>
        <b-col cols="12" sm="6">
          <change-history v-if="userRoles.aquifers.edit" class="mt-5" :id="id" resource="aquifers" ref="aquiferHistory"/>
        </b-col>
      </b-row>
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
  display: block;
}
.artesian-search {
  cursor: pointer;
}

a {
  text-decoration-skip-ink: none;
}

.card-container .card-body {
  padding: 0;
  margin: 0;
}

.color-grey {
  color: #494949
}

.main-title {
  padding-bottom: 1rem;
  font-size: 1.8em;
  color: #494949;
}

.aquifer-information-list {
  list-style-type: none;
  box-sizing: border-box;
  position: relative;
}

.aquifer-information-list > li {
  display: block;
  width: 100%;
  font-size: 0;
  margin: 0.3rem 0;
}
.aquifer-information-list dt,
.aquifer-information-list dd {
  display: inline-block;
  vertical-align: top;
  width: 50%;
  font-size: 1rem;
}

.aquifer-information-list dt {
  padding-right: 2rem;
}

.aquifer-information-list dd {
  padding-left: 2rem;
}

.aquifer-information-list-divider {
  position: absolute;
  top: 0;
  width: 1px;
  height: 100%;
  background-color: rgba(0,0,0,0.1);
  left: calc(50% - 0.5px);
}
</style>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import AquiferForm from './Form'
import Documents from './Documents.vue'
import SingleAquiferMap from './SingleAquiferMap.vue'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import { mapActions, mapGetters, mapState } from 'vuex'
export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm,
    'aquifer-documents': Documents,
    'single-aquifer-map': SingleAquiferMap,
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
      licence_details: {},
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
    bySection (resources, section) {
      return (resources || []).filter(function (resource) {
        return resource.section_code === section.code
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
          console.log(this.record)
          this.licence_details = response.data.licence_details
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
    handleWellSearch () {
      this.$router.push({
        path: '/',
        query: {
          'match_any': false,
          'search': '',
          'well': '',
          'aquifer': this.record.aquifer_id
        }
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
    }
  }}
</script>
