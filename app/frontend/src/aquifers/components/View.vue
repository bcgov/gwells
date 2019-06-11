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
    <b-alert show v-if="files_uploading">File Upload In Progress...</b-alert>
    <b-alert show v-if="!files_uploading && file_upload_error" variant="warning" >
      There was an error uploading the files
    </b-alert>
    <b-alert show v-if="!files_uploading && file_upload_success" variant="success" >
      Successfully uploaded all files
    </b-alert>
    <b-alert show v-if="shapefile_upload_success &! shapefile_uploading" variant="success" >
      Shapefile uploaded.
    </b-alert>
    <b-alert show v-if="!shapefile_upload_success &! shapefile_uploading && shapefile_upload_message" variant="warning" >
      There was an error uploading the shapefile: {{ shapefile_upload_message }}.
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
              <ul class="m-0 p-0 aquifer-information-list aquifer-main-information-list">
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
                <dd>{{record.vulnerability}}</dd>
              </li>
              <li>
                <dt>Material type</dt>
                <dd>{{record.material}}</dd>
              </li>
              <li>
                <dt>Subtype</dt>
                <dd>{{record.subtype}}</dd>
              </li>
              <li>
                <dt>Quality concerns</dt>
                <dd>{{record.quality_concern}}</dd>
              </li>
              <li>
                <dt>Productivity</dt>
                <dd>{{record.productivity}}</dd>
              </li>
              <li>
                <dt>Size (km²)</dt>
                <dd>{{record.area}}</dd>
              </li>
              <li>
                <dt>Demand</dt>
                <dd>{{record.demand}}</dd>
              </li>
              </ul>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="12" md="12" lg="7" class="p-0">
          <single-aquifer-map v-bind:geom="record.geom" :key="mapKey"/>
        </b-col>
      </b-row>

      <b-row v-if="viewMode" class="mt-5">
        <b-col cols="12" xl="4" lg="6">
          <h5 class="mt-3 border-bottom pb-4 main-title">Well Information</h5>
          <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li>
              <dt>Number of wells associated to the aquifer</dt>
              <dd><a href="" @click.prevent="handleWellSearch()">{{ licence_details.num_wells }}</a></dd>
            </li>
          </ul>
          <p><i v-if="licence_details.wells_updated">Well info last updated {{ licence_details.wells_updated.update_date__max|formatDate }}</i></p>
          <h5 class="mt-5 border-bottom pb-4 main-title">Documentation</h5>
          <aquifer-documents :files="aquiferFiles"
            :editMode="editMode"
            :id="this.id"
            v-on:fetchFiles="fetchFiles">
          </aquifer-documents>
        </b-col>
        <b-col cols="12" xl="4" lg="6">
          <h5 class="mt-3 border-bottom pb-4 main-title">Licensing Information</h5>
          <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
            <li>
              <dt>Number of groundwater licences</dt>
              <dd>{{ licence_details.licence_count }}</dd>
            </li>
            <li>
              <dt>Water withdrawal volume (annual)</dt>
              <dd v-if="waterWithdrawlVolume">{{ waterWithdrawlVolume | unitWaterVolume}}</dd>
              <dd v-else>No information available.</dd>
            </li>
          </ul>
          <div v-if="licence_details.lic_qty.length > 0">
              <h5 class="pie-chart-title">Licenced use volume by purpose</h5>
              <PieChart :chartData="licence_details.usage" class="mt-3"></PieChart>
              <h5 class="pie-chart-title pt-4">Licenced quantity by use</h5>
              <PieChart :chartData="licence_details.lic_qty" class="mt-3"></PieChart>
          </div>
          <b-table striped hover :items="licence_details.wells_by_licence"></b-table>
          <p><i v-if="licence_details.licences_updated">Licence info last updated {{ licence_details.licences_updated.update_date__max|formatDate }}</i></p>
          <p>
            Licensing information is obtained from the <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" @click="handleOutboundLinkClicks('https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public')">Water Rights Licence - Public data layer</a>.
          </p>
          <p>
            Unique licenses are counted once for each aquifer that they are associated with.
          </p>
          <p>
            The total licensed volume is counted once for each licence (the total volume may be shared between wells if there are multiple wells in a licence). In cases where specific volumes are licensed for multiple purposes, individual volumes are summed.
          </p>
        </b-col>
        <b-col cols="12" xl="4" lg="6">
          <h5 class="mt-3 border-bottom pb-4 main-title">Knowledge Indicators</h5>
          <ul class="ml-0 mr-0 mb-0 mt-4 p-0 aquifer-information-list">
            <div class="aquifer-information-list-divider"></div>
          <li :key="section.id" v-for="(section, index) in aquifer_resource_sections">
              <div class="artesian-conditions" v-if="index === 1">
                <dt>Artesian conditions</dt>
                <dd><a href="#" @click="handleArtesianSearch()">{{ licence_details.num_artesian_wells }} artesian wells in aquifer</a></dd>
              </div>
              <div class="observational-wells" v-if="index === 2">
                <dt>Observation wells</dt>
                <dd v-if="obs_wells.length > 0">
                  <ul class="p-0 m-0">
                    <li v-for="owell in obs_wells" :key="owell.observation_well_number">
                      <a :href="getObservationWellLink(owell.observation_well_number)">Observation Well {{ owell.observation_well_number }}</a>
                      <br/>Water Level Analysis:
                      <a v-if="waterLevels.find(o => o.wellNumber === owell.observation_well_number)" href="http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html">
                      {{ (waterLevels.find(o => o.wellNumber === owell.observation_well_number).levels )}}
                      </a>
                      <span v-else>No information available.</span>
                    </li>
                  </ul>
                </dd>
                <dd v-else>
                  No information available.
                </dd>
              </div>
              <dt>{{ section.name }}</dt>
              <dd>
                <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                  <li><a :href="resource.url" @click="handleExternalResourceClicks">{{ resource.name }}</a></li>
                </ul>
                <p v-if="!bySection(record.resources, section).length">No information available.</p>
              </dd>
              <div class="water-quality-information" v-if="index === 5">
                <dt>Water quality information</dt>
                <dd><a :href="getEMSLink()">{{ licence_details['num_wells_with_ems'] }} wells with an EMS ID</a></dd>
                <dt>Hydraulically connected <a href='#' style='font-size:140%' title="Inferred based on aquifer subtype - not field verified">*</a></dt>
                <dd>{{ licence_details['hydraulically_connected'] ? "Yes" : "No"}}</dd>
              </div>
          </li>
          </ul>
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

