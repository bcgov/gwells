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
  <div id="aquifer-detail">
    <b-card no-body class="mb-3 container d-print-none">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"/>
    </b-card>
    <div v-if="loadingAquifer">
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
    </div>
    <b-card v-else-if="errorNotFound" class="container p-1">
      <h1>Not Found</h1>
      <p>The page you are looking for was not found.</p>
    </b-card>
    <div v-else>
      <b-card class="container container-wide card-container p-0 pb-5 main-card" :class="{ 'p-4': editMode }">
        <api-error v-if="error" :error="error"/>
        <b-alert show v-if="viewMode && isRetired && !isUnpublished" variant="warning">
          This aquifer is retired and stored for record keeping purposes. It will be hidden from
          DataBC, iMapBC and the CSV/XLS export.
        </b-alert>
        <b-alert show v-if="viewMode && isUnpublished" variant="warning">
          This aquifer is unpublished and will be hidden from DataBC, iMapBC, the GWELLS Aquifer
          Search, the GWELLS Aquifer Summary and the CSV/XLS export.
        </b-alert>
        <b-alert show v-if="files_uploading || shapefile_uploading">File Upload In Progress...</b-alert>
        <b-alert show v-if="!files_uploading && file_upload_error" variant="danger">
          There was an error uploading the documents
        </b-alert>
        <b-alert show v-if="!files_uploading && file_upload_success" variant="success">
          Successfully uploaded all documents
        </b-alert>
        <b-alert show v-if="shapefile_upload_success & !shapefile_uploading" variant="success">
          Shapefile uploaded.
        </b-alert>
        <b-alert show v-if="!shapefile_upload_success & !shapefile_uploading && shapefile_upload_message" variant="danger">
          There was an error uploading the shapefile: {{ shapefile_upload_message }}.
        </b-alert>
        <b-alert variant="success" :show="showSaveSuccess" id="aquifer-success-alert">
          Aquifer {{ id }}'s information successfully updated.
        </b-alert>

        <div v-if="editMode">
          <div v-if="loadingForm" id="form-loading-spinner">
            <div class="fa-2x text-center">
              <i class="fa fa-circle-o-notch fa-spin"></i>
            </div>
          </div>
          <b-row class="border-bottom mb-3 pb-2">
            <b-col><h4>Aquifer {{id}} Summary - Edit</h4></b-col>
          </b-row>
          <aquifer-form
            :fieldErrors="fieldErrors"
            :record="form"
            :files="aquiferFiles"
            :loadingData="loadingForm"
            :loadingFiles="loadingFiles"
            showId
            v-on:save="save"
            v-on:cancel="navigateToView"
            v-on:fetchFiles="fetchFiles"
            />
          <change-history class="mt-5" :id="id" resource="aquifers" ref="aquiferHistory"/>
        </div>

        <b-container fluid v-if="viewMode">
          <b-row>
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
                        v-if="!isRetired"
                        href="#"
                        title="Print"
                        v-on:click.prevent="print"
                      />
                    </div>
                  </div>
                </b-col>
              </b-row>
              <b-row>
                <b-col cols="12" sm="12" class="pl-4 pr-4 aquifer-main-information-list">
                  <b-row>
                    <b-col cols="6" md="3" lg="6">Aquifer number</b-col>
                    <b-col cols="6" md="3" lg="6" id="aquifer-view-number">{{id}}</b-col>
                    <b-col cols="6" md="3" lg="6">Year of mapping</b-col>
                    <b-col cols="6" md="3" lg="6" class="aquifer-mapping-year">{{record.mapping_year}}</b-col>
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
                    <b-col cols="6" md="3" lg="6">
                      Vulnerability
                      <i id="vulnerability-info" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="vulnerability-info"
                        triggers="hover focus"
                        content="The susceptibility of an aquifer to contamination from surface sources. Three vulnerability categories are used: high, moderate, or low. Vulnerability is based on hydrogeology alone and does not consider the existing type of land use or nature of the potential contaminants."/>
                    </b-col>
                    <b-col cols="6" md="3" lg="6">{{record.vulnerability}}</b-col>
                  </b-row>
                  <b-row>
                    <b-col cols="6" md="3" lg="6">Material type</b-col>
                    <b-col cols="6" md="3" lg="6">{{record.material}}</b-col>
                    <b-col cols="6" md="3" lg="6">
                      Subtype
                      <i id="aquifer-subtype-info" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="aquifer-subtype-info"
                        triggers="hover focus"
                      >
                        There are different types of aquifers, depending on the geologic materials in which they occur. Subtype descriptions can be
                        <a href='https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells-aquifers/understanding-aquifers/aquifer-subtype-code-description' target='_blank' rel="noopener noreferrer" \class='d-print-url'>found here</a>.
                      </b-popover>
                    </b-col>
                    <b-col cols="6" md="3" lg="6">{{record.subtype}}</b-col>
                  </b-row>
                  <b-row>
                    <b-col cols="6" md="3" lg="6">
                      Quality concerns
                      <i id="aquifer-quality-concerns" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="aquifer-quality-concerns"
                        triggers="hover focus"
                      >
                        Classified as unknown/none, isolated, local, or regional. For details see page 16 of the Guide to Using the
                        <a href='https://www2.gov.bc.ca/assets/gov/environment/air-land-water/water/science-data/aquifer_maps_guide.pdf' target='_blank' rel="noopener noreferrer" class='d-print-url'>BC Aquifer Classification System</a>.
                      </b-popover>
                    </b-col>
                    <b-col cols="6" md="3" lg="6">{{record.quality_concern}}</b-col>
                    <b-col cols="6" md="3" lg="6">
                      Productivity
                      <i id="productivity-info" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="productivity-info"
                        triggers="hover focus"
                        content="Productivity describes the rate of groundwater flow from wells and springs and the abundance of groundwater in an aquifer. Classified as low, medium, or high."/>
                    </b-col>
                    <b-col cols="6" md="3" lg="6">{{record.productivity}}</b-col>
                  </b-row>
                  <b-row>
                    <b-col cols="6" md="3" lg="6">Size (km²)</b-col>
                    <b-col cols="6" md="3" lg="6">{{record.area}}</b-col>
                    <b-col cols="6" md="3" lg="6">
                      Calculated well density
                      <i id="calculated-demand-density-info" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="calculated-demand-density-info"
                        triggers="hover focus"
                        content="Calculated based on the number of wells known to be completed in the aquifer per square kilometer. Light ≤ 4 km²; Medium 4 – 20 km²; Heavy > 20 km²"/>
                    </b-col>
                    <b-col cols="6" md="3" lg="6">{{record.demand}}</b-col>
                  </b-row>
                </b-col>
              </b-row>
            </b-col>
            <b-col id="map-container" cols="12" md="12" lg="7" class="p-0">
              <map-loading-spinner :loading="loadingMap"/>

              <single-aquifer-map
                :aquifer-id="id"
                :geom="record.geom"
                :key="mapKey"
                :aquifer-notations="aquiferNotations"
                @mapLoading="loadingMap = true"
                @mapLoaded="loadingMap = false"/>
            </b-col>
          </b-row>

          <b-row v-if="!isRetired" class="mt-5 aquifer-details">
            <b-col cols="12" xl="4" lg="6">
              <h5 class="mt-3 border-bottom pb-4 main-title">Well Information</h5>
              <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
                <div class="aquifer-information-list-divider"></div>
                <li>
                  <dl>
                    <dt>Number of wells correlated to the aquifer
                      <i id="correlated-wells-count" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="correlated-wells-count"
                        triggers="hover focus"
                        content="The total number of wells that fall within the aquifer boundaries and, based on depth and lithology, are believed to withdraw water from that aquifer."/>
                    </dt>
                    <dd class="m-0">
                      <router-link :to="{ name: 'wells-home', query: {'match_any':false, 'aquifer': id, 'search':'', 'well':''}, hash: '#advanced'}">
                        {{ licenceDetails.num_wells }}
                      </router-link>
                    </dd>
                  </dl>
                </li>
                <li>
                  <dl>
                    <dt>
                      Number of uncorrelated wells within mapped aquifer extent
                      <i id="uncorrelated-wells-count" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="uncorrelated-wells-count"
                        triggers="hover focus"
                        content="The total number of wells that fall within the aquifer polygon but have not been correlated to any aquifer. These wells may potentially be located within this aquifer or may be completed within an aquitard or within another aquifer located at a different depth."/>
                    </dt>
                    <dd class="m-0">
                      {{ uncorrelatedWells.length }}
                    </dd>
                  </dl>
                </li>
                <li>
                  <dl>
                    <dt>Flowing artesian wells
                      <i id="artesian-wells" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="artesian-wells"
                        triggers="hover focus"
                        content="A flowing artesian well is one that has been drilled into an aquifer where the pressure within the aquifer forces the groundwater to rise above the land surface naturally without using a pump."/>
                    </dt>
                    <dd class="m-0">
                      <router-link :to="{ name: 'wells-home', query: {'match_any':false, 'aquifer': id, 'artesian_conditions':true}, hash: '#advanced'}">
                        {{ licenceDetails.num_artesian_wells }} artesian wells in aquifer
                      </router-link>
                    </dd>
                  </dl>
                </li>
              </ul>
              <p>
                <i v-if="licenceDetails.wells_updated">Well info last updated {{ licenceDetails.wells_updated.update_date__max|formatDate }}</i>
              </p>
              <h5 class="mt-5 border-bottom pb-4 main-title">Documentation</h5>
              <aquifer-documents :files="aquiferFiles"
                highlightTitle="Factsheets"
                :highlightRegexp="factsheetRe"
                publicFilesTitle="Other Documents"
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
                  The licensing summaries should be considered estimates. Total volume is likely more than what is indicated in charts due to
                  domestic use and unprocessed licence applications. Due to complexities in the structure of the licensing data,
                  reported values should be confirmed through the
                  <a href="https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main" target="_blank" class="d-print-url">
                    e&#8209;licensing portal</a>.
                </p>
              </div>
              <ul class="ml-0 mr-0 mt-4 mb-0 p-0 aquifer-information-list">
                <div class="aquifer-information-list-divider"></div>
                <li>
                  <dt>Number of groundwater licences</dt>
                  <dd class="m-0">{{ licenceDetails.licence_count }}</dd>
                </li>
                <li>
                  <dt>Water withdrawal volume (annual)</dt>
                  <dd class="m-0" v-if="waterWithdrawlVolume">{{ waterWithdrawlVolume | unitWaterVolume}}</dd>
                  <dd class="m-0" v-else>No information available.</dd>
                </li>
              </ul>
              <div v-if="licenceDetails.lic_qty.length > 0">
                <b-row class="pt-5">
                  <b-col cols="12" md="6" lg="12" class="pb-5">
                    <h5 class="pie-chart-title">Licensed volume by purpose (millions of cubic meters)</h5>
                    <pie-chart
                      :data="licenceUsageChartData"
                      :labels="licenceUsageChartLabels"
                      :chart-options="licenceUsageChartOptions"
                      class="mt-3"/>
                  </b-col>
                  <b-col cols="12" md="6" lg="12" class="pb-5">
                    <h5 class="pie-chart-title">Number of licences by purpose</h5>
                    <pie-chart
                      :data="licenceQuantityChartData"
                      :labels="licenceQuantityChartLabels"
                      :chart-options="licenceQuantityChartOptions"
                      class="mt-3"/>
                  </b-col>
                </b-row>
              </div>
              <b-table id="licenses" striped :items="licenceDetails.wells_by_licence">
                <template v-slot:cell(licence_number)="row">
                  <a :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${row.item.licence_number}`" target="_blank">
                    {{ row.item.licence_number }}
                  </a>
                </template>
                <template v-slot:cell(well_tag_numbers_in_licence)="row">
                  <ul class="p-0 m-0">
                    <li v-for="wtn in row.item.well_tag_numbers_in_licence" :key="wtn">
                      <router-link :to="{ name: 'wells-detail', params: { id: wtn }}">{{ wtn }}</router-link>
                    </li>
                  </ul>
                </template>
              </b-table>
              <p><i v-if="licenceDetails.licences_updated && licenceDetails.licences_updated.update_date__max">Licence info last updated {{ licenceDetails.licences_updated.update_date__max|formatDate }}</i></p>
              <p>
                Licensing information is obtained from
                the <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" target="_blank" class="d-print-url">
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
                  <div class="advanced-mapping" v-if="section.code === 'M'">
                    <dt class="text-right">Advanced mapping
                      <i id="aquifer-advanced-mapping" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                      <b-popover
                        target="aquifer-advanced-mapping"
                        triggers="hover focus"
                        content="Aquifers with advanced mapping have been mapped in three dimensions. Generally, cross-sections and/or three-dimensional models, have been developed."/>
                    </dt>
                    <dd class="m-0">
                      <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                        <li><a :href="sanitizeResourceUrl(resource.url)" target="_blank" rel="noopener noreferrer" class="d-print-url">{{ resource.name }}</a></li>
                      </ul>
                      <p class="m-0" v-if="!bySection(record.resources, section).length">No information available.</p>
                    </dd>
                  </div>
                  <div class="observational-wells" v-else-if="section.key === 'obs-wells'">
                    <dl>
                      <dt class="text-right">Observation wells
                        <i id="aquifer-observation-wells" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquifer-observation-wells"
                          triggers="hover focus"
                          content="Groundwater Observation Wells are used to monitor aquifer groundwater levels and chemistry over time."/>
                      </dt>
                      <dd class="m-0">
                        <div v-if="activeObsWells.length > 0">
                          <h6 class="border-bottom">Active</h6>
                          <ul class="p-0 m-0">
                            <li v-for="owell in activeObsWells" :key="owell.well_tag_number" :data-water-level="owell.waterLevels" :class="{error: owell.errorFetching}">
                              <observation-well
                                :observationWell="owell"
                                @reload="getWaterLevels"/>
                            </li>
                          </ul>
                        </div>
                        <div v-if="inactiveObsWellsWithWaterLevel.length > 0 || inativeObsWellsWithOutWaterLevel.length > 0">
                          <h6 class="border-bottom mt-2">Inactive<br><small>(data may not be available)</small></h6>
                          <ul class="p-0 m-0">
                            <li v-for="owell in inactiveObsWellsWithWaterLevel" :key="owell.well_tag_number" :data-water-level="owell.waterLevels" :class="{error: owell.errorFetching}">
                              <observation-well
                                :observationWell="owell"
                                @reload="getWaterLevels"/>
                            </li>
                            <li v-if="inativeObsWellsWithOutWaterLevel.length > 0" class="obs-wells-wo-well-level">
                              No Water Level Analysis:
                              <observation-well
                                v-for="owell in inativeObsWellsWithOutWaterLevel"
                                :key="owell.observation_well_number"
                                :observationWell="owell"
                                @reload="getWaterLevels"/>
                            </li>
                          </ul>
                        </div>
                        <div v-if="noObsWells">
                          No information available.
                        </div>
                      </dd>
                    </dl>
                  </div>
                  <div class="water-quality-information" v-else-if="section.key === 'water-quality'">
                    <dl>
                      <dt class="text-right">Water quality information
                        <i id="aquiferWaterQualityInformation" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferWaterQualityInformation"
                          triggers="hover focus"
                          content="Indicates there are wells correlated to the aquifer with water quality information in the Environmental Monitoring System (EMS) database."/>
                      </dt>
                      <dd class="m-0">
                        <router-link :to="{ name: 'wells-home', query: {'match_any':false, 'ems_has_value':true, 'aquifer': id}, hash: '#advanced'}">
                          {{ licenceDetails['num_wells_with_ems'] }} wells with an EMS ID
                        </router-link>
                      </dd>
                    </dl>
                  </div>
                  <div class="aquifer-connected" v-else-if="section.key === 'aquifer-connected'">
                    <dl>
                      <dt class="text-right">Hydraulically connected (screening level)
                        <i id="aquiferConnectedInfo" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferConnectedInfo"
                          triggers="hover focus"
                          content="Likelihood of hydraulic connection between groundwater and surface water requires aquifer specific assessment and professional judgement. "/>
                      </dt>
                      <dd class="m-0">
                        <a href="http://a100.gov.bc.ca/appsdata/acat/documents/r50832/HydraulicConnectMW3_1474311684426_4310694949.pdf"
                        target="_blank" rel="noopener noreferrer">See Guidance on Determining Likelihood of Hydraulic Connection</a>
                      </dd>
                    </dl>
                  </div>
                  <div class="aquifer-numerical-model" v-else-if="section.code === 'N'">
                    <dl>
                      <dt class="text-right">Numerical Model
                        <i id="aquiferNumericalModel" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferNumericalModel"
                          triggers="hover focus"
                          content="Numerical groundwater flow models are mathematical representations of groundwater flow in an aquifer and the interactions with adjacent surface water bodies."/>
                      </dt>
                      <dd class="m-0">
                        <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                          <li><a :href="sanitizeResourceUrl(resource.url)" target="_blank" rel="noopener noreferrer" class="d-print-url">{{ resource.name }}</a></li>
                        </ul>
                        <p class="m-0" v-if="!bySection(record.resources, section).length">No information available.</p>
                      </dd>
                    </dl>
                  </div>
                  <div class="aquifer-water-budget" v-else-if="section.code === 'W'">
                    <dl>
                      <dt class="text-right">Water Budget
                        <i id="aquiferWaterBudget" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferWaterBudget"
                          triggers="hover focus"
                          content="Water budget studies are an accounting of all the water flowing into and out of an aquifer and/or a watershed over a specified time."/>
                      </dt>
                      <dd class="m-0">
                        <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                          <li><a :href="sanitizeResourceUrl(resource.url)" target="_blank" rel="noopener noreferrer" class="d-print-url">{{ resource.name }}</a></li>
                        </ul>
                        <p class="m-0" v-if="!bySection(record.resources, section).length">No information available.</p>
                      </dd>
                    </dl>
                  </div>
                  <div class="aquifer-groundwater-surface-interactions" v-else-if="section.code === 'G'">
                    <dl>
                      <dt class="text-right">Groundwater Surface Water Interactions
                        <i id="aquiferGroundwaterSurfaceInteractions" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferGroundwaterSurfaceInteractions"
                          triggers="hover focus"
                          content="Studies that characterize the exchange of water and/or chemicals between the land surface and the subsurface."/>
                      </dt>
                      <dd class="m-0">
                        <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                          <li><a :href="sanitizeResourceUrl(resource.url)" target="_blank" rel="noopener noreferrer" class="d-print-url">{{ resource.name }}</a></li>
                        </ul>
                        <p class="m-0" v-if="!bySection(record.resources, section).length">No information available.</p>
                      </dd>
                    </dl>
                  </div>
                  <div class="aquifer-artesian-advisory" v-else-if="section.code === 'A'">
                    <dl>
                      <dt class="text-right">Drilling & operation advisory
                        <i id="aquiferArtesianAdvisory" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferArtesianAdvisory"
                          triggers="hover focus"
                          content="Advisories highlighting regional concerns about water availability, water quality, and flowing artesian conditions."/>
                      </dt>
                      <dd class="m-0">
                        <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                          <li><a :href="sanitizeResourceUrl(resource.url)" target="_blank" rel="noopener noreferrer" class="d-print-url">{{ resource.name }}</a></li>
                        </ul>
                        <p class="m-0" v-if="!bySection(record.resources, section).length">No information available.</p>
                      </dd>
                    </dl>
                  </div>
                  <div class="aquifer-notations" v-else-if="section.key === 'aquifer-notations'">
                    <dl>
                      <dt class="text-right">Aquifer notations
                        <i id="aquiferNotations" tabindex="0" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none"></i>
                        <b-popover
                          target="aquiferNotations"
                          triggers="hover focus">
                          <p>Water allocation notations are a water management tool that indicates a potential lack of water availability/quality in a source. For details click <a href="https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-licensing-rights/water-allocation-notations">here</a>.</p>
                        </b-popover>
                      </dt>
                      <dd class="m-0">{{ aquiferNotations || 'No notation currently assigned.' }}</dd>
                    </dl>
                  </div>
                  <div v-else>
                    <dt class="text-right">{{ section.name }}</dt>
                    <dd class="m-0">
                      <ul class="p-0 m-0" :key="resource.id" v-for="resource in bySection(record.resources, section)">
                        <li><a :href="sanitizeResourceUrl(resource.url)" target="_blank" rel="noopener noreferrer" class="d-print-url">{{ resource.name }}</a></li>
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
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState, mapMutations } from 'vuex'
import { sumBy, orderBy, groupBy, range, cloneDeep } from 'lodash'
import * as Sentry from '@sentry/browser'

import ApiService from '@/common/services/ApiService.js'

import APIErrorMessage from '@/common/components/APIErrorMessage'
import ChangeHistory from '@/common/components/ChangeHistory.vue'
import MapLoadingSpinner from '@/common/components/MapLoadingSpinner.vue'
import AquiferForm from './Form'
import Documents from './Documents.vue'
import SingleAquiferMap from './SingleAquiferMap.vue'
import PieChart from './PieChart.vue'
import ObservationWell from './ObservationWell.vue'
import { MAX_API_RESULT_AND_EXPORT_COUNT } from '@/common/constants'
import { sanitizeUrl } from '@braintree/sanitize-url'

const ONE_MILLION = 1 * 1000 * 1000

export default {
  components: {
    'api-error': APIErrorMessage,
    'aquifer-form': AquiferForm,
    'aquifer-documents': Documents,
    'single-aquifer-map': SingleAquiferMap,
    'map-loading-spinner': MapLoadingSpinner,
    'change-history': ChangeHistory,
    'pie-chart': PieChart,
    'observation-well': ObservationWell
  },
  props: {
    'edit': Boolean
  },
  created () {
    if (this.id === null) {
      this.error = `Unable to load aquifer '${this.id}'`
    }

    if (this.id !== this.storedId) {
      this.fetch()
    }

    if (this.editMode) {
      this.loadForm()
    }
  },
  data () {
    return {
      mapKey: 0, // component key to force updates.
      error: undefined,
      fieldErrors: {},
      form: {},
      showSaveSuccess: false,
      aquifer_resource_sections: [
        { code: 'M', name: 'Advanced mapping' },
        { code: 'A', name: 'Drilling and operation advisory' },
        { key: 'obs-wells', name: 'Oberservation Wells' },
        { code: 'N', name: 'Numerical model' },
        { key: 'aquifer-notations', name: 'Aquifer notations' },
        { code: 'W', name: 'Water budget' },
        { key: 'water-quality', name: 'Water quality information' },
        { key: 'aquifer-connected', name: 'Hydraulically connected (screening level)' },
        { code: 'G', name: 'Groundwater Surface Water Interactions' },
        { code: 'I', name: 'Other information' }
      ],
      waterWithdrawlVolume: '',
      factsheetRe: /[_ -]factsheet[_ -]*.*\.pdf$/i,
      loadingAquifer: false,
      loadingFiles: false,
      loadingMap: false,
      loadingForm: false,
      licenceUsageChartOptions: {
        tooltips: {
          callbacks: {
            label (tooltipItem, data) {
              return data.labels[tooltipItem.index]
            }
          }
        }
      },
      licenceQuantityChartOptions: {}
    }
  },
  computed: {
    ...mapGetters(['userRoles']),
    ...mapGetters('aquiferStore/view', {
      uncorrelatedWells: 'wellsWithoutAquiferCorrelation'
    }),
    ...mapGetters('aquiferStore/notations', [
      'getAquiferNotationsById'
    ]),
    ...mapState('documentState', [
      'files_uploading',
      'file_upload_error',
      'file_upload_success',
      'upload_files',
      'shapefile',
      'shapefile_uploading',
      'shapefile_upload_message',
      'shapefile_upload_success'
    ]),
    ...mapState('aquiferStore/view', [
      'record',
      'aquiferFiles',
      'aquiferWells'
    ]),
    ...mapState('aquiferStore/view', {
      storedId: 'id'
    }),
    id () { return parseInt(this.$route.params.id) || null },
    editMode () { return this.edit },
    viewMode () { return !this.edit },
    licenceDetails () {
      return this.record.licence_details || { usage: [], lic_qty: [], obs_wells: [] }
    },
    licenceUsageChartData () {
      const groupedLicenses = groupBy(this.licenceDetails.usage, 'purpose__description')
      const chartData = Object.values(groupedLicenses).map((val) => {
        return Math.round(sumBy(val, o => o.total_qty) / ONE_MILLION * 100) / 100
      })
      return chartData
    },
    licenceUsageChartLabels () {
      const groupedLicenses = groupBy(this.licenceDetails.lic_qty, 'purpose__description')
      const chartLabels = Object.keys(groupedLicenses).map((purpose, i) => {
        const label = purpose.split(' - ')[1] // the label, without code.
        const mcm = this.licenceUsageChartData[i]
        return `${label} ${mcm === 0 ? '<0.01' : mcm}`
      })
      return chartLabels
    },
    licenceQuantityChartData () {
      const groupedLicenses = groupBy(this.licenceDetails.lic_qty, 'purpose__description')
      const chartData = Object.values(groupedLicenses).map((val) => {
        return sumBy(val, o => o.total_qty)
      })
      return chartData
    },
    licenceQuantityChartLabels () {
      const groupedLicenses = groupBy(this.licenceDetails.lic_qty, 'purpose__description')
      const chartLabels = Object.keys(groupedLicenses).map((label) => {
        return label.split(' - ')[1] // the label, without code.
      })
      return chartLabels
    },
    obsWells () {
      return this.licenceDetails.obs_wells || []
    },
    obsWellsByStatus () {
      const sortedWells = orderBy(this.obsWells, ['hasLevelAnalysis', 'waterLevels'], ['desc', 'asc']) // sorts so wells with waterLevels are at the top.
      const wellsByStatus = groupBy(sortedWells, 'observation_well_status') // groups wells into active and inactive categories
      return wellsByStatus
    },
    activeObsWells () {
      return orderBy(this.obsWellsByStatus.Active || [], ['observation_well_number'])
    },
    inactiveObsWells () {
      return orderBy(this.obsWellsByStatus.Inactive || [], ['observation_well_number'])
    },
    inactiveObsWellsWithWaterLevel () {
      // inactive wells with water level analysis
      return this.inactiveObsWells.filter((w) => w.waterLevels)
    },
    inativeObsWellsWithOutWaterLevel () {
      // inactive wells without water level analysis
      return this.inactiveObsWells.filter((w) => !w.waterLevels)
    },
    noObsWells () {
      // Show the "No information available." message when there are no obs wells to show
      return this.activeObsWells.length === 0 && this.inactiveObsWells.length === 0
    },
    errorNotFound () {
      return this.error && this.error.status === 404
    },
    breadcrumbs () {
      const breadcrumbs = [
        {
          text: 'Aquifer Search',
          to: { name: 'aquifers-home' }
        }
      ]

      if (this.editMode) {
        breadcrumbs.push(...[
          {
            text: `Aquifer ${this.id} Summary`,
            to: { name: 'aquifers-view', params: { id: this.id } }
          },
          {
            text: 'Edit Aquifer',
            active: true
          }
        ])
      } else {
        breadcrumbs.push({
          text: this.errorNotFound ? 'Not found' : 'Aquifer Summary',
          active: true
        })
      }

      return breadcrumbs
    },
    isRetired () {
      const { retire_date: retireDate } = this.record
      if (retireDate) {
        return new Date(retireDate) < new Date()
      }

      return false
    },
    isUnpublished () {
      const { effective_date: effectiveDate, expiry_date: expiryDate } = this.record
      if (effectiveDate && expiryDate) {
        return new Date(effectiveDate) > new Date() || new Date(expiryDate) < new Date()
      }

      return false
    },
    aquiferNotations () {
      return this.getAquiferNotationsById(this.id, this.record.geom)
    }
  },
  watch: {
    id () {
      if (this.id !== this.storedId) {
        this.fetch()
      }
    },
    editMode (editMode) {
      if (editMode) {
        this.loadForm()
      }
    },
    licenceDetails (newLDetails, oldLDetails) {
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
      return ((value.getMonth() + 1) + '/' + value.getDate() + '/' + value.getFullYear())
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
    ...mapActions('aquiferStore/view', [
      'resetAquiferData'
    ]),
    ...mapMutations('aquiferStore/view', [
      'setAquiferRecord',
      'setAquiferFiles',
      'setAquiferWells'
    ]),
    loadForm () {
      this.loadingForm = true
      ApiService.query(`aquifers/${this.id}/edit`)
        .then((response) => {
          this.loadingForm = false
          this.form = response.data
        })
        .catch(() => {
          this.loadingForm = false
        })
    },
    bySection (resources, section) {
      return (resources || []).filter(function (resource) {
        return resource.section_code === section.code
      })
    },
    handleSaveSuccess (response) {
      this.fetchAquifer()

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
      let writableRecord = cloneDeep(this.form)
      delete writableRecord.licence_details
      delete writableRecord.geom
      delete writableRecord.area
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
      this.fetchAquifer()
    },
    navigateToEdit () {
      this.showSaveSuccess = false
      this.$router.push({ name: 'aquifers-edit', params: { id: this.id } })
    },
    print () {
      window.print()
    },
    fetch () {
      this.error = undefined
      this.resetAquiferData()

      this.fetchAquifer()
      this.fetchWells()
      this.fetchFiles()
    },
    fetchAquifer (id = this.id) {
      this.loadingAquifer = true
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

          const obsWells = responseData.licence_details.obs_wells
          Promise.all(
            obsWells.map((owell) => this.getWaterLevels(owell))
          ).then(() => {
            this.setAquiferRecord(responseData)
          })
        })
        .catch((e) => {
          this.error = e.response
        })
        .finally(() => {
          this.loadingAquifer = false
        })
    },
    fetchFiles (id = this.id) {
      this.loadingFiles = true
      return ApiService.query(`aquifers/${id}/files`)
        .then((response) => {
          this.setAquiferFiles(response.data)
          this.loadingFiles = false
        })
    },
    fetchWells (id = this.id) {
      const maxResults = MAX_API_RESULT_AND_EXPORT_COUNT // the API max
      const params = { intersects_aquifer_id: id, limit: maxResults }
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
          this.setAquiferWells(wells || [])
        })
    },
    getWaterLevels (owell) {
      owell.hasLevelAnalysis = false
      owell.fetchingAnalysis = true
      let wellNumber = owell.observation_well_number
      const url = `https://catalogue.data.gov.bc.ca/api/3/action/datastore_search?resource_id=a8933793-eadb-4a9c-992c-da4f6ac8ca51&fields=EMS_ID,Well_Num,trend_line_slope,category&filters=%7b%22Well_Num%22:%22${wellNumber}%22%7d`

      return ApiService.query(url).then((response) => {
        owell.errorFetching = false
        owell.fetchingAnalysis = false
        if (response.data.result.records.length > 0) {
          const { category } = response.data.result.records[0]
          owell.hasLevelAnalysis = category.toUpperCase() !== 'N/A'
          owell.waterLevels = category
        }
      }, () => {
        // Swallow any API error from https://catalogue.data.gov.bc.ca/api
        owell.fetchingAnalysis = false
        owell.errorFetching = true
      })
    },
    setWaterVolume (details) {
      if (details.usage && details.usage.constructor === Array && details.usage.length > 0) {
        this.waterWithdrawlVolume = sumBy(details.usage, 'total_qty')
      }
    },
    sanitizeResourceUrl (url) {
      const sanitized = sanitizeUrl(url)
      return encodeURI(sanitized)
    }
  }
}
</script>

