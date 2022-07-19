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
  <div class="well-detail">
    <div v-if="loading">
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
    </div>
    <div v-else>
      <b-card no-body class="mb-3 container d-print-none">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"/>
      </b-card>
      <b-card v-if="errorNotFound" class="container p-1">
        <h1>Not Found</h1>
        <p>The page you are looking for was not found.</p>
      </b-card>
      <b-card v-else class="container p-1">
        <b-alert
            show
            variant="info"
            class="mb-3"
            v-for="(survey, index) in surveys"
            :key="`survey ${index}`">
          <p class="m-0">
            <a :href="survey.survey_link">
              {{ survey.survey_introduction_text }}
            </a>
          </p>
        </b-alert>
        <b-alert show v-if="show.edit && isUnpublished" variant="warning">
          This well is unpublished and will be hidden from DataBC, iMapBC, GWELLS Well Search, and the CSV/XLS export.
        </b-alert>
        <!-- SUMMARY -->
        <fieldset id="summary_fieldset" class="detail-section mb-3">
          <legend>
            <span class="h2">Well Summary</span>
            <div class="float-right d-print-none">
              <router-link v-if="show.edit" :to="{ name: 'SubmissionsEdit', params: { id } }" class="mr-3">
                <button class="btn btn-primary mb-1">Edit</button>
              </router-link>
              <span class="print-notice">For best print results, use the Chrome browser</span>
              <b-btn variant="light" aria-label="Print" class="mb-1" @click="handlePrint"><i class="fa fa-lg fa-print"></i></b-btn>
            </div>
          </legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Tag Number:</span> {{ well.well_tag_number }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Status:</span> {{ well.well_status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Observation Well Number: </span>
              <a
                v-if="well.observation_well_number"
                id="obs_well_number"
                :href="`https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20${well.observation_well_number}`"
                target="_blank"
              >{{ well.observation_well_number }}</a>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ well.identification_plate_number }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Class:</span> {{ well.well_class }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Observation Well Status:</span> {{ well.observation_well_status }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Owner Name:</span> {{ well.owner_full_name }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Subclass:</span> {{ well.well_subclass }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Environmental Monitoring System (EMS) ID:</span> {{ well.ems }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Intended Water Use:</span> {{ well.intended_water_use }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Aquifer Number: </span>
              <router-link :to="{ name: 'aquifers-view', params: { id: well.aquifer } }">
                {{ well.aquifer }}
              </router-link>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Alternative specs submitted:</span> {{ well.alternative_specs_submitted }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Condition:</span> {{ well.artesian_conditions | nullBooleanToYesNo }}</b-col>
          </b-row>
        </fieldset>

        <!-- LINKS -->
        <fieldset id="jump_links_fieldset" class="d-print-none detail-section my-3">
            <legend>Sections</legend>
            <b-row>
              <b-col cols="12" md="4">
                <div><a class="jump_link" href="#location_information_fieldset">Location Information</a></div>
                <div><a class="jump_link" href="#well_activity_fieldset">Well Activity</a></div>
                <div><a class="jump_link" href="#well_work_dates_fieldset">Well Work Dates</a></div>
                <div><a class="jump_link" href="#well_completion_data_fieldset">Well Completion Data and Artesian Flow</a></div>
                <div><a class="jump_link" href="#lithology_fieldset">Lithology</a></div>
              </b-col>
              <b-col cols="12" md="4">
                <div><a class="jump_link" href="#casing_fieldset">Casing Details</a></div>
                <div><a class="jump_link" href="#surface_seal_fieldset">Surface Seal and Backfill Details</a></div>
                <div><a class="jump_link" href="#liner_details_fieldset">Liner Details</a></div>
                <div><a class="jump_link" href="#screen_details_fieldset">Screen Details</a></div>
                <div><a class="jump_link" href="#well_development_fieldset">Well Development</a></div>
              </b-col>
              <b-col cols="12" md="4">
                <div><a class="jump_link" href="#well_yield_fieldset">Well Yield</a></div>
                <div><a class="jump_link" href="#well_decommissioning_fieldset">Well Decommissioning</a></div>
                <div><a class="jump_link" href="#well_comments_fieldset">Comments</a></div>
                <div v-if="config && config.enable_documents"><a class="jump_link" href="#documents_fieldset">Documentation</a></div>
                <div><a class="jump_link" href="#disclaimer_fieldset">Disclaimer</a></div>
              </b-col>
            </b-row>
        </fieldset>

        <!-- LICENSING -->
        <fieldset id="well_licensing_fieldset" class="my-3 detail-section">
          <legend>Licensing Information</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Licensed Status:</span> {{ wellLicence.status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Licence Number:</span>&nbsp;
              <a :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${wellLicence.number}`" target="_blank">
                {{ wellLicence.number }}
              </a>
            </b-col>
            <b-col cols="12" md="4"></b-col>
          </b-row>
        </fieldset>

        <!-- LOCATION -->
        <fieldset id="location_information_fieldset" class="my-3 detail-section">
          <legend>Location Information</legend>
          <b-row>
            <b-col cols="12" md="6" xl="5">
              <b-row>
                <b-col><span class="font-weight-bold">Street Address:</span> {{ well.street_address }}</b-col>
              </b-row>
              <b-row>
                <b-col><span class="font-weight-bold">Town/City:</span> {{ well.city }}</b-col>
              </b-row>
              <b-row>
                <b-col>
                  <div class="my-3"><span class="font-weight-bold">Legal Description:</span></div>
                  <div class="table-responsive">
                    <table class="table table-sm table-striped table-bordered">
                      <tbody>
                        <tr>
                          <th class="w-50">Lot</th>
                          <td>{{ well.legal_lot }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Plan</th>
                          <td>{{ well.legal_plan }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">District Lot</th>
                          <td>{{ well.legal_district_lot }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Block</th>
                          <td>{{ well.legal_block }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Section</th>
                          <td>{{ well.legal_section }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Township</th>
                          <td>{{ well.legal_township }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Range</th>
                          <td>{{ well.legal_range }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Land District</th>
                          <td>{{ well.land_district }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Property Identification Description (PID)</th>
                          <td>{{ well.legal_pid }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <div>
                      <span class="font-weight-bold">Description of Well Location:</span> {{ well.well_location_description }}
                    </div>
                  </div>
                </b-col>
              </b-row>
            </b-col>
            <b-col cols="12" md="6" xl="6" offset-xl="1">
              <single-well-map :latitude="well.latitude" :longitude="well.longitude"/>
              <div class="font-weight-bold mt-5">
                Geographic Coordinates - North American Datum of 1983 (NAD 83)
              </div>
              <b-row>
                <b-col cols="12" md="4"><span class="font-weight-bold">Latitude:</span> {{well.latitude}}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Longitude:</span> {{well.longitude}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="4"><span class="font-weight-bold">UTM Easting:</span> {{ UTM.easting ? Math.round(UTM.easting) : ''}}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">UTM Northing:</span> {{ UTM.northing ? Math.round(UTM.northing) : ''}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="4"><span class="font-weight-bold">Zone:</span> {{UTM.zone}}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Coordinate Acquisition Code:</span> {{well.coordinate_acquisition_code}}</b-col>
              </b-row>
            </b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_activity_fieldset" class="my-3 detail-section">
          <legend>Well Activity</legend>
          <b-table
            id="submissionActivityTable"
            ref="submissionActivityTable"
            striped
            small
            bordered
            :items="well.submission_work_dates"
            responsive
            show-empty
            empty-text="There has been no activity related to this well."
            :per-page="submissionsPerPage"
            :current-page="submissionsPage"
            :fields="activity_fields"
          >
            <template slot="create_date" slot-scope="data">
              <div>
                {{ data.item.create_date | moment("MMMM Do YYYY [at] LT") }}
              </div>
            </template>
          </b-table>
          <b-pagination v-if="!!well.submission_work_dates && well.submission_work_dates.length > submissionsPerPage" size="md" :total-rows="well.submission_work_dates.length" v-model="submissionsPage" :per-page="submissionsPerPage" />
        </fieldset>

        <fieldset id="well_work_dates_fieldset" class="my-3 detail-section">
          <legend>Well Work Dates</legend>
          <b-table
            id="wellWorkDatesTable"
            ref="wellWorkDatesTable"
            striped
            bordered
            :items=wellDates
            :fields="work_date_fields"
          >
          </b-table>
        </fieldset>

        <fieldset id="well_completion_data_fieldset" class="my-3 detail-section">
          <legend>Well Completion Data</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Total Depth Drilled:</span> {{ well.total_depth_drilled | excludeZeroDecimals }} {{ well.total_depth_drilled ? 'ft bgl':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimated Well Yield:</span> {{ well.well_yield | excludeZeroDecimals }} {{ well.well_yield ? 'USgpm':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Static Water Level (BTOC):</span> {{ well.static_water_level | excludeZeroDecimals }} {{ well.static_water_level ? 'feet btoc': ''}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ well.finished_well_depth | excludeZeroDecimals }} {{ well.finished_well_depth ? 'ft bgl':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Cap:</span> {{ well.well_cap_type }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Flow:</span> {{ well.artesian_flow | excludeZeroDecimals }} {{ well.artesian_flow ? 'USgpm':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Final Casing Stick Up:</span> {{ well.final_casing_stick_up | excludeZeroDecimals }} {{ well.final_casing_stick_up ? 'inches':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Disinfected Status:</span> {{ well.well_disinfected_status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Pressure (head):</span> {{ well.artesian_pressure_head | excludeZeroDecimals }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Depth to Bedrock:</span> {{ well.bedrock_depth | excludeZeroDecimals }} {{ well.bedrock_depth ? 'feet bgl':''}}</b-col>
            <b-col cols="12" md="4">
              <span class="font-weight-bold">Drilling Method<span v-if="well.drilling_methods && well.drilling_methods.length > 1">s</span>:</span>
              <span v-for="(method, index) in well.drilling_methods" :key="`drillingMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Pressure (PSI):</span> {{ well.artesian_pressure | excludeZeroDecimals }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Ground elevation:</span> {{ well.ground_elevation | excludeZeroDecimals }} {{ well.ground_elevation ? 'feet':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ well.ground_elevation_method }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Orientation of Well:</span> {{ well.well_orientation_status }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="lithology_fieldset" class="my-3 detail-section">
          <legend>Lithology</legend>
          <b-table
            striped
            small
            bordered
            :items="well.lithologydescription_set"
            show-empty
            :fields="lithology_fields">
            <template slot="start" slot-scope="data">{{ data.item.start | excludeZeroDecimals }}</template>
            <template slot="end" slot-scope="data">{{ data.item.end | excludeZeroDecimals }}</template>
            <template slot="water_bearing_estimated_flow" slot-scope="data">{{ data.item.water_bearing_estimated_flow | excludeZeroDecimals }}</template>
          </b-table>
        </fieldset>

        <fieldset id="casing_fieldset" class="my-3 detail-section">
          <legend>Casing Details</legend>
          <div class="table-responsive">
            <b-table
                striped
                small
                bordered
                :items="well.casing_set"
                :fields="['from', 'to', 'casing_type', 'casing_material', 'diameter', 'wall_thickness', 'drive_shoe']"
                show-empty>

              <template slot="from" slot-scope="data">{{ data.item.start | excludeZeroDecimals }}</template>
              <template slot="HEAD_from" slot-scope="data">{{ data.label }} (ft bgl)</template>
              <template slot="to" slot-scope="data">{{ data.item.end | excludeZeroDecimals }}</template>
              <template slot="HEAD_to" slot-scope="data">{{ data.label }} (ft bgl)</template>
              <template slot="casing_type" slot-scope="data">{{codeToDescription('casing_codes', data.item.casing_code)}}</template>
              <template slot="casing_material" slot-scope="data">{{codeToDescription('casing_materials', data.item.casing_material)}}</template>
              <template slot="HEAD_diameter" slot-scope="data">{{ data.label }} (in)</template>
              <template slot="diameter" slot-scope="data">{{ data.item.diameter | excludeZeroDecimals }}</template>
              <template slot="HEAD_wall_thickness" slot-scope="data">{{ data.label }} (in)</template>
              <template slot="wall_thickness" slot-scope="data">{{ data.item.wall_thickness | excludeZeroDecimals }}</template>
              <template slot="drive_shoe" slot-scope="data">{{codeToDescription('drive_shoe', data.item.drive_shoe_status)}}</template>
            </b-table>
          </div>
        </fieldset>

        <fieldset id="surface_seal_fieldset" class="my-3 detail-section">
          <legend>Surface Seal and Backfill Details</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Material:</span> {{ codeToDescription('surface_seal_materials', well.surface_seal_material) }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Material Above Surface Seal:</span> {{ codeToDescription('surface_seal_materials', well.backfill_above_surface_seal) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Installation Method:</span> {{ codeToDescription('surface_seal_methods', well.surface_seal_method) }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Depth:</span> {{ well.backfill_depth | excludeZeroDecimals }} {{ well.backfill_depth ? 'feet':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Thickness:</span> {{ well.surface_seal_thickness | excludeZeroDecimals }} {{ well.surface_seal_thickness ? 'inches':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Depth:</span> {{ well.surface_seal_depth | excludeZeroDecimals }} {{ well.surface_seal_depth ? 'feet':''}}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="liner_details_fieldset" class="my-3 detail-section">
          <legend>Liner Details</legend>
          <b-row>
            <b-col cols="12" md="6">
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Material:</span> {{ codeToDescription('liner_materials', well.liner_material) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Diameter:</span> {{ well.liner_diameter | excludeZeroDecimals }} {{ well.liner_diameter ? 'inches':'' }}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Thickness:</span> {{ well.liner_thickness | excludeZeroDecimals }} {{ well.liner_thickness ? 'inches':'' }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner from:</span> {{ well.liner_from | excludeZeroDecimals }} {{ well.liner_from ? '(ft bgl)':'' }}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner to:</span> {{ well.liner_to | excludeZeroDecimals }} {{ well.liner_to ? '(ft bgl)':'' }}</b-col>
              </b-row>
            </b-col>
            <b-col cols="12" md="6">
              <div class="font-weight-bold">Liner perforations</div>
              <b-table
                  striped
                  small
                  bordered
                  :items="well.linerperforation_set"
                  :fields="['from', 'to']"
                  show-empty
              >
                <template slot="HEAD_from" slot-scope="data">{{data.label}} (ft bgl)</template>
                <template slot="from" slot-scope="data">{{ data.item.start | excludeZeroDecimals }}</template>
                <template slot="HEAD_to" slot-scope="data">{{data.label}} (ft bgl)</template>
                <template slot="to" slot-scope="data">{{ data.item.end | excludeZeroDecimals }}</template>
              </b-table>
            </b-col>
          </b-row>
        </fieldset>

        <fieldset id="screen_details_fieldset" class="my-3 detail-section">
          <legend>Screen Details</legend>
          <b-row>
            <b-col cols="12" md="4">
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', well.screen_intake_method) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Type:</span> {{ codeToDescription('screen_types', well.screen_type) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Material:</span> {{ codeToDescription('screen_materials', well.screen_material) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Opening:</span> {{ codeToDescription('screen_openings', well.screen_opening) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', well.screen_bottom) }}</b-col>
              </b-row>
            </b-col>
            <b-col cols="12" md="8">
              <div class="font-weight-bold">Installed Screens</div>
              <b-table
                  striped
                  small
                  bordered
                  :items="well.screen_set"
                  :fields="['from', 'to', 'diameter', 'assembly_type', 'slot_size']"
                  show-empty
                  >
                <template slot="HEAD_from" slot-scope="data">{{data.label}} (ft bgl)</template>
                <template slot="from" slot-scope="data">{{data.item.start}}</template>
                <template slot="HEAD_to" slot-scope="data">{{data.label}} (ft bgl)</template>
                <template slot="to" slot-scope="data">{{data.item.end}}</template>
                <template slot="HEAD_diameter" slot-scope="data">{{data.label}} (in)</template>
                <template slot="diameter" slot-scope="data">{{data.item.diameter}}</template>
                <template slot="assembly_type" slot-scope="data">{{codeToDescription('screen_assemblies', data.item.assembly_type)}}</template>
              </b-table>
            </b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_development_fieldset" class="my-3 detail-section">
          <legend>Well Development</legend>
          <b-row>
            <b-col cols="12" md="4">
              <span class="font-weight-bold">Developed by:</span>
              <span v-for="(method, index) in well.development_methods" :key="`developmentMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Development Total Duration:</span> {{ well.development_hours | excludeZeroDecimals }} {{ well.development_hours ? 'hours':'' }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_yield_fieldset" class="my-3 detail-section">
          <legend>Well Yield</legend>

          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Method:</span> {{codeToDescription('yield_estimation_methods', well.yield_estimation_method)}} </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Rate:</span> {{ well.yield_estimation_rate | excludeZeroDecimals }} {{ well.yield_estimation_rate ? 'USgpm':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Duration:</span> {{ well.yield_estimation_duration | excludeZeroDecimals }} {{ well.yield_estimation_duration ? 'hours':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Static Water Level Before Test:</span> {{ well.static_level_before_test | excludeZeroDecimals }} {{well.static_level_before_test ? 'ft (btoc)':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Drawdown:</span> {{ well.drawdown | excludeZeroDecimals }} {{ well.drawdown ? 'ft (btoc)':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Hydrofracturing Performed:</span> {{well.hydro_fracturing_performed | nullBooleanToYesNo}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Increase in Yield Due to Hydrofracturing:</span> {{ well.hydro_fracturing_yield_increase | excludeZeroDecimals }} {{ well.hydro_fracturing_yield_increase ? 'USgpm':'' }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_decommissioning_fieldset" class="my-3 detail-section">
          <legend>Well Decommission Information</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Reason for Decommission:</span> {{ well.decommission_reason }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Method of Decommission:</span> {{ well.decommission_method }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Sealant Material:</span> {{ well.decommission_sealant_material }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Material:</span> {{ well.decommission_backfill_material }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Decommission Details:</span> {{ well.decommission_details }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_comments_fieldset" class="my-3 detail-section">
          <legend>Comments</legend>
          <p>
            {{ well.comments ? well.comments : 'No comments submitted' }}
          </p>
          <p>
            <span class="font-weight-bold">Alternative Specs Submitted:</span> {{ well.alternative_specs_submitted | nullBooleanToYesNo }}
          </p>
        </fieldset>

        <fieldset id="documents_fieldset" class="detail-section my-3">
          <legend>Documents</legend>
          <documents :well="id"/>
        </fieldset>

        <fieldset id="disclaimer_fieldset" class="detail-section my-3">
          <legend>Disclaimer</legend>
          <p>
            The information provided should not be used as a basis for making financial or any other commitments. The Government of British Columbia accepts no liability for the accuracy, availability, suitability, reliability, usability, completeness or timeliness of the data or graphical depictions rendered from the data.
          </p>
        </fieldset>

      </b-card>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'

import SingleWellMap from '@/wells/components/SingleWellMap.vue'
import Documents from '@/wells/components/Documents.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ApiService from '@/common/services/ApiService.js'
import codeToDescription from '@/common/codeToDescription.js'

import { RESET_WELL_DATA } from '@/wells/store/actions.types.js'
import { SET_WELL_RECORD, SET_WELL_LICENCE } from '@/wells/store/mutations.types.js'

export default {
  name: 'WellDetail',
  components: {
    SingleWellMap,
    Documents
  },
  mixins: [
    convertCoordinatesMixin, codeToDescription
  ],
  data () {
    return {
      surveys: [],
      lithology_fields: {
        start: { label: 'From (ft bgl)' },
        end: { label: 'To (ft bgl)' },
        lithology_raw_data: { label: 'Raw Data' },
        lithology_description: { label: 'Description' },
        lithology_moisture: { label: 'Moisture' },
        lithology_colour: { label: 'Colour' },
        lithology_hardness: { label: 'Hardness' },
        lithology_observation: { label: 'Observations' },
        water_bearing_estimated_flow: { label: 'Water Bearing Flow Estimate (USGPM)' }
      },
      activity_fields: {
        well_activity_description: { label: 'Activity', sortable: true },
        work_start_date: { label: 'Work Start Date', sortable: true },
        work_end_date: { label: 'Work End Date', sortable: true },
        drilling_company: { label: 'Drilling Company', sortable: true },
        create_date: { label: 'Date Entered', sortable: true }
      },
      work_date_fields: {
        construction_start_date: { label: 'Start Date of Construction', class: 'text-center' },
        construction_end_date: { label: 'End Date of Construction', class: 'text-center' },
        alteration_start_date: { label: 'Start Date of Alteration', class: 'text-center' },
        alteration_end_date: { label: 'End Date of Alteration', class: 'text-center' },
        decommission_start_date: { label: 'Start Date of Decommission', class: 'text-center' },
        decommission_end_date: { label: 'End Date of Decommission', class: 'text-center' }
      },
      submissionsPerPage: 5,
      submissionsPage: 1,
      loading: false,
      error: null
    }
  },
  computed: {
    id () { return parseInt(this.$route.params.id) || null },
    wellDates () {
      return [{
        construction_start_date: this.well.construction_start_date,
        construction_end_date: this.well.construction_end_date,
        alteration_start_date: this.well.alteration_start_date,
        alteration_end_date: this.well.alteration_end_date,
        decommission_start_date: this.well.decommission_start_date,
        decommission_end_date: this.well.decommission_end_date
      }]
    },
    errorNotFound () {
      return this.error && this.error.status === 404
    },
    analytics () {
      return !!window.ga
    },
    show () {
      return {
        edit: !!this.config && this.userRoles.wells.edit === true
      }
    },
    UTM () {
      // converts form lat/long and returns an object containing UTM easting, northing, and zone
      if (this.well && this.well.latitude && this.well.longitude) {
        return this.convertToUTM(Number(this.well.longitude), Number(this.well.latitude))
      }
      return {}
    },
    breadcrumbs () {
      return [
        {
          text: 'Well Search',
          to: { name: 'wells-home' }
        },
        {
          text: this.errorNotFound ? 'Not found' : 'Well Summary',
          active: true
        }
      ]
    },
    isUnpublished () {
      return !this.well.is_published
    },
    ...mapGetters(['userRoles', 'config', 'well', 'wellLicence', 'storedWellId'])
  },
  methods: {
    handlePrint () {
      if (window.ga) {
        window.ga('send', 'event', 'Button', 'print', 'Wells Summary Print')
      }
      window.print()
    },
    fetchWellData () {
      this.loading = true
      this.error = null

      this[RESET_WELL_DATA]()

      return Promise.all([
        ApiService.get('wells', this.id).then((response) => {
          return response.data || {}
        }).catch((e) => {
          this.error = e.response
          throw e
        }),
        ApiService.query(`wells/licensing?well_tag_number=${this.id}`).then((response) => {
          return response.data || {}
        })
      ]).then(([wellData, licenceData]) => {
        this[SET_WELL_RECORD](wellData)
        this[SET_WELL_LICENCE](licenceData)
      }).finally(() => {
        this.loading = false
      })
    },
    fetchSurveys () {
      ApiService.query('surveys').then((response) => {
        if (response.data) {
          response.data.forEach((survey) => {
            if (survey.survey_page === 'w' && survey.survey_enabled) {
              this.surveys.push(survey)
            }
          })
        }
      })
    },
    ...mapMutations([ SET_WELL_RECORD, SET_WELL_LICENCE ]),
    ...mapActions([ RESET_WELL_DATA ])
  },
  watch: {
    id () {
      if (this.id !== this.storedWellId) {
        this.fetchWellData()
      }
    }
  },
  created () {
    this.fetchSurveys()

    if (this.id === null) {
      this.error = `Unable to load well '${this.id}'`
    }

    if (this.id !== this.storedWellId) {
      this.fetchWellData()
    }
  }
}
</script>

<style lang="scss">
.well-detail .print-notice {
  font-size: 1rem;
}

@media print {
  .well-detail {
    fieldset {
      page-break-inside: avoid;
    }

    .card {
      border: none;
    }

    table.b-table > thead > tr > th {
      &.sorting::before,
      &.sorting::after,
      &.sorting_desc::before,
      &.sorting_desc::after,
      &.sorting_asc::before,
      &.sorting_desc::after {
        content: none;
      }
    }
  }
}
</style>