.sub-title {

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

.aquifer-main-information-list dt {
  width: 35%;
}

.aquifer-main-information-list dd {
  width: 65%;
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

.aquifer-main-information-list .aquifer-information-list-divider {
  left: calc(35% - 0.5px);
}

.pie-chart-title {
  font-weight: bold !important;
  font-size: 1rem !important;
}
.pie-chart-container {
  margin: 0 auto;
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
import { sumBy } from 'lodash'
import PieChart from './PieChart.vue'
export default {

  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm,
    'aquifer-documents': Documents,
    'single-aquifer-map': SingleAquiferMap,
    ChangeHistory,
    PieChart
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
      mapKey: 0, // component key to force updates.
      error: undefined,
      fieldErrors: {},
      loading: false,
      record: {},
      licence_details: {
        usage: [],
        lic_qty: []
      },
      showSaveSuccess: false,
      aquiferFiles: {},
      aquifer_resource_sections: [],
      wells: [],
      obs_wells: [],
      waterLevels: [],
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
    obs_wells (newObsWells, oldObsWells) {
      this.getWaterLevels(newObsWells)
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
      'fileUploadFail'
    ]),
    fetchWells (id = this.id) {
      ApiService.query(`aquifers/${id}/details`)
        .then((response) => {
          this.wells = response.data
        }).catch((error) => {
          console.error(error)
        })
    },
    bySection (resources, section) {
      return (resources || []).filter(function (resource) {
        return resource.section_code === section.code
      })
    },
    handleSaveSuccess (response) {
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

      if (this.shapefile) {
        this.uploadShapefile({
          documentType: 'aquifers',
          recordId: this.id
        }).then(() => {
          this.fetch()
          this.mapKey++
        })
      } else {
        this.fetch()
      }
      this.navigateToView()
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
      let writableRecord = JSON.parse(JSON.stringify(this.record))
      delete writableRecord.licence_details
      delete writableRecord.geom
      ApiService.patch('aquifers', this.id, writableRecord)
        .then(this.handleSaveSuccess)
        .catch(this.handlePatchError)
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
      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          // force the map to update.
          this.record = response.data
          this.licence_details = response.data.licence_details
          this.lic_qty = response.data.licence_details.lic_qty
          this.obs_wells = response.data.licence_details.obs_wells
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
          'artesian_flow_has_value': true
        },
        hash: '#advanced'
      })
    },
    getObservationWellLink (wellNumber) {
      return `https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS WELL ${wellNumber}`
    },
    getWaterLevels (obsWells) {
      obsWells.map((owell) => {
        function getRequestUrl (wellNumber) {
          return `https://catalogue.data.gov.bc.ca/api/3/action/datastore_search?resource_id=a8933793-eadb-4a9c-992c-da4f6ac8ca51&fields=EMS_ID,Well_Num,trend_line_slope,category&filters=%7b%22Well_Num%22:%22${wellNumber}%22%7d`
        }
        let wellNumber = owell.observation_well_number
        ApiService.query(getRequestUrl(wellNumber)).then((response) => {
          this.waterLevels.push({ wellNumber, levels: response.data.result.records[0].category })
        }).catch((e) => {
          console.error(e)
        })
      })
    },
    setWaterVolume (details) {
      if (details.usage && details.usage.constructor === Array && details.usage.length > 0) {
        this.waterWithdrawlVolume = sumBy(details.usage, 'total_qty')
      }
    },
    getEMSLink () {
      return `https://apps.nrs.gov.bc.ca/gwells/?match_any=false&ems_has_value=true&aquifer=${this.record['aquifer_id']}#advanced`
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