<style lang="scss">
#aquifer-detail {

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

  .main-card > .card-body {
    padding: 0;
    margin: 0;

    & > .alert {
      margin: 1.25rem;
    }
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

  .aquifer-information-list {
    & > li {
      margin: 0.7rem 0;
    }

    dt, dd {
      display: inline-block;
      vertical-align: top;
      width: 50%;
      font-size: 1rem;
    }

    dt {
      padding-right: 2rem;
      font-weight: bold;
    }

    dd {
      padding-left: 2rem;
    }
  }

  .pie-chart-title {
    font-weight: bold !important;
    font-size: 1rem !important;
  }
  .pie-chart-container {
    margin: 0 auto;
  }

  .aquifer-main-information-list .row {
    & > div {
      padding-bottom: 0.7rem;
    }

    & > :nth-child(odd) {
      font-weight: bold;
      border-right: 1px solid rgba(0,0,0,0.1);
    }
  }

  .observational-wells {
    .obs-wells-wo-well-level span.observation-well:not(:last-child):after {
      content: ", ";
    }
  }

  #licenses li {
    list-style: none;
    display: inline;

    &:not(:last-child):after {
      content: ', ';
    }
  }

  #form-loading-spinner {
    position: absolute;
    top: 13px;
    left: 50%;
  }

  @media print {
    a:not(.d-print-url) {
      text-decoration: none !important;
    }

    a.d-print-url[href]::after {
      content: " (" attr(href) ") ";
      word-break: break-all;
    }

    .aquifer-information-list {
      dt {
        width: 25%;
      }

      dd {
        width: 75%;
      }

      .row > :nth-child(odd) {
        border: none;
      }
    }

    main {
      margin-bottom: 0 !important;

      & > .card.container {
        padding-bottom: 0 !important;
      }
    }

    body, main, .card, .aquifer-details {
      display: block !important;
    }
  }
}
</style>
