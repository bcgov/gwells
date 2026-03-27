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
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Tag Number:</span> {{ well_tag_number }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Status:</span> {{ well_status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Observation Well Number: </span>
              <a
                v-if="observation_well_number"
                id="obs_well_number"
                :href="`https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20${observation_well_number}`"
                target="_blank"
              >{{ observation_well_number }}</a>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ identification_plate_number }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Class:</span> {{ well_class }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Observation Well Status:</span> {{ observation_well_status }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Owner Name:</span> {{ owner_full_name }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Subclass:</span> {{ well_subclass }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Environmental Monitoring System (EMS) ID:</span> {{ ems }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Intended Water Use:</span> {{ intended_water_use }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Aquifer Number: </span>
              <router-link :to="{ name: 'aquifers-view', params: { id: aquifer } }">
                {{ aquifer }}
              </router-link>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Alternative specs submitted:</span> {{ alternative_specs_submitted }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Condition:</span> {{ booleanToYesNo(artesian_conditions) }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Technical Report:</span>
              <a
                v-if="technical_report"
                id="technical_report"
                href='https://foirequestform.gov.bc.ca/?general='
                target="_blank"
                rel="noopener noreferrer"
              > Report Available</a>
              <span v-if="!technical_report"> N/A</span>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Drinking Water Area Indicator:</span> {{ booleanToYesNo(drinking_water_protection_area_ind) }}</b-col>
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
                <div><a class="jump_link" href="#aquifer_parameters_fieldset">Aquifer Parameters</a></div>
                <div><a class="jump_link" href="#surface_seal_fieldset">Surface Seal and Backfill Details</a></div>
                <div><a class="jump_link" href="#liner_details_fieldset">Liner Details</a></div>
                <div><a class="jump_link" href="#screen_details_fieldset">Screen Details</a></div>
              </b-col>
              <b-col cols="12" md="4">
                <div><a class="jump_link" href="#well_development_fieldset">Well Development</a></div>
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
            <b-col cols="12" md="4"><span class="font-weight-bold">Licensed Status:</span> {{ recordLicence?.status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Licence Number{{ recordLicence.number.length > 1 ? "s" : "" }}:</span>&nbsp;
              <a v-for="(licence, index) in recordLicence.number" :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${licence}`" target="_blank">
                {{ licence}}{{ index + 1 < recordLicence.number.length ? ", " : ""}}
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
                <b-col><span class="font-weight-bold">Street Address:</span> {{ street_address }}</b-col>
              </b-row>
              <b-row>
                <b-col><span class="font-weight-bold">Town/City:</span> {{ city }}</b-col>
              </b-row>
              <b-row>
                <b-col>
                  <div class="my-3"><span class="font-weight-bold">Legal Description:</span></div>
                  <div class="table-responsive">
                    <table class="table table-sm table-striped table-bordered">
                      <tbody>
                        <tr>
                          <th class="w-50">Lot</th>
                          <td>{{ legal_lot }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Plan</th>
                          <td>{{ legal_plan }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">District Lot</th>
                          <td>{{ legal_district_lot }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Block</th>
                          <td>{{ legal_block }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Section</th>
                          <td>{{ legal_section }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Township</th>
                          <td>{{ legal_township }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Range</th>
                          <td>{{ legal_range }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Land District</th>
                          <td>{{ land_district }}</td>
                        </tr>
                        <tr>
                          <th class="w-50">Property Identification Description (PID)</th>
                          <td>{{ legal_pid }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <div>
                      <span class="font-weight-bold">Description of Well Location:</span> {{ well_location_description }}
                    </div>
                  </div>
                </b-col>
              </b-row>
            </b-col>
            <b-col cols="12" md="6" xl="6" offset-xl="1">
              <single-well-map :latitude="latitude" :longitude="longitude"/>
              <div class="font-weight-bold mt-5">
                Geographic Coordinates - North American Datum of 1983 (NAD 83)
              </div>
              <b-row>
                <b-col cols="12" md="4"><span class="font-weight-bold">Latitude:</span> {{latitude}}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Longitude:</span> {{longitude}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="4"><span class="font-weight-bold">UTM Easting:</span> {{ UTM.easting ? Math.round(UTM.easting) : ''}}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">UTM Northing:</span> {{ UTM.northing ? Math.round(UTM.northing) : ''}}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="4"><span class="font-weight-bold">Zone:</span> {{UTM.zone}}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Coordinate Acquisition Code:</span> {{coordinate_acquisition_code}}</b-col>
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
            :items="submission_work_dates"
            responsive
            show-empty
            empty-text="There has been no activity related to this well."
            :per-page="submissionsPerPage"
            :current-page="submissionsPage"
            :fields="activity_fields"
          >
            <template v-slot:cell(create_date)="data">
              <div>
                {{ formatDate(data.item.create_date, "MMMM Do YYYY [at] LT") }}
              </div>
            </template>
          </b-table>
          <b-pagination v-if="!!submission_work_dates && submission_work_dates.length > submissionsPerPage" size="md" :total-rows="submission_work_dates.length" v-model="submissionsPage" :per-page="submissionsPerPage" />
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
            <b-col cols="12" md="4"><span class="font-weight-bold">Total Depth Drilled:</span> {{ excludeZeroDecimals(total_depth_drilled) }} {{ total_depth_drilled ? 'ft bgl':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimated Well Yield:</span> {{ excludeZeroDecimals(well_yield) }} {{ well_yield ? 'USgpm':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Static Water Level (BTOC):</span> {{ excludeZeroDecimals(static_water_level) }} {{ static_water_level ? 'feet btoc': ''}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ excludeZeroDecimals(finished_well_depth) }} {{ finished_well_depth ? 'ft bgl':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Cap:</span> {{ well_cap_type }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Flow:</span> {{ excludeZeroDecimals(artesian_flow) }} {{ artesian_flow ? 'USgpm':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Final Casing Stick Up:</span> {{ excludeZeroDecimals(final_casing_stick_up) }} {{ final_casing_stick_up ? 'inches':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Disinfected Status:</span> {{ well_disinfected_status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Pressure (head):</span> {{ excludeZeroDecimals(artesian_pressure_head) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Depth to Bedrock:</span> {{ excludeZeroDecimals(bedrock_depth) }} {{ bedrock_depth ? 'feet bgl':''}}</b-col>
            <b-col cols="12" md="4">
              <span class="font-weight-bold">Drilling Method<span v-if="drilling_methods && drilling_methods.length > 1">s</span>:</span>
              <span v-for="(method, index) in drilling_methods" :key="`drillingMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Pressure (PSI):</span> {{ excludeZeroDecimals(artesian_pressure) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Ground elevation:</span> {{ excludeZeroDecimals(ground_elevation) }} {{ ground_elevation ? 'feet':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ ground_elevation_method }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Orientation of Well:</span> {{ well_orientation_status }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="lithology_fieldset" class="my-3 detail-section">
          <legend>Lithology</legend>
          <b-table
            striped
            small
            bordered
            :items="lithologydescription_set"
            show-empty
            :fields="lithology_fields">
            <template v-slot:cell(start)="data">{{ excludeZeroDecimals(data.item.start) }}</template>
            <template v-slot:cell(end)="data">{{ excludeZeroDecimals(data.item.end) }}</template>
            <template v-slot:cell(water_bearing_estimated_flow)="data">{{ excludeZeroDecimals(data.item.water_bearing_estimated_flow) }}</template>
          </b-table>
        </fieldset>

        <fieldset id="casing_fieldset" class="my-3 detail-section">
          <legend>Casing Details</legend>
          <div class="table-responsive">
            <b-table
                striped
                small
                bordered
                :items="casing_set"
                :fields="['from', 'to', 'casing_type', 'casing_material', 'diameter', 'wall_thickness', 'drive_shoe']"
                show-empty>

              <template v-slot:cell(from)="data">{{ excludeZeroDecimals(data.item.start) }}</template>
              <template v-slot:cell(HEAD_from)="data">{{ data.label }} (ft bgl)</template>
              <template v-slot:cell(to)="data">{{ excludeZeroDecimals(data.item.end) }}</template>
              <template v-slot:cell(HEAD_to)="data">{{ data.label }} (ft bgl)</template>
              <template v-slot:cell(casing_type)="data">{{codeToDescription('casing_codes', data.item.casing_code)}}</template>
              <template v-slot:cell(casing_material)="data">{{codeToDescription('casing_materials', data.item.casing_material)}}</template>
              <template v-slot:cell(HEAD_diameter)="data">{{ data.label }} (in)</template>
              <template v-slot:cell(diameter)="data">{{ excludeZeroDecimals(data.item.diameter) }}</template>
              <template v-slot:cell(HEAD_wall_thickness)="data">{{ data.label }} (in)</template>
              <template v-slot:cell(wall_thickness)="data">{{ excludeZeroDecimals(data.item.wall_thickness) }}</template>
              <template v-slot:cell(drive_shoe)="data">{{codeToDescription('drive_shoe', data.item.drive_shoe_status)}}</template>
            </b-table>
          </div>
        </fieldset>

        <fieldset id="surface_seal_fieldset" class="my-3 detail-section">
          <legend>Surface Seal and Backfill Details</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Material:</span> {{ codeToDescription('surface_seal_materials', surface_seal_material) }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Material Above Surface Seal:</span> {{ codeToDescription('surface_seal_materials', backfill_above_surface_seal) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Installation Method:</span> {{ codeToDescription('surface_seal_methods', surface_seal_method) }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Depth:</span> {{ excludeZeroDecimals(backfill_depth) }} {{ backfill_depth ? 'feet':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Thickness:</span> {{ excludeZeroDecimals(surface_seal_thickness) }} {{ surface_seal_thickness ? 'inches':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Depth:</span> {{ excludeZeroDecimals(surface_seal_depth) }} {{ surface_seal_depth ? 'feet':''}}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="liner_details_fieldset" class="my-3 detail-section">
          <legend>Liner Details</legend>
          <b-row>
            <b-col cols="12" md="6">
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Material:</span> {{ codeToDescription('liner_materials', liner_material) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Diameter:</span> {{ excludeZeroDecimals(liner_diameter) }} {{ liner_diameter ? 'inches':'' }}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Thickness:</span> {{ excludeZeroDecimals(liner_thickness) }} {{ liner_thickness ? 'inches':'' }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner from:</span> {{ excludeZeroDecimals(liner_from) }} {{ liner_from ? '(ft bgl)':'' }}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner to:</span> {{ excludeZeroDecimals(liner_to) }} {{ liner_to ? '(ft bgl)':'' }}</b-col>
              </b-row>
            </b-col>
            <b-col cols="12" md="6">
              <div class="font-weight-bold">Liner perforations</div>
              <b-table
                  striped
                  small
                  bordered
                  :items="linerperforation_set"
                  :fields="['from', 'to']"
                  show-empty
              >
                <template v-slot:cell(HEAD_from)="data">{{data.label}} (ft bgl)</template>
                <template v-slot:cell(from)="data">{{ excludeZeroDecimals(data.item.start) }}</template>
                <template v-slot:cell(HEAD_to)="data">{{data.label}} (ft bgl)</template>
                <template v-slot:cell(to)="data">{{ excludeZeroDecimals(data.item.end) }}</template>
              </b-table>
            </b-col>
          </b-row>
        </fieldset>

        <fieldset id="screen_details_fieldset" class="my-3 detail-section">
          <legend>Screen Details</legend>
          <b-row>
            <b-col cols="12" md="4">
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', screen_intake_method) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Type:</span> {{ codeToDescription('screen_types', screen_type) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Material:</span> {{ codeToDescription('screen_materials', screen_material) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Opening:</span> {{ codeToDescription('screen_openings', screen_opening) }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', screen_bottom) }}</b-col>
              </b-row>
            </b-col>
            <b-col cols="12" md="8">
              <div class="font-weight-bold">Installed Screens</div>
              <b-table
                  striped
                  small
                  bordered
                  :items="screen_set"
                  :fields="['from', 'to', 'diameter', 'assembly_type', 'slot_size']"
                  show-empty
                  >
                <template v-slot:cell(HEAD_from)="data">{{data.label}} (ft bgl)</template>
                <template v-slot:cell(from)="data">{{data.item.start}}</template>
                <template v-slot:cell(HEAD_to)="data">{{data.label}} (ft bgl)</template>
                <template v-slot:cell(to)="data">{{data.item.end}}</template>
                <template v-slot:cell(HEAD_diameter)="data">{{data.label}} (in)</template>
                <template v-slot:cell(diameter)="data">{{data.item.diameter}}</template>
                <template v-slot:cell(assembly_type)="data">{{codeToDescription('screen_assemblies', data.item.assembly_type)}}</template>
              </b-table>
            </b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_development_fieldset" class="my-3 detail-section">
          <legend>Well Development</legend>
          <b-row>
            <b-col cols="12" md="4">
              <span class="font-weight-bold">Developed by:</span>
              <span v-for="(method, index) in development_methods" :key="`developmentMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Development Total Duration:</span> {{ excludeZeroDecimals(development_hours) }} {{ development_hours ? 'hours':'' }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_yield_fieldset" class="my-3 detail-section">
          <legend>Well Yield</legend>

          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Method:</span> {{codeToDescription('yield_estimation_methods', yield_estimation_method)}} </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Rate:</span> {{ excludeZeroDecimals(yield_estimation_rate) }} {{ yield_estimation_rate ? 'USgpm':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Duration:</span> {{ excludeZeroDecimals(yield_estimation_duration) }} {{ yield_estimation_duration ? 'hours':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Static Water Level Before Test:</span> {{ excludeZeroDecimals(static_level_before_test) }} {{ static_level_before_test ? 'ft (btoc)':'' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Drawdown:</span> {{ excludeZeroDecimals(drawdown) }} {{ drawdown ? 'ft (btoc)':'' }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Hydrofracturing Performed:</span> {{booleanToYesNo(hydro_fracturing_performed)}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Increase in Yield Due to Hydrofracturing:</span> {{ excludeZeroDecimals(hydro_fracturing_yield_increase) }} {{ hydro_fracturing_yield_increase ? 'USgpm':'' }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_decommissioning_fieldset" class="my-3 detail-section">
          <legend>Well Decommission Information</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Reason for Decommission:</span> {{ decommission_reason }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Method of Decommission:</span> {{ decommission_method }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Sealant Material:</span> {{ decommission_sealant_material }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Material:</span> {{ decommission_backfill_material }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Decommission Details:</span> {{ decommission_details }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="aquifer_parameters_fieldset" class="my-3 detail-section">
          <legend>Pumping Test Information and Aquifer Parameters</legend>
          <div class="table-responsive">
            <b-table
                striped
                small
                bordered
                :items="aquifer_parameters_set"
                :fields="[
                  { key: 'start_date_pumping_test', label: 'Start Date' },
                  { key: 'pumping_test_description', label: 'Description' },
                  { key: 'test_duration', label: 'Test Duration (min)' },
                  { key: 'boundary_effect', label: 'Boundary Effect' },
                  { key: 'storativity', label: 'Storativity' },
                  { key: 'transmissivity', label: 'Transmissivity (m²/day)' },
                  { key: 'hydraulic_conductivity', label: 'Hydraulic Conductivity (m/day)' },
                  { key: 'specific_yield', label: 'Specific Yield' },
                  { key: 'specific_capacity', label: 'Specific Capacity (L/s/m)' },
                  { key: 'analysis_method', label: 'Analysis Method' },
                  { key: 'comments', label: 'Comments' }
                ]"
                show-empty>
                <template v-slot:head(pumping_test_description)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="test_duration" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="test_duration" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.pumping_test" ></b-popover>
                </template>
                <template v-slot:head(boundary_effect)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="boundary_effect" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="boundary_effect" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.boundary_effect" ></b-popover>
                </template>
                <template v-slot:head(storativity)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="storativity" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="storativity" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.storativity" ></b-popover>
                </template>
                <template v-slot:head(transmissivity)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="transmissivity" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="transmissivity" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.transmissivity" ></b-popover>
                </template>
                <template v-slot:head(hydraulic_conductivity)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="hydraulic_conductivity" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="hydraulic_conductivity" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.hydraulic_conductivity" ></b-popover>
                </template>
                <template v-slot:head(specific_yield)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="specific_yield" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="specific_yield" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.specific_yield" ></b-popover>
                </template>
                <template v-slot:head(specific_capacity)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="specific_capacity" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="specific_capacity" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.specific_capacity" ></b-popover>
                </template>
                <template v-slot:head(analysis_method)="data">
                  <span>{{ data.label }}</span>&nbsp;
                  <i id="analysis_method" class="fa fa-question-circle color-info fa-xs pt-0 mt-0 d-print-none" ></i>
                  <b-popover no-arrow target="analysis_method" placement="top" triggers="hover focus" :content="TOOLTIP_TEXT.pumping_test_information.analysis_method" ></b-popover>
                </template>
                <template v-slot:cell(pumping_test_description)="data">{{codeToDescription('pumping_test_description_codes', data.item.pumping_test_description)}}</template>
                <template v-slot:cell(boundary_effect)="data">{{codeToDescription('boundary_effect_codes', data.item.boundary_effect)}}</template>
                <template v-slot:cell(analysis_method)="data">{{codeToDescription('analysis_method_codes', data.item.analysis_method)}}</template>
                <template v-slot:cell(storativity)="data">{{data.item.storativity && parseFloat(data.item.storativity).toString()}}</template>
                <template v-slot:cell(transmissivity)="data">{{data.item.transmissivity && parseFloat(data.item.transmissivity).toString()}}</template>
                <template v-slot:cell(hydraulic_conductivity)="data">{{data.item.hydraulic_conductivity && parseFloat(data.item.hydraulic_conductivity).toString()}}</template>
            </b-table>
          </div>
        </fieldset>

        <fieldset id="well_comments_fieldset" class="my-3 detail-section">
          <legend>Comments</legend>
          <p>
            {{ comments ? comments : 'No comments submitted' }}
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
import { mapStores } from 'pinia'

import moment from 'moment'

import SingleWellMap from '@/wells/components/SingleWellMap.vue'
import Documents from '@/wells/components/Documents.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ApiService from '@/common/services/ApiService.js'
import codeToDescription from '@/common/codeToDescription.js'
import { useSubmissionStore } from '@/stores/submission.js'
import { RESET_WELL_DATA } from '@/wells/store/actions.types.js'
import { SET_WELL_RECORD, SET_WELL_LICENCE } from '@/wells/store/mutations.types.js'
import { TOOLTIP_TEXT } from '@/common/constants.js'
import { useWellsStore } from '@/stores/wells.js'
import { booleanToYesNo, excludeZeroDecimals } from '../../common/filters'

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
      TOOLTIP_TEXT: TOOLTIP_TEXT,
      surveys: [],
      lithology_fields: [
        { key: 'start', label: 'From (ft bgl)' },
        { key: 'end', label: 'To (ft bgl)' },
        { key: 'lithology_raw_data', label: 'Raw Data' },
        { key: 'lithology_description', label: 'Description' },
        { key: 'lithology_moisture', label: 'Moisture' },
        { key: 'lithology_colour', label: 'Colour' },
        { key: 'lithology_hardness', label: 'Hardness' },
        { key: 'lithology_observation', label: 'Observations' },
        { key: 'water_bearing_estimated_flow', label: 'Water Bearing Flow Estimate (USGPM)' }
      ],
      activity_fields: [
        { key: 'well_activity_description', label: 'Activity', sortable: true },
        { key: 'work_start_date', label: 'Work Start Date', sortable: true },
        { key: 'work_end_date', label: 'Work End Date', sortable: true },
        { key: 'drilling_company', label: 'Drilling Company', sortable: true },
        { key: 'create_date', label: 'Date Entered', sortable: true }
      ],
      work_date_fields: [
        { key: 'construction_start_date', label: 'Start Date of Construction', class: 'text-center' },
        { key: 'construction_end_date', label: 'End Date of Construction', class: 'text-center' },
        { key: 'alteration_start_date', label: 'Start Date of Alteration', class: 'text-center' },
        { key: 'alteration_end_date', label: 'End Date of Alteration', class: 'text-center' },
        { key: 'decommission_start_date', label: 'Start Date of Decommission', class: 'text-center' },
        { key: 'decommission_end_date', label: 'End Date of Decommission', class: 'text-center' }
      ],
      submissionsPerPage: 5,
      submissionsPage: 1,
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapStores(useWellsStore),
    well_tag_number () { return this.wellsStore.wellRecord?.well_tag_number ?? '' },
    well_status () { return this.wellsStore.wellRecord?.well_status ?? '' },
    observation_well_number () { return this.wellsStore.wellRecord?.observation_well_number ?? '' },
    identification_plate_number () { return this.wellsStore.wellRecord?.identification_plate_number ?? '' },
    well_class () { return this.wellsStore.wellRecord?.well_class ?? '' },
    owner_full_name () { return this.wellsStore.wellRecord?.owner_full_name ?? '' },
    well_subclass () { return this.wellsStore.wellRecord?.well_subclass ?? '' },
    ems () { return this.wellsStore.wellRecord?.ems ?? '' },
    intended_water_use () { return this.wellsStore.wellRecord?.intended_water_use ?? '' },
    aquifer () { return this.wellsStore.wellRecord?.aquifer ?? '' },
    alternative_specs_submitted () { return this.wellsStore.wellRecord?.alternative_specs_submitted ?? '' },
    artesian_conditions () { return this.wellsStore.wellRecord?.artesian_conditions ?? false },
    drinking_water_protection_area_ind () { return this.wellsStore.wellRecord?.drinking_water_protection_area_ind ?? false },
    recordLicence () { return this.wellLicence ?? { status: '', number: [] } },
    id () { return parseInt(this.$route.params.id) || null },
    wellDates () {
      return [{
        construction_start_date: this.construction_start_date,
        construction_end_date: this.construction_end_date,
        alteration_start_date: this.alteration_start_date,
        alteration_end_date: this.alteration_end_date,
        decommission_start_date: this.decommission_start_date,
        decommission_end_date: this.decommission_end_date
      }]
    },
    errorNotFound () {
      return this.error && this.error.status === 404
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
    ...mapGetters(['userRoles', 'config', 'codes'])
  },
  methods: {
    booleanToYesNo (value) {
      return booleanToYesNo(value)
    },
    excludeZeroDecimals (value) {
      return excludeZeroDecimals(value)
    },
    formatDate (value, format) {
      if (!value) {
        return ''
      }
      const m = moment(value)
      return m.isValid() ? m.format(format) : ''
    },
    handlePrint () {
      window.print()
    },
    fetchWellData () {
      this.loading = true
      this.error = null

      this.wellsStore.resetWellData();

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
        this.wellsStore.setWellRecord(wellData);
        this.recordLicence = licenceData;
        console.log('wellData', wellData);
        console.log('licenceData', licenceData);
        console.log('state', this.wellsStore.wellRecord)
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
  },
  watch: {
    id () {
      if (this.id !== this.storedWellId) {
        this.fetchWellData()
      }
    }
  },
  created () {
    this.wellsStore
    this.fetchSurveys()
    this.useSubmissionStore.fetchCodes()
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
.popover .arrow {
  display: none !important;
}
.popover {
  margin: 1em !important;
}
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
