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
  <div>
    <h1 class="card-title">
      <b-row>
        <b-col cols="12">
          <div>Well Activity Submission<span v-if="!reportSubmitted"> Preview</span></div>
          <b-btn v-if="reportSubmitted" @click="$emit('startNewReport')" variant="primary">Submit New Report</b-btn>
          <b-btn v-else class="float-right" @click="$emit('back')" variant="primary">Back to Edit</b-btn>
        </b-col>
      </b-row>
    </h1>
    <fieldset class="my-3 detail-section">
      <legend>Type of Work and Well Class</legend>
      <b-row>
        <b-col>
          <span class="font-weight-bold">Report Type:</span> {{ codeToDescription('activity_types', activity) }}
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Class of Well:</span> {{ codeToDescription('well_classes', form.well_class) }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Subclass:</span> {{ wellSubclass }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Intended Water Use:</span> {{ codeToDescription('intended_water_uses', form.intended_water_use) }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4" id="wellTagNumberDisplay">
          <span class="font-weight-bold">Well Tag Number: </span>
          <router-link :to="{ name: 'SubmissionsEdit', params: { id: form.well }}" v-if="reportSubmitted && canEditWells">
            {{ form.well }}
          </router-link>
          <span v-else>{{ form.well }}</span>
        </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ form.identification_plate_number }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Where Plate Attached:</span> {{ form.well_identification_plate_attached }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Work Start Date:</span> {{ form.work_start_date }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Work End Date:</span> {{ form.work_end_date }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Person Responsible for Work</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Person Responsible for Work:</span> {{ form.person_responsible ? form.person_responsible['name'] : '' }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Person Who Performed Work:</span> {{ form.driller_name }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Company of Person Responsible for Work:</span> {{ form.company_of_person_responsible ? form.company_of_person_responsible['org_verbose_name'] : '' }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Consultant Name:</span> {{ form.consultant_name }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Consultant Company:</span> {{ form.consultant_company }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Well Owner</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Name:</span> {{ form.owner_full_name }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="3"><span class="font-weight-bold">Mailing address:</span> {{ form.owner_mailing_address }}</b-col>
        <b-col cols="12" lg="3"><span class="font-weight-bold">City:</span> {{ form.owner_city }}</b-col>
        <b-col cols="12" lg="3"><span class="font-weight-bold">Province:</span> {{ form.owner_province_state }}</b-col>
        <b-col cols="12" lg="3"><span class="font-weight-bold">Postal Code:</span> {{ form.owner_postal_code }}</b-col>

      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Location Information</legend>
      <b-row>
        <b-col cols="12" lg="6" xl="4">
          <b-row>
            <b-col><span class="font-weight-bold">Street Address:</span> {{ form.street_address }}</b-col>
          </b-row>
          <b-row>
            <b-col><span class="font-weight-bold">Town/City:</span> {{ form.city }}</b-col>
          </b-row>
          <b-row>
            <b-col>
              <div class="my-3"><span class="font-weight-bold">Legal Description:</span></div>
              <div class="table-responsive">
                <table class="table table-sm table-striped table-bordered">
                  <tbody>
                    <tr>
                      <th class="w-50">Lot</th>
                      <td>{{ form.legal_lot }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Plan</th>
                      <td>{{ form.legal_plan }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">District Lot</th>
                      <td>{{ form.legal_district_lot }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Block</th>
                      <td>{{ form.legal_block }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Section</th>
                      <td>{{ form.legal_section }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Township</th>
                      <td>{{ form.legal_township }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Range</th>
                      <td>{{ form.legal_range }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Land District</th>
                      <td>{{ form.land_district }}</td>
                    </tr>
                    <tr>
                      <th class="w-50">Property Identification Description (PID)</th>
                      <td>{{ form.legal_pid }}</td>
                    </tr>
                  </tbody>
                </table>
                <div>
                  <span class="font-weight-bold">Description of Well Location:</span> {{ form.well_location_description }}
                </div>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="12" lg="6" xl="6" offset-xl="2">
          <div>
            <coords-map :latitude="form.latitude" :longitude="form.longitude" :draggable="false" :drinking_water="form.drinking_water_protection_area_ind"/>
          </div>
          <div class="my-3">&nbsp;</div>
          <div><span class="font-weight-bold">Geographic Coordinates - North American Datum of 1983 (NAD 83)</span></div>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Latitude:</span> {{form.latitude}}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Longitude:</span> {{form.longitude}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">UTM Easting:</span> {{UTM.easting}}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">UTM Northing:</span> {{UTM.northing}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Zone:</span> {{UTM.zone}}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Location Accuracy Code:</span> {{form.location_accuracy_code}}</b-col>
          </b-row>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Method of Drilling</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Ground elevation:</span> {{ form.ground_elevation }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ codeToDescription('ground_elevation_methods', form.ground_elevation_method) }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Drilling methods:</span> <div v-for="(item, index) in form.drilling_methods" :key="index">{{ codeToDescription('drilling_methods', item) }}</div></b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Orientation of well:</span> {{ form.well_orientation_status }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.lithology">
      <legend>Lithology</legend>
      <div class="table-responsive">
        <b-table
          striped
          small
          bordered
          :items="filterBlankRows(form.lithologydescription_set)"
          show-empty
          :fields="[
            'from',
            'to',
            'description',
            'colour',
            'hardness',
            'moisture',
            'descriptor',
            'water_bearing_estimated_flow',
            'observations'
          ]">
          <template v-slot:cell(description)="data">{{data.item.lithology_raw_data}}</template>
          <template v-slot:cell(from)="data">{{data.item.start}}</template>
          <template v-slot:cell(to)="data">{{data.item.end}}</template>
          <template v-slot:cell(colour)="data">{{codeToDescription('lithology_colours', data.item.lithology_colour) }}</template>
          <template v-slot:cell(hardness)="data">{{codeToDescription('lithology_hardness_codes', data.item.lithology_hardness) }}</template>
          <template v-slot:cell(moisture)="data">{{codeToDescription('lithology_moisture_codes', data.item.lithology_moisture) }}</template>
          <template v-slot:cell(descriptor)="data">{{codeToDescription('lithology_descriptors', data.item.lithology_description) }}</template>
          <template v-slot:cell(observations)="data">{{ data.item.lithology_observation }}</template>
        </b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.closureDescription">
      <legend>Decommission Description</legend>
      <div class="table-responsive">
        <b-table
          striped
          small
          bordered
          :items="filterBlankRows(form.decommission_description_set)"
          :fields="['start', 'end', 'material', 'observations']"
          show-empty
        >
          <template v-slot:cell(start)="data">{{data.item.start}} ft</template>
          <template v-slot:cell(end)="data">{{data.item.end}} ft</template>
          <template v-slot:cell(material)="data">{{codeToDescription('decommission_materials', data.item.material)}}</template>
          <template v-slot:cell(observations)="data">{{codeToDescription('decommission_materials', data.item.observations)}}</template>
        </b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Casing Details</legend>
      <div class="table-responsive">
        <b-table
            striped
            small
            bordered
            :items="filterBlankRows(form.casing_set)"
            :fields="['from', 'to', 'casing_type', 'casing_material', 'diameter', 'wall_thickness', 'drive_shoe_status']"
            show-empty>

          <template v-slot:cell(from)="data">{{data.item.start}}{{data.item.start ? ' ft' : '' }}</template>
          <template v-slot:cell(to)="data">{{data.item.end}}{{data.item.end ? ' ft' : '' }}</template>
          <template v-slot:cell(casing_type)="data">{{codeToDescription('casing_codes', data.item.casing_code)}}</template>
          <template v-slot:cell(casing_material)="data">{{codeToDescription('casing_materials', data.item.casing_material)}}</template>
          <template v-slot:cell(drive_shoe_status)="data">{{codeToDescription('drive_shoe_status', data.item.drive_shoe_status)}}</template>

        </b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.backfill">
      <legend>Surface Seal and Backfill Details</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Material:</span> {{ codeToDescription('surface_seal_materials', form.surface_seal_material) }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Material Above Surface Seal:</span> {{ codeToDescription('surface_seal_materials', form.backfill_type) }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Installation Method:</span> {{ codeToDescription('surface_seal_methods', form.surface_seal_method) }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Depth:</span> {{ form.backfill_depth }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Thickness:</span> {{ form.surface_seal_thickness }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Depth:</span> {{ form.surface_seal_depth }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.liner">
      <legend>Liner Details</legend>
      <b-row>
        <b-col cols="12" lg="6">
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Material:</span> {{ codeToDescription('liner_materials', form.liner_material) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Diameter:</span> {{ form.liner_diameter }}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Thickness:</span> {{ form.liner_thickness }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Liner from:</span> {{ form.liner_from }}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Liner to:</span> {{ form.liner_to }}</b-col>
          </b-row>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="font-weight-bold">Liner perforations</div>
          <b-table
              striped
              small
              bordered
              :items="filterBlankRows(form.linerperforation_set)"
              :fields="['from', 'to']"
              show-empty
          >
            <template v-slot:cell(from)="data">{{data.item.start}} ft</template>
            <template v-slot:cell(to)="data" >{{data.item.end}} ft</template>
          </b-table>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.screens">
      <legend>Screen Details</legend>
      <b-row>
        <b-col cols="12" lg="4">
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', form.screen_intake_method) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Type:</span> {{ codeToDescription('screen_types', form.screen_type) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Material:</span> {{ codeToDescription('screen_materials', form.screen_material) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Opening:</span> {{ codeToDescription('screen_openings', form.screen_opening) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', form.screen_bottom) }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Other Material:</span> {{form.other_screen_material}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Information:</span> {{form.screen_information}}</b-col>
          </b-row>
        </b-col>
        <b-col cols="12" lg="8">
          <div class="font-weight-bold">Installed Screens</div>
          <b-table
              striped
              small
              bordered
              :items="filterBlankRows(form.screen_set)"
              :fields="['from', 'to', 'diameter', 'assembly_type', 'slot_size']"
              show-empty
              >
            <template v-slot:cell(from)="data">{{data.item.start}} ft</template>
            <template v-slot:cell(to)="data">{{data.item.end}} ft</template>
            <template v-slot:cell(assembly_type)="data">{{codeToDescription('screen_assemblies', data.item.assembly_type)}}</template>
          </b-table>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.filterPack">
      <legend>Filter Pack</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack from:</span> {{ form.filter_pack_from }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack to:</span> {{ form.filter_pack_to }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack thickness:</span> {{ form.filter_pack_thickness }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack material:</span> {{ codeToDescription('filter_pack_material', form.filter_pack_material) }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack material size:</span> {{ form.filter_pack_material_size }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.wellDevelopment">
      <legend>Well Development</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Developed by:</span> <div v-for="(item, index) in form.development_methods" :key="index"> {{ codeToDescription('development_methods', item) }}</div></b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Development Total Duration:</span> {{ form.development_hours }} {{ form.development_hours ? 'hours':'' }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Development Notes:</span> {{ form.development_notes }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.wellYield">
      <legend>Well Yield</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Method:</span> {{codeToDescription('yield_estimation_methods', form.yield_estimation_method)}} </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Rate:</span> {{form.yield_estimation_rate}} </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Duration:</span> {{form.yield_estimation_duration}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Static Water Level Before Test:</span> {{form.static_level_before_test}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Drawdown:</span> {{form.drawdown}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Hydrofracturing Performed:</span> {{form.hydro_fracturing_performed | nullBooleanToYesNo}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Increase in Yield Due to Hydrofracturing:</span> {{form.hydro_fracturing_yield_increase}}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.waterQuality">
      <legend>Water Quality</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Characteristics:</span>
          <span v-for="(item, index) in form.water_quality_characteristics" :key="`previewWaterCharacteristic${index}`">
            <!-- Add a comma before each item except index 0 -->
            {{ index ? ', ': ''}}{{ codeToDescription('water_quality_characteristics', item) }}
          </span>
        </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Water Quality Colour:</span> {{ codeToDescription('water_quality_colours', form.water_quality_colour) }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6"><span class="font-weight-bold">Water Quality Odour:</span> {{ form.water_quality_odour }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6"><span class="font-weight-bold">EMS ID:</span> {{ form.ems }}</b-col>
      </b-row>
    </fieldset>
    <fieldset class="my-3 detail-section" v-if="sections.wellCompletion">
      <legend>Well Completion Data</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Total Depth Drilled:</span> {{ form.total_depth_drilled }} {{ form.total_depth_drilled ? 'ft bgl':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Static Water Level (BTOC):</span> {{ form.static_water_level }} {{ form.static_water_level ? 'feet': ''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Pressure (head):</span> {{ form.artesian_pressure_head }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ form.finished_well_depth }} {{ form.finished_well_depth ? 'feet':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimated Well Yield:</span> {{ form.well_yield }} {{ form.well_yield ? 'USGPM': ''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Pressure (PSI):</span> {{ form.artesian_pressure }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Final Casing Stick Up:</span> {{ form.final_casing_stick_up }} {{ form.final_casing_stick_up ? 'inches':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Condition:</span> {{ form.artesian_conditions | nullBooleanToYesNo }} </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Cap:</span> {{ form.well_cap_type }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Depth to Bedrock:</span> {{ form.bedrock_depth }} {{ form.bedrock_depth ? 'feet':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Flow:</span> {{ form.artesian_flow }} {{ form.artesian_flow ? 'USGPM': ''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Disinfected:</span> {{ form.well_disinfected_status }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.decommissionInformation">
      <legend>Well Decommission Information</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Reason for Decommission:</span> {{ form.decommission_reason }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Method of Decommission:</span> {{ form.decommission_method }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Sealant Material:</span> {{ form.decommission_sealant_material }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Material:</span> {{ form.decommission_backfill_material }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Decommission Details:</span> {{ form.decommission_details }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Pumping Test Information and Aquifer Parameters</legend>
      <div class="table-responsive">
        <b-table
            striped
            small
            bordered
            :items="filterBlankRows(form.aquifer_parameters_set)"
            :fields="[
                  'start_date_pumping_test',
                  'pumping_test_description',
                  { key: 'test_duration', label: 'Test Duration (min)' },
                  'boundary_effect',
                  'storativity',
                  { key: 'transmissivity', label: 'Transmissivity (m²/day)' },
                  { key: 'hydraulic_conductivity', label: 'Hydraulic Conductivity (m/day)' },
                  'specific_yield',
                  { key: 'specific_capacity', label: 'Specific Capacity (L/s/m)' },
                  'analysis_method',
                  'comments'
                ]"
            show-empty>
            <template v-slot:cell(pumping_test_description)="data">{{codeToDescription('pumping_test_description_codes', data.item.pumping_test_description)}}</template>
            <template v-slot:cell(boundary_effect)="data">{{codeToDescription('boundary_effect_codes', data.item.boundary_effect)}}</template>
            <template v-slot:cell(analysis_method)="data">{{codeToDescription('analysis_method_codes', data.item.analysis_method)}}</template>
        </b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Comments</legend>
      <p>
        {{ form.comments ? form.comments : 'No comments submitted' }}
      </p>
      <p>
        <span class="font-weight-bold">Alternative Specs Submitted:</span> {{ form.alternative_specs_submitted | nullBooleanToYesNo }}
      </p>
      <p>
        <span class="font-weight-bold">Technical Report:</span> {{ form.technical_report | nullBooleanToYesNo }}
      </p>
      <p>
        <span class="font-weight-bold">Drinking Water Area Indicator:</span> {{ form.drinking_water_protection_area_ind | nullBooleanToYesNo }}
      </p>
    </fieldset>

    <fieldset v-if="upload_files && upload_files.length > 0">
      <legend>Documents to Upload</legend>
      <b-row>
        <b-col cols="12" lg="8">
          <b-list-group>
            <b-list-group-item v-for="(f, index) in upload_files" :key="index">
              {{f.file ? f.file.name.replace('null', '{ASSIGNED_WELL_ID}') : f.name}}
              <a
                class="fa fa-trash fa-lg"
                variant="primary"
                style="margin-left: 0.5em"
                href="#"
                @click="handleDelete(index)"
              ></a>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset v-if="uploadedFiles && uploadedFiles.public && uploadedFiles.public.length > 0 && reportSubmitted">
      <legend>Uploaded Documents</legend>
      <b-row>
        <b-col cols="12" lg="4">
          <b-list-group>
            <b-list-group-item v-for="(f, index) in uploadedFiles.public" :key="index">{{f.name}}</b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset v-if="uploadedFiles && uploadedFiles.private && uploadedFiles.private.length > 0 && reportSubmitted">
      <legend>Uploaded Internal Documentation</legend>
      <b-row>
        <b-col cols="12" lg="4">
          <b-list-group>
            <b-list-group-item v-for="(f, index) in uploadedFiles.private" :key="index">{{f.name}}</b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>General Disclaimer</legend>
      <b-row>
        <b-col cols="12" lg="9">
          This information is collected by the Ministry of Water, Land and Resource Stewardship under section 26 (c)
          of the Freedom of Information and Protection of Privacy Act and section 117 (1) of the
          Water Sustainability Act (WSA).
          <br><br>
          The groundwater information (e.g. any notes and comments that are included in well reports
          filed under WSA and its regulations) will be made available to the public by the government
          in accordance with the Open Government License-British Columba (OGL-BC) which grants the
          public a worldwide, royalty-free, perpetual, non-exclusive license to make use of the reports,
          including for commercial purposes, but subject to the terms described in the OGL-BC:
          <a href="https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc" target="_blank" rel="noopener noreferrer">
            https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc.
          </a>
          <br><br>
          Information, including personal information, will be used to determine well location and confirm
          that the construction, alteration, or decommission of a well has been done in accordance with the
          WSA and Groundwater Protection Regulation (GWPR). Well reports submitted to the Comptroller, or
          retained by the person responsible, as required under section 57 of the WSA and Part 10 of the GWPR,
          shall be considered part of the Provincial Government records. Documents or images included as part
          of submission and that contain personal information not covered under this legislation will be deleted.
          <br><br>
          Should you have any questions about the collection or use of this information, please contact the
          Groundwater Data Specialist, email: <a href = "mailto: groundwater@gov.bc.ca">groundwater@gov.bc.ca.</a>
        </b-col>
      </b-row>
    </fieldset>

    <!-- Back / Next / Submit controls -->
    <b-row v-if="!reportSubmitted" class="mt-5">
      <b-col>
        <b-btn @click="$emit('back')" variant="primary">Back to Edit</b-btn>
      </b-col>
      <b-col class="pr-4 text-right">
        <b-btn id="formSubmitButton" type="submit" variant="primary" ref="activitySubmitBtn" :disabled="formSubmitLoading">Submit</b-btn>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import CoordsMap from '@/submissions/components/SubmissionForm/CoordsMap.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import filterBlankRows from '@/common/filterBlankRows'
import codeToDescription from '@/common/codeToDescription.js'

export default {
  name: 'SubmissionPreview',
  components: {
    CoordsMap
  },
  mixins: [filterBlankRows, codeToDescription, convertCoordinatesMixin],
  props: [
    'form',
    'activity',
    'sections',
    'reportSubmitted',
    'formSubmitLoading',
    'uploadedFiles'
  ],
  data () {
    return {
    }
  },
  methods: {
    fetchFiles () {
      this.$emit('fetchFiles')
    },
    handleDelete (index) {
      this.upload_files.splice(index, 1);
    },
  },
  created () {
    this.fetchFiles()
  },
  computed: {
    ...mapGetters(['codes', 'userRoles']),
    ...mapState('documentState', [
      'upload_files'
    ]),
    canEditWells () {
      return this.userRoles.wells.edit
    },
    wellSubclass () {
      let subclassCodes = []
      let subclass = null

      // generate a list of subclasses
      if (this.form.well_subclass && this.form.well_class) {
        this.codes.well_classes.forEach((item) => {
          if (item.wellsubclasscode_set) {
            subclassCodes = subclassCodes.concat(item.wellsubclasscode_set)
          }
        })

        // find the subclass to get its description
        subclass = subclassCodes.find((code) => {
          return code.well_subclass_guid === this.form.well_subclass
        })['description']
      }

      return subclass
    },
    UTM () {
    // converts form lat/long and returns an object containing UTM easting, northing, and zone
      if (this.form.latitude || this.form.longitude) {
        let utm = this.convertToUTM(Number(this.form.longitude), Number(this.form.latitude))
        utm.easting = Math.round(utm.easting)
        utm.northing = Math.round(utm.northing)
        return utm
      } else {
        return {
          easting: null,
          northing: null,
          zone: null
        }
      }
    }
  }
}
</script>

<style>

</style>
