<template>
  <div>
    <div v-if="loading">
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
    </div>
    <div v-else>
      <b-card no-body class="mb-3 container d-print-none">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
      </b-card>
      <b-card v-if="errorNotFound" class="container p-1">
        <h1>Not Found</h1>
        <p>The page you are looking for was not found.</p>
      </b-card>
      <b-card v-else class="container p-1">

        <!-- SUMMARY -->
        <fieldset id="summary_fieldset" class="detail-section mb-3">
          <legend>
            <span class="h2">Well Summary</span>
            <div class="float-right d-print-none">
              <router-link v-if="show.edit" :to="{ name: 'SubmissionsEdit', params: { id: $route.params.id } }" class="mr-3">
                <button class="btn btn-primary mb-1">Edit</button>
              </router-link>
              <b-btn variant="light" aria-label="Print" @click="handlePrint"><i class="fa fa-lg fa-print"></i></b-btn>
            </div>
          </legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Tag Number:</span> {{ well.well_tag_number }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Status:</span> {{ well.well_status }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Observation Well Number:</span>
              <a
                v-if="well.observation_well_number"
                id="obs_well_number"
                :href="`https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20${well.observation_well_number}`"
              >
                {{ well.observation_well_number }}
              </a>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ well.identification_plate_number }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Class:</span> {{ well.well_class }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Observation Well Status:</span> {{ well.observation_well_status }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Owner Name:</span> {{ well.owner_full_name }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Subclass:</span> {{ well.subclass }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Environmental Monitoring System (EMS) ID:</span> {{ well.ems || well.ems_id }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Intended Water Use:</span> {{ well.intended_water_use }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Aquifer Number:</span>
              <router-link :to="{ name: 'aquifers-view', params: { id: well.aquifer } }">
                {{ well.aquifer }}
              </router-link>
            </b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Alternative specs submitted:</span> {{ well.alternative_specs_submitted }}</b-col>
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
                <div><a class="jump_link" href="#perforations_fieldset">Liner Details</a></div>
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
            <b-col cols="12" md="4"><span class="font-weight-bold">Licensed Status:</span> {{ licence ? licence.status : '' }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Licence Number:</span> {{ licence ? licence.number : '' }}</b-col>
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
                          <td>{{ ('000000000' + well.legal_pid).slice(-9) }}</td>
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
              <div>
                <single-well-map :latitude="Number(well.latitude)" :longitude="Number(well.longitude)" :draggable="false"></single-well-map>
              </div>
              <div class="my-3">&nbsp;</div>
              <div><span class="font-weight-bold">Geographic Coordinates - North American Datum of 1983 (NAD 83)</span></div>
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
                <b-col cols="12" md="6"><span class="font-weight-bold">Location Accuracy Code:</span> {{well.location_accuracy_code}}</b-col>
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
          <b-pagination v-if="!!well.submission_work_dates.length && well.submission_work_dates.length > submissionsPerPage" size="md" :total-rows="well.submission_work_dates.length" v-model="submissionsPage" :per-page="submissionsPerPage" />
        </fieldset>

        <fieldset id="well_work_dates_fieldset" class="my-3 detail-section">
          <legend>Well Work Dates</legend>
          <b-table
            id="wellWorkDatesTable"
            ref="wellWorkDatesTable"
            striped
            bordered
            :items=well_dates
            :fields="work_date_fields"
          >
          </b-table>
        </fieldset>

        <fieldset id="well_completion_data_fieldset" class="my-3 detail-section">
          <legend>Well Completion Data</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Total Depth Drilled:</span> {{ well.total_depth_drilled }} {{ well.total_depth_drilled ? 'feet':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Static Water Level (BTOC):</span> {{ well.static_water_level }} {{ well.static_water_level ? 'feet': ''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Cap:</span> {{ well.well_cap_type }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ well.finished_well_depth }} {{ well.finished_well_depth ? 'feet':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Estimated Well Yield:</span> {{ well.well_yield }} {{ well.well_yield ? 'USGPM': ''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Well Disinfected Status:</span> {{ well.well_disinfected_status }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Final Casing Stick Up:</span> {{ well.final_casing_stick_up }} {{ well.final_casing_stick_up ? 'inches':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Flow:</span> {{ well.artesian_flow }} {{ well.artesian_flow ? 'USGPM': ''}}</b-col>
            <b-col cols="12" md="4">
              <span class="font-weight-bold">Drilling Method<span v-if="well.drilling_methods && well.drilling_methods.length > 1">s</span>:</span>
              <span v-for="(method, index) in well.drilling_methods" :key="`drillingMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Depth to Bedrock:</span> {{ well.bedrock_depth }} {{ well.bedrock_depth ? 'feet':''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Artesian Pressure:</span> {{ well.artesian_pressure }} {{ well.artesian_pressure ? 'feet': ''}}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Orientation of Well:</span> {{ well.well_orientation }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Ground elevation:</span> {{ well.ground_elevation }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ well.ground_elevation_method }}</b-col>
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
            :fields="lithology_fields"
          ></b-table>
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

              <template slot="from" slot-scope="data">{{data.item.start}}</template>
              <template slot="HEAD_from" slot-scope="data">{{ data.label }} (ft)</template>
              <template slot="to" slot-scope="data">{{data.item.end}}</template>
              <template slot="HEAD_to" slot-scope="data">{{ data.label }} (ft)</template>
              <template slot="casing_type" slot-scope="data">{{codeToDescription('casing_codes', data.item.casing_code)}}</template>
              <template slot="casing_material" slot-scope="data">{{codeToDescription('casing_materials', data.item.casing_material)}}</template>
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
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Depth:</span> {{ well.backfill_depth }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Thickness:</span> {{ well.surface_seal_thickness }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Surface Seal Depth:</span> {{ well.surface_seal_depth }}</b-col>
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
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Diameter:</span> {{ well.liner_diameter }}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner Thickness:</span> {{ well.liner_thickness }}</b-col>
              </b-row>
              <b-row>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner from:</span> {{ well.liner_from }}</b-col>
                <b-col cols="12" md="6"><span class="font-weight-bold">Liner to:</span> {{ well.liner_to }}</b-col>
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
                <template slot="from" slot-scope="data">{{data.item.start}} ft</template>
                <template slot="to" slot-scope="data">{{data.item.end}} ft</template>
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
                  :fields="['from', 'to', 'internal_diameter', 'assembly_type', 'slot_size']"
                  show-empty
                  >
                <template slot="from" slot-scope="data">{{data.item.start}} ft</template>
                <template slot="to" slot-scope="data">{{data.item.end}} ft</template>
                <template slot="assembly_type" slot-scope="data">{{codeToDescription('screen_assemblies', data.item.assembly_type)}}</template>
              </b-table>
            </b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_development_fieldset" class="my-3 detail-section">
          <legend>Well Development</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Developed by:</span> {{ codeToDescription('development_methods', well.development_method) }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Development Total Duration:</span> {{ well.development_hours }} {{ well.development_hours ? 'hours':'' }}</b-col>
          </b-row>
        </fieldset>

        <fieldset id="well_yield_fieldset" class="my-3 detail-section">
          <legend>Well Yield</legend>

          <div v-if="!well.production_data_set">No well yield data available.</div>

          <div v-for="(productionTest, index) in well.production_data_set" :key="`ProductionDataSet${index}`">
            <b-row>
              <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Method:</span> {{codeToDescription('yield_estimation_methods', productionTest.yield_estimation_method)}} </b-col>
              <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Rate:</span> {{productionTest.yield_estimation_rate}} </b-col>
              <b-col cols="12" md="4"><span class="font-weight-bold">Estimation Duration:</span> {{productionTest.yield_estimation_duration}}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" md="4"><span class="font-weight-bold">Static Water Level Before Test:</span> {{productionTest.static_level}}</b-col>
              <b-col cols="12" md="4"><span class="font-weight-bold">Drawdown:</span> {{productionTest.drawdown}}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" md="4"><span class="font-weight-bold">Hydrofracturing Performed:</span> {{productionTest.hydro_fracturing_performed}}</b-col>
              <b-col cols="12" md="4"><span class="font-weight-bold">Increase in Yield Due to Hydrofracturing:</span> {{productionTest.hydro_fracturing_yield_increase}}</b-col>
            </b-row>
          </div>
        </fieldset>

        <fieldset id="well_decommissioning_fieldset" class="my-3 detail-section">
          <legend>Well Decommission Information</legend>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Reason for Decommission:</span> {{ well.decommission_reason }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Method of Decommission:</span> {{ well.decommission_method }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" md="4"><span class="font-weight-bold">Sealant Material:</span> {{ well.sealant_material }}</b-col>
            <b-col cols="12" md="4"><span class="font-weight-bold">Backfill Material:</span> {{ well.backfill_material }}</b-col>
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
            <span class="font-weight-bold">Alternative Specs Submitted:</span> {{ well.alternative_specs_submitted === true ? "Yes" : "No" }}
          </p>
        </fieldset>

        <fieldset id="documents_fieldset" class="detail-section my-3">
          <legend>Documents</legend>
          <documents :well="$route.params.id"></documents>
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
import { mapGetters } from 'vuex'
import SingleWellMap from '@/wells/components/SingleWellMap.vue'
import Documents from '@/wells/components/Documents.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ApiService from '@/common/services/ApiService.js'
import codeToDescription from '@/common/codeToDescription.js'

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
      well: {},
      licence: {
        status: '',
        number: ''
      },
      lithology_fields: {
        lithology_from: { label: 'From (ft bgl)' },
        lithology_to: { label: 'To (ft bgl)' },
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
    well_dates () {
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
      const links = [
        {
          text: 'Well Search',
          to: { name: 'wells-home' }
        }
      ]

      if (this.errorNotFound) {
        links.push({
          text: 'Not found',
          active: true
        })
        return links
      }
      links.push({
        text: 'Well Summary',
        active: true
      })
      return links
    },
    ...mapGetters(['userRoles', 'config'])
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
      ApiService.get('wells', this.$route.params.id).then((response) => {
        this.well = response.data
      }).catch((e) => {
        this.error = e.response
      }).finally(() => {
        this.loading = false
      })
      ApiService.query(`wells/licensing?well_tag_number=${this.$route.params.id}`).then((response) => {
        this.licence = response.data
      }).catch((e) => {
        this.loadLicencingError = e.response
      })
    }
  },
  created () {
    this.fetchWellData()
  }
}
</script>

<style>
</style>
