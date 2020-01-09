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
  <b-card class="container container-wide p-0 card-container pb-5" :class="{ 'p-4': editMode }">
    <api-error v-if="error" :error="error"/>
    <b-alert show v-if="files_uploading || shapefile_uploading">File Upload In Progress...</b-alert>
    <b-alert show v-if="!files_uploading && file_upload_error" variant="danger" >
      There was an error uploading the documents
    </b-alert>
    <b-alert show v-if="!files_uploading && file_upload_success" variant="success" >
      Successfully uploaded all documents
    </b-alert>
    <b-alert show v-if="shapefile_upload_success & !shapefile_uploading" variant="success" >
      Shapefile uploaded.
    </b-alert>
    <b-alert show v-if="!shapefile_upload_success & !shapefile_uploading && shapefile_upload_message" variant="danger" >
      There was an error uploading the shapefile: {{ shapefile_upload_message }}.
    </b-alert>
    <b-alert variant="success" :show="showSaveSuccess" id="aquifer-success-alert">
      Aquifer {{ id }}'s information successfully updated.
    </b-alert>
    <b-container fluid>
      <b-row v-if="editMode && !loading" class="border-bottom mb-3 pb-2">
        <b-col><h4>Aquifer {{record.aquifer_id}} Summary - Edit</h4></b-col>
      </b-row>
      <aquifer-form
        :fieldErrors="fieldErrors"
        :record="form"
        :files="aquiferFiles"
        :loadingFiles="loadingFiles"
        showId
        v-if="editMode"
        v-on:load="loadForm"
        v-on:save="save"
        v-on:cancel="navigateToView"
        v-on:fetchFiles="fetchFiles"
        />
      <change-history v-if="userRoles.aquifers.edit && editMode" class="mt-5" :id="id" resource="aquifers" ref="aquiferHistory"/>

      <b-row v-if="viewMode">
        <b-col class="aquifer-detail" cols="12" md="12" lg="5">
          <b-row>
            <b-col class="pt-0 pl-4 pb-4 pr-4">
              <div class="d-flex justify-content-between align-items-center">
              <h4 class="color-grey main-title mt-4">Aquifer {{ id }} Summary</h4>
                <div>
                <b-button
                  variant="default"
                  v-if="userRoles.aquifers.edit"
                  v-on:click.prevent="navigateToEdit">
                  <span title="Edit" class="fa fa-edit"/> Edit
                </b-button>
                <a class="ml-2 print-button fa fa-print fa-lg d-print-none"
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
            <b-col cols="12" sm="12" class="pl-4 pr-4 aquifer-main-information-list">
              <b-row>
                <b-col cols="6" md="3" lg="6">Aquifer number</b-col>
                <b-col cols="6" md="3" lg="6" id="aquifer-view-number">{{record.aquifer_id}}</b-col>
                <b-col cols="6" md="3" lg="6">Year of mapping</b-col>
                <b-col cols="6" md="3" lg="6">{{record.mapping_year}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="6" md="3" lg="6">Aquifer name</b-col>
                <b-col cols="6" md="3" lg="6" id="aquifer-view-name">{{record.aquifer_name}}</b-col>
                <b-col cols="6" md="3" lg="6">Litho stratigraphic unit</b-col>
                <b-col cols="6" md="3" lg="6">{{record.litho_stratographic_unit}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="6" md="3" lg="6">Descriptive location</b-col>
                <b-col cols="6" md="3" lg="6">{{record.location_description}}</b-col>
                <b-col cols="6" md="3" lg="6">Vulnerability</b-col>
                <b-col cols="6" md="3" lg="6">{{record.vulnerability}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="6" md="3" lg="6">Material type</b-col>
                <b-col cols="6" md="3" lg="6">{{record.material}}</b-col>
                <b-col cols="6" md="3" lg="6">Subtype</b-col>
                <b-col cols="6" md="3" lg="6">{{record.subtype}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="6" md="3" lg="6">Quality concerns</b-col>
                <b-col cols="6" md="3" lg="6">{{record.quality_concern}}</b-col>
                <b-col cols="6" md="3" lg="6">Productivity</b-col>
                <b-col cols="6" md="3" lg="6">{{record.productivity}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="6" md="3" lg="6">Size (km²)</b-col>
                <b-col cols="6" md="3" lg="6">{{record.area}}</b-col>
                <b-col cols="6" md="3" lg="6">Demand</b-col>
                <b-col cols="6" md="3" lg="6">{{record.demand}}</b-col>
              </b-row>
            </b-col>
          </b-row>
        </b-col>
        <b-col id="map-container" cols="12" md="12" lg="7" class="p-0">
          <map-loading-spinner :loading="loadingMap"/>

          <single-aquifer-map :aquifer-id="id" :geom="record.geom" :wells="wells" :key="mapKey" :loading="loadingMap"/>
        </b-col>
      </b-row>

      <b-row v-if="viewMode" class="mt-5 aquifer-details">
        <b-col cols="12" xl="4" lg="6">
          <h5 class="mt-3 border-bottom pb-4 main-title">Well Information</h5>
          <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li>
              <dt>Number of wells associated to the aquifer</dt>
              <dd class="m-0">
                <router-link :to="{ name: 'wells-home', query: {'match_any':false, 'aquifer': this.record.aquifer_id, 'search':'', 'well':''}}">
                  {{ licence_details.num_wells }}
                </router-link>
              </dd>
            </li>
            <li>
              <dt>Artesian wells</dt>
              <dd class="m-0">
                <router-link :to="{ name: 'wells-home', query: {'match_any':false, 'aquifer':this.id, 'artesian_flow_has_value':true}, hash: '#advanced'}">
                  {{ licence_details.num_artesian_wells }} artesian wells in aquifer
                </router-link>
              </dd>
            </li>
          </ul>
          <p><i v-if="licence_details.wells_updated">Well info last updated {{ licence_details.wells_updated.update_date__max|formatDate }}</i></p>
          <h5 class="mt-5 border-bottom pb-4 main-title">Documentation</h5>
          <aquifer-documents :files="aquiferFiles"
            :editMode="editMode"
            :id="this.id"
            :loading="loadingFiles"
            v-on:fetchFiles="fetchFiles">
          </aquifer-documents>
        </b-col>
        <b-col cols="12" xl="4" lg="6">
          <h5 class="mt-3 border-bottom pb-4 main-title">Licensing Information</h5>
          <div>
            <p>
              The licensing summaries should be considered estimates. Due to complexities in the structure
              of the licensing data, reported values should be confirmed through the
              <a href="https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main" target="_blank" class="d-print-url">
                e&#8209;licensing portal</a>.
            </p>
          </div>
          <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li>
              <dt>Number of groundwater licences</dt>
              <dd class="m-0">{{ licence_details.licence_count }}</dd>
            </li>
            <li>
              <dt>Water withdrawal volume (annual)</dt>
              <dd class="m-0" v-if="waterWithdrawlVolume">{{ waterWithdrawlVolume | unitWaterVolume}}</dd>
              <dd class="m-0" v-else>No information available.</dd>
            </li>
          </ul>
          <div v-if="licence_details.lic_qty.length > 0">
            <b-row class="pt-5">
              <b-col cols="12" md="6" lg="12" class="pb-5">
                <h5 class="pie-chart-title">Licensed volume by purpose</h5>
                <PieChart :chartData="licence_details.usage" class="mt-3"></PieChart>
              </b-col>
              <b-col cols="12" md="6" lg="12" class="pb-5">
                <h5 class="pie-chart-title">Number of licences by purpose</h5>
                <PieChart :chartData="licence_details.lic_qty" class="mt-3"></PieChart>
              </b-col>
            </b-row>
          </div>
          <b-table id="licenses" striped :items="licence_details.wells_by_licence">
            <template slot="licence_number" slot-scope="row">
              <a :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${row.item.licence_number}`" target="_blank">
                {{ row.item.licence_number }}
              </a>
            </template>
            <template slot="well_tag_numbers_in_licence" slot-scope="row">
              <ul class="p-0 m-0">
                <li v-for="wtn in row.item.well_tag_numbers_in_licence" :key="wtn">
                  <router-link :to="{ name: 'wells-detail', params: { id: wtn }}">{{ wtn }}</router-link>
                </li>
              </ul>
            </template>
          </b-table>
          <p><i v-if="licence_details.licences_updated && licence_details.licences_updated.update_date__max">Licence info last updated {{ licence_details.licences_updated.update_date__max|formatDate }}</i></p>
          <p>
            Licensing information is obtained from
            the <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" @click="handleOutboundLinkClicks('https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public')" target="_blank" class="d-print-url">
              Water Rights Licence - Public data layer
            </a>.
          </p>
          <p>
            Unique licenses are counted once for each aquifer that they are associated with.
          </p>
          <p>
            The total licensed volume is counted once for each licence (the total volume may
            be shared between wells if there are multiple wells in a licence). In cases where
            specific volumes are licensed for multiple purposes, individual volumes are summed.
          </p>
        </b-col>
        <b-col cols="12" xl="4" lg="6" class="knowledge-indicators">
          <h5 class="mt-3 border-bottom pb-4 main-title">Knowledge Indicators</h5>
          <ul class="ml-0 mr-0 mb-0 mt-4 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li :key="section.id" v-for="section in aquifer_resource_sections">
              <div class="observational-wells" v-if="section.key === 'obs-wells'">
                <dt class="text-right">Observation wells</dt>
                <dd class="m-0">
                  <div v-if="activeObsWells.length > 0">
                    <h6 class="border-bottom">Active</h6>
                    <ul class="p-0 m-0">
                      <li v-for="owell in activeObsWells" :key="owell.observation_well_number" :data-water-level="owell.waterLevels">
                        <a :href="getObservationWellLink(owell.observation_well_number)" target="_blank" class="d-print-url">
                          {{ owell.observation_well_number }}
                        </a>
                        <span v-if="owell.waterLevels">
                          Water Level Analysis:
                          <a :href="owell.hasLevelAnalysis ? 'http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html' : false" target="_blank" class="d-print-url">
                            {{ owell.waterLevels }}
                          </a>
                        </span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="inactiveObsWellsWithWaterLevel.length > 0 || inativeObsWellsWithOutWaterLevel.length > 0">
                    <h6 class="border-bottom mt-2">Inactive<br><small>(data may not be available)</small></h6>
                    <ul class="p-0 m-0">
                      <li v-for="owell in inactiveObsWellsWithWaterLevel" :key="owell.observation_well_number" :data-water-level="owell.waterLevels">
                        <a :href="getObservationWellLink(owell.observation_well_number)" target="_blank" class="d-print-url">
                          {{ owell.observation_well_number }}
                        </a>
                        <div v-if="owell.waterLevels">
                          Water Level Analysis:
                          <a :href="owell.hasLevelAnalysis ? 'http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html' : false" target="_blank" class="d-print-url">
                            {{ owell.waterLevels }}
                          </a>
                        </div>
                      </li>
                      <li v-if="inativeObsWellsWithOutWaterLevel.length > 0" class="obs-wells-wo-well-level">
                        No Water Level Analysis:
                        <span v-for="owell in inativeObsWellsWithOutWaterLevel" :key="owell.observation_well_number">
                          <a :href="getObservationWellLink(owell.observation_well_number)" target="_blank">{{ owell.observation_well_number }}</a>
                        </span>
                      </li>
                    </ul>
                  </div>
                  <div v-if="noObsWells">
                    No information available.
                  </div>
                </dd>
              </div>
              <div class="water-quality-information" v-else-if="section.key === 'water-quality'">
                <dt class="text-right">Water quality information</dt>
                <dd class="m-0">
                  <router-link :to="{ name: 'wells-home', query: {'match_any':false, 'ems_has_value':true, 'aquifer': id}, hash: '#advanced'}">
                    {{ licence_details['num_wells_with_ems'] }} wells with an EMS ID
                  </router-link>
                </dd>
              </div>
              <div class="aquifer-connected" v-else-if="section.key === 'aquifer-connected'">
                <dt class="text-right">Hydraulically connected (screening level)
                  <i id="aquiferConnectedInfo" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                  <b-popover
                    target="aquiferConnectedInfo"
                    triggers="hover focus"
                    content="Inferred based on aquifer subtype - not field verified."/>
                </dt>
                <dd class="m-0">{{ licence_details['hydraulically_connected'] ? "More likely" : "Less likely"}}</dd>
              </div>
              <div v-else>
                <dt class="text-right">{{ section.name }}</dt>
                <dd class="m-0">
                  <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                    <li><a :href="resource.url" @click="handleExternalResourceClicks" target="_blank" class="d-print-url">{{ resource.name }}</a></li>
                  </ul>
                  <p class="m-0" v-if="!bySection(record.resources, section).length">No information available.</p>
                </dd>
              </div>
            </li>
          </ul>
        </b-col>
      </b-row>
    </b-container>
  </b-card>
</template>

<style>
.print-button, .print-button:hover {
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

#map-container {
  position: relative;
}

.card-container .card-body {
  padding: 0;
  margin: 0;
}

.color-grey {
  color: #494949
}

.color-info {
  color: #38598a;
}

.main-title {
  padding-bottom: 1rem;
  font-size: 1.8em;
  color: #494949;
}

.aquifer-information-list {
  list-style: none;
  box-sizing: border-box;
  position: relative;
}

.aquifer-information-list-divider {
  position: absolute;
  top: 0;
  width: 1px;
  height: 100%;
  background-color: rgba(0,0,0,.1);
  left: 50%;
}

.aquifer-information-list > li {
  margin: 0.7rem 0;
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
  font-weight: bold;
}

.aquifer-information-list dd {
  padding-left: 2rem;
}

.pie-chart-title {
  font-weight: bold !important;
  font-size: 1rem !important;
}
.pie-chart-container {
  margin: 0 auto;
}

.aquifer-main-information-list .row > div {
  padding-bottom: 0.7rem;
}

.aquifer-main-information-list .row > :nth-child(odd) {
  font-weight: bold;
  border-right: 1px solid rgba(0,0,0,0.1);
}

.observational-wells .obs-wells-wo-well-level span:not(:last-child):after {
  content: ", ";
}

#licenses li {
  list-style: none;
  display: inline;
}

#licenses li:not(:last-child):after {
  content: ', ';
}

@media print {
  a:not(.d-print-url) {
    text-decoration: none !important;
  }

  a.d-print-url[href]::after {
    content: " (" attr(href) ") ";
    word-break: break-all;
  }

  .aquifer-information-list dt {
    width: 25%;
  }

  .aquifer-information-list dd {
    width: 75%;
  }

  .aquifer-main-information-list .row > :nth-child(odd) {
    border: none;
  }

  main {
    margin-bottom: 0 !important;
  }

  main > .card.container {
    padding-bottom: 0 !important;
  }

  body, main, .card, .aquifer-details {
    display: block !important;
  }
}
</style>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import AquiferForm from './Form'
import Documents from './Documents.vue'
import SingleAquiferMap from './SingleAquiferMap.vue'
import MapLoadingSpinner from './MapLoadingSpinner.vue'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import { sumBy, orderBy, groupBy, range } from 'lodash'
import PieChart from './PieChart.vue'
import * as Sentry from '@sentry/browser'

export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm,
    'aquifer-documents': Documents,
    'single-aquifer-map': SingleAquiferMap,
    'map-loading-spinner': MapLoadingSpinner,
    ChangeHistory,
    PieChart
  },
  props: {
    'edit': Boolean
  },
  created () {
    this.loadingMap = true

    Promise.all([
      this.fetch(),
      this.fetchWells()
    ]).then(() => {
      this.loadingMap = false
    })

    this.fetchFiles()
  },
  data () {
    return {
      mapKey: 0, // component key to force updates.
      error: undefined,
      fieldErrors: {},
      loading: false,
      loadingFiles: false,
      loadingMap: false,
      record: {},
      form: {},
      licence_details: {
        usage: [],
        lic_qty: []
      },
      showSaveSuccess: false,
      aquiferFiles: {},
      aquifer_resource_sections: [
        { code: 'M', name: 'Advanced mapping' },
        { code: 'A', name: 'Artesian advisory' },
        { key: 'obs-wells', name: 'Oberservation Wells' },
        { code: 'N', name: 'Numerical model' },
        { code: 'P', name: 'Pumping stress index' },
        { code: 'W', name: 'Water budget' },
        { key: 'water-quality', name: 'Water quality information' },
        { key: 'aquifer-connected', name: 'Hydraulically connected (screening level)' },
        { code: 'G', name: 'Groundwater Surface Water Interactions' },
        { code: 'I', name: 'Other information' }
      ],
      wells: [],
      activeObsWells: [],
      inactiveObsWellsWithWaterLevel: [],
      inativeObsWellsWithOutWaterLevel: [],
      noObsWells: false,
      waterWithdrawlVolume: ''
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
      'shapefile',
      'shapefile_uploading',
      'shapefile_upload_message',
      'shapefile_upload_success'
    ])
  },
  watch: {
    id () {
      this.fetch()
    },
    licence_details (newLDetails, oldLDetails) {
      this.setWaterVolume(newLDetails)
    }
  },
  filters: {
    unitWaterVolume (volume) {
      return Math.round(volume) + ' cubic metres'
    },
    formatDate: function (value) {
      if (!value) return ''
      value = new Date(value)
      return value.getMonth() + '/' + value.getDate() + '/' + value.getFullYear()
    }
  },
  methods: {
    ...mapActions('documentState', [
      'uploadFiles',
      'uploadShapefile',
      'fileUploadSuccess',
      'fileUploadFail',
      'clearUploadShapeFileMessage',
      'clearUploadFilesMessage'
    ]),
    loadForm () {
      ApiService.query(`aquifers/${this.id}/edit`)
        .then((response) => {
          this.form = response.data
        })
    },
    bySection (resources, section) {
      return (resources || []).filter(function (resource) {
        return resource.section_code === section.code
      })
    },
    handleSaveSuccess (response) {
      this.fetch()

      if (this.$refs.aquiferHistory) {
        this.$refs.aquiferHistory.update()
      }

      this.navigateToView()
    },
    handlePatchError (error) {
      Sentry.captureException(error)
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
      this.clearUploadShapeFileMessage()
      this.clearUploadFilesMessage()
      this.fieldErrors = {}
      let writableRecord = JSON.parse(JSON.stringify(this.form))
      delete writableRecord.licence_details
      delete writableRecord.geom
      return ApiService.patch('aquifers', this.id, writableRecord)
        .then(() => {
          this.showSaveSuccess = true
          return this.finishSavingFiles()
        }, this.handlePatchError)
    },
    finishSavingFiles () {
      const promises = []
      if (this.upload_files.length > 0) {
        const filePromise = this.uploadFiles({
          documentType: 'aquifers',
          recordId: this.id
        }).then(() => {
          this.fileUploadSuccess()
          this.fetchFiles()
        }).catch((error) => {
          Sentry.captureException(error)
          this.fileUploadFail()
          throw error
        })
        promises.push(filePromise)
      }

      if (this.shapefile) {
        const shapeFilePromise = this.uploadShapefile({
          documentType: 'aquifers',
          recordId: this.id
        }).then(() => {
          this.mapKey++
        })
        promises.push(shapeFilePromise)
      }

      return Promise.all(promises).then(this.handleSaveSuccess)
    },
    navigateToView () {
      this.$router.push({ name: 'aquifers-view', params: { id: this.id } })
      this.fetch()
    },
    navigateToEdit () {
      this.showSaveSuccess = false
      this.$router.push({ name: 'aquifers-edit', params: { id: this.id } })
    },
    print () {
      window.print()
    },
    fetch (id = this.id) {
      return ApiService.query(`aquifers/${id}`)
        .then((response) => {
          const responseData = response.data || {}

          if (responseData.licence_details.wells_by_licence) {
            responseData.licence_details.wells_by_licence.forEach((licence) => {
              if (licence.well_tag_numbers_in_licence) {
                const wtns = licence.well_tag_numbers_in_licence
                licence.well_tag_numbers_in_licence = wtns.split(',').map((n) => parseInt(n))
              }
            })
          }

          // force the map to update.
          this.record = responseData
          this.licence_details = responseData.licence_details
          this.lic_qty = responseData.licence_details.lic_qty
          const obsWells = responseData.licence_details.obs_wells

          return this.getWaterLevels(obsWells).then(() => {
            const sortedWells = orderBy(obsWells, ['hasLevelAnalysis', 'waterLevels'], ['desc', 'asc']) // sorts so wells with waterLevels are at the top.
            const wellsByStatus = groupBy(sortedWells, 'observation_well_status') // groups wells into active and inactive categories

            this.activeObsWells = wellsByStatus.Active || []

            const inactiveObsWells = wellsByStatus.Inactive || []

            // split inactive wells into those with water level analysis and those without
            this.inactiveObsWellsWithWaterLevel = inactiveObsWells.filter((w) => w.waterLevels)
            this.inativeObsWellsWithOutWaterLevel = inactiveObsWells.filter((w) => !w.waterLevels)

            // Show the "No information available." message when there are no obs wells to show
            this.noObsWells = this.activeObsWells.length === 0 && inactiveObsWells.length === 0
          })
        })
    },
    fetchFiles (id = this.id) {
      this.loadingFiles = true
      return ApiService.query(`aquifers/${id}/files`)
        .then((response) => {
          this.aquiferFiles = response.data
          this.loadingFiles = false
        })
    },
    fetchWells (id = this.id) {
      const maxResults = 5000 // 5000 is the API max
      const params = { aquifer: id, limit: maxResults }
      return ApiService.query('wells/locations', params)
        .then((response) => {
          const total = response.data.count

          const initialPromise = Promise.resolve(response.data.results || [])
          let promise = initialPromise

          if (total > maxResults) {
            const numFetches = Math.ceil(total / maxResults)
            promise = range(1, numFetches).reduce((previousPromise, pageNum) => {
              return previousPromise.then((results) => {
                return ApiService.query('wells/locations', { ...params, offset: pageNum * maxResults }).then((response2) => {
                  return results.concat(response2.data.results)
                })
              })
            }, initialPromise)
          }

          return promise
        }).then((wells) => {
          this.wells = wells || []
        })
    },
    getObservationWellLink (wellNumber) {
      return `https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS WELL ${wellNumber}`
    },
    getWaterLevels (obsWells) {
      return Promise.all(
        obsWells.map((owell) => {
          owell.hasLevelAnalysis = false
          let wellNumber = owell.observation_well_number
          const url = `https://catalogue.data.gov.bc.ca/api/3/action/datastore_search?resource_id=a8933793-eadb-4a9c-992c-da4f6ac8ca51&fields=EMS_ID,Well_Num,trend_line_slope,category&filters=%7b%22Well_Num%22:%22${wellNumber}%22%7d`
          return ApiService.query(url).then((response) => {
            if (response.data.result.records.length > 0) {
              const { category } = response.data.result.records[0]
              owell.hasLevelAnalysis = category.toUpperCase() !== 'N/A'
              owell.waterLevels = category
            }
          }, () => {}) // Swallow any API error from https://catalogue.data.gov.bc.ca/api
        })
      )
    },
    setWaterVolume (details) {
      if (details.usage && details.usage.constructor === Array && details.usage.length > 0) {
        this.waterWithdrawlVolume = sumBy(details.usage, 'total_qty')
      }
    },
    // log a google analytics event when clicking on links to other sites
    handleOutboundLinkClicks (link) {
      if (window.ga) {
        window.ga('send', 'event', {
          eventCategory: 'Outbound Link',
          eventAction: 'click',
          eventLabel: link
        })
      }
    },
    // log a google analytics event when clicking on external aquifer resources
    // (e.g. PDFS or other files)
    handleExternalResourceClicks () {
      if (window.ga) {
        window.ga('send', 'event', {
          eventCategory: 'Attachment',
          eventAction: 'Accessed',
          eventLabel: 'Aquifer Factsheet'
        })
      }
    }
  }
}
</script>
