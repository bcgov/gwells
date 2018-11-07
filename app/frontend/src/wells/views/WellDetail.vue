<template>
  <div>
    <b-card no-body class="mb-3 container container-wide">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <b-card class="container container-wide p-1">

      <!-- SUMMARY -->
      <fieldset id="summary_fieldset" class="detail-section mb-3">
        <legend>
          <span class="h2">Well Summary</span>
          <div class="float-right">
            <router-link v-if="show.edit" :to="{ name: 'SubmissionsEdit', params: { id: well.well_tag_number || 0 } }" class="hide-for-print mr-3">
              <button class="btn btn-primary mb-1">Edit</button>
            </router-link>
            <b-btn variant="light" v-if="analytics" aria-label="Print" @click="ga('send', 'event', 'Button', 'print', 'Wells Summary Print'); handlePrint;"><i class="fa fa-print"></i></b-btn>
            <b-btn variant="light" v-else aria-label="Print" @click="handlePrint"><i class="fa fa-lg fa-print"></i></b-btn>

          </div>
        </legend>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Tag Number:</span> {{ well.well_tag_number }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Status:</span> {{ well.well_status }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Observation Well Number:</span> {{ well.observation_well_number }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ well.identification_plate_number }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Class:</span> {{ well.well_class }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Observation Well Status:</span> {{ well.observation_well_status }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Owner Name:</span> {{ well.owner_full_name }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Subclass:</span> {{ well.subclass }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Environmental Monitoring System (EMS) ID:</span> {{ well.ems_id }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Licensed Status:</span> {{ well.licenced_status }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Intended Water Use:</span> {{ well.intended_water_use }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Aquifer Number:</span> {{ well.aquifer }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"></b-col>
          <b-col cols="12" lg="4"></b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Alternative specs submitted (if required):</span> {{ well.alternative_specs_submitted }}</b-col>
        </b-row>
      </fieldset>

      <!-- LINKS -->
      <fieldset id="jump_links_fieldset" class="no-print detail-section my-3">
          <legend>Sections</legend>
          <b-row>
            <b-col cols="12" lg="4">
              <div><a class="jump_link" href="#location_information_fieldset">Location Information</a></div>
              <div><a class="jump_link" href="#well_activity_fieldset">Well Activity</a></div>
              <div><a class="jump_link" href="#well_completion_data_fieldset">Well Completion Data and Artesian Flow</a></div>
              <div><a class="jump_link" href="#lithology_fieldset">Lithology</a></div>
              <div><a class="jump_link" href="#casing_fieldset">Casing Details</a></div>
            </b-col>
            <b-col cols="12" lg="4">
              <div><a class="jump_link" href="#surface_seal_fieldset">Surface Seal and Backfill Details</a></div>
              <div><a class="jump_link" href="#perforations_fieldset">Liner Details</a></div>
              <div><a class="jump_link" href="#screen_details_fieldset">Screen Details</a></div>
              <div><a class="jump_link" href="#well_development_fieldset">Well Development</a></div>
              <div><a class="jump_link" href="#well_yield_fieldset">Well Yield</a></div>
            </b-col>
            <b-col cols="12" lg="4">
              <div><a class="jump_link" href="#well_decommissioning_fieldset">Well Decommissioning</a></div>
              <div><a class="jump_link" href="#well_comments_fieldset">Comments</a></div>
              <div v-if="config && config.enable_documents"><a class="jump_link" href="#documents_fieldset">Documentation</a></div>
              <div><a class="jump_link" href="#disclaimer_fieldset">Disclaimer</a></div>
            </b-col>
          </b-row>
      </fieldset>

      <!-- LOCATION -->
      <fieldset id="location_information_fieldset" class="my-3 detail-section">
        <legend>Location Information</legend>
        <b-row>
          <b-col cols="12" lg="6" xl="5">
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
          <b-col cols="12" lg="6" xl="6" offset-xl="1">
            <div>
              <coords-map :latitude="Number(well.latitude) || 49" :longitude="Number(well.longitude) || -123" :draggable="false"></coords-map>
            </div>
            <div class="my-3">&nbsp;</div>
            <div><span class="font-weight-bold">Geographic Coordinates - North American Datum of 1983 (NAD 83)</span></div>
            <b-row>
              <b-col cols="12" lg="4"><span class="font-weight-bold">Latitude:</span> {{well.latitude}}</b-col>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Longitude:</span> {{well.longitude}}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="4"><span class="font-weight-bold">UTM Easting:</span> {{ UTM.easting ? Math.round(UTM.easting) : ''}}</b-col>
              <b-col cols="12" lg="6"><span class="font-weight-bold">UTM Northing:</span> {{ UTM.northing ? Math.round(UTM.northing) : ''}}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="4"><span class="font-weight-bold">Zone:</span> {{UTM.zone}}</b-col>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Location Accuracy Code:</span> {{well.location_accuracy_code}}</b-col>
            </b-row>
          </b-col>
        </b-row>
      </fieldset>

      <fieldset id="well_activity_fieldset" class="my-3 detail-section">
        <legend>Well Activity</legend>
        <b-table
          striped
          small
          bordered
          show-empty
          :fields="['activity_type', 'work_start_date', 'work_end_date', 'drilling_company']"
        >

        </b-table>
      </fieldset>

      <fieldset id="well_completion_data_fieldset" class="my-3 detail-section">
        <legend>Well Completion Data</legend>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Total Depth Drilled:</span> {{ well.total_depth_drilled }} {{ well.total_depth_drilled ? 'feet':''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Static Water Level (BTOC):</span> {{ well.static_water_level }} {{ well.static_water_level ? 'feet': ''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Cap:</span> {{ well.well_cap_type }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ well.finished_well_depth }} {{ well.finished_well_depth ? 'feet':''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Estimated Well Yield:</span> {{ well.well_yield }} {{ well.well_yield ? 'USGPM': ''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Well Disinfected:</span> {{ well.well_disinfected }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Final Casing Stick Up:</span> {{ well.final_casing_stick_up }} {{ well.final_casing_stick_up ? 'inches':''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Flow:</span> {{ well.artesian_flow }} {{ well.artesian_flow ? 'USGPM': ''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Drilling Method:</span> {{ well.method_of_drilling }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Depth to Bedrock:</span> {{ well.bedrock_depth }} {{ well.bedrock_depth ? 'feet':''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Pressure:</span> {{ well.artesian_pressure }} {{ well.artesian_pressure ? 'feet': ''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Orientation of Well:</span> {{ well.well_orientation }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Ground elevation:</span> {{ well.ground_elevation }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ well.ground_elevation_method }}</b-col>
        </b-row>
      </fieldset>

      <fieldset id="lithology_fieldset" class="my-3 detail-section">
        <legend>Lithology</legend>
        <b-table
          striped
          small
          bordered
          show-empty
          :fields="['from', 'to', 'description', 'relative hardness', 'colour', 'estimated_water_bearing_flow']"
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

            <template slot="from" slot-scope="data">{{data.item.start}} ft</template>
            <template slot="to" slot-scope="data">{{data.item.end}} ft</template>
            <template slot="casing_type" slot-scope="data">{{codeToDescription('casing_codes', data.item.casing_code)}}</template>
            <template slot="casing_material" slot-scope="data">{{codeToDescription('casing_materials', data.item.casing_material)}}</template>
          </b-table>
        </div>
      </fieldset>

      <fieldset id="surface_seal_fieldset" class="my-3 detail-section">
        <legend>Surface Seal and Backfill Details</legend>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Material:</span> {{ codeToDescription('surface_seal_materials', well.surface_seal_material) }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Material Above Surface Seal:</span> {{ codeToDescription('surface_seal_materials', well.backfill_above_surface_seal) }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Installation Method:</span> {{ codeToDescription('surface_seal_methods', well.surface_seal_method) }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Depth:</span> {{ well.backfill_depth }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Thickness:</span> {{ well.surface_seal_thickness }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Depth:</span> {{ well.surface_seal_depth }}</b-col>
        </b-row>
      </fieldset>

      <fieldset id="liner_details_fieldset" class="my-3 detail-section">
        <legend>Liner Details</legend>
        <b-row>
          <b-col cols="12" lg="6">
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Material:</span> {{ codeToDescription('liner_materials', well.liner_material) }}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Diameter:</span> {{ well.liner_diameter }}</b-col>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Thickness:</span> {{ well.liner_thickness }}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Liner from:</span> {{ well.liner_from }}</b-col>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Liner to:</span> {{ well.liner_to }}</b-col>
            </b-row>
          </b-col>
          <b-col cols="12" lg="6">
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
          <b-col cols="12" lg="4">
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', well.screen_intake_method) }}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Type:</span> {{ codeToDescription('screen_types', well.screen_type) }}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Material:</span> {{ codeToDescription('screen_materials', well.screen_material) }}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Opening:</span> {{ codeToDescription('screen_openings', well.screen_opening) }}</b-col>
            </b-row>
            <b-row>
              <b-col cols="12" lg="6"><span class="font-weight-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', well.screen_bottom) }}</b-col>
            </b-row>
          </b-col>
          <b-col cols="12" lg="8">
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
          <b-col cols="12" lg="4"><span class="font-weight-bold">Developed by:</span> {{ codeToDescription('development_methods', well.development_method) }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Development Total Duration:</span> {{ well.development_hours }} {{ well.development_hours ? 'hours':'' }}</b-col>
        </b-row>
      </fieldset>

      <fieldset id="well_yield_fieldset" class="my-3 detail-section">
        <legend>Well Yield</legend>

        <div v-if="!well.production_data_set">No well yield data available.</div>

        <div v-for="(productionTest, index) in well.production_data_set" :key="`ProductionDataSet${index}`">
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Method:</span> {{codeToDescription('yield_estimation_methods', productionTest.yield_estimation_method)}} </b-col>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Rate:</span> {{productionTest.yield_estimation_rate}} </b-col>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Duration:</span> {{productionTest.yield_estimation_duration}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Static Water Level Before Test:</span> {{productionTest.static_level}}</b-col>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Drawdown:</span> {{productionTest.drawdown}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Hydrofracturing Performed:</span> {{productionTest.hydro_fracturing_performed}}</b-col>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Increase in Yield Due to Hydrofracturing:</span> {{productionTest.hydro_fracturing_yield_increase}}</b-col>
          </b-row>
        </div>
      </fieldset>

      <fieldset id="well_decommissioning_fieldset" class="my-3 detail-section">
        <legend>Well Decommission Information</legend>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ well.finished_well_depth }} {{ well.finished_well_depth ? 'feet':''}}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Sealant Material:</span> {{ well.sealant_material }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Reason for Decommission:</span> {{ well.decommission_reason }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Material:</span> {{ well.backfill_material }}</b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Method of Decommission:</span> {{ well.decommission_method }}</b-col>
          <b-col cols="12" lg="4"><span class="font-weight-bold">Decommission Details:</span> {{ well.decommission_details }}</b-col>
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
</template>

<script>
import { mapGetters } from 'vuex'
import CoordsMap from '@/submissions/components/SubmissionForm/CoordsMap.vue'
import Documents from '@/wells/components/Documents.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ApiService from '@/common/services/ApiService.js'
import codeToDescription from '@/common/codeToDescription.js'

export default {
  name: 'WellDetail',
  components: {
    CoordsMap,
    Documents
  },
  mixins: [
    convertCoordinatesMixin, codeToDescription
  ],
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Well Search',
          to: { name: 'wells-home' }
        },
        {
          text: 'Well Summary',
          active: true
        }
      ],
      well: {}
    }
  },
  computed: {
    analytics () {
      return !!window.ga
    },
    show () {
      return {
        edit: (!!this.config && this.config.enable_data_entry === true) && this.userRoles.submissions.edit === true
      }
    },
    UTM () {
    // converts form lat/long and returns an object containing UTM easting, northing, and zone
      // if (this.well && this.well.latitude && this.well.longitude) {
      //   return this.convertToUTM(Number(this.well.longitude), Number(this.well.latitude))
      // }
      return {}
    },
    ...mapGetters(['userRoles', 'config'])
  },
  methods: {
    handlePrint () {
      window.print()
    },
    fetchWellData () {
      ApiService.get('wells', this.$route.params.id).then((response) => {
        this.well = response.data
      }).catch((e) => {
        this.loadWellError = e.response
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
