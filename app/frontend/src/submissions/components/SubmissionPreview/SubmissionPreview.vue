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
      <div class="flex">
        <div>
          <div>Well Activity Submission<span v-if="!reportSubmitted"> Preview</span></div>
          <Button v-if="reportSubmitted" label="Submit New Report" @click="$emit('startNewReport')"/>
          <Button v-else label="Back to Edit" class="float-right" @click="$emit('back')"/>
        </div>
      </div>
    </h1>
    <fieldset class="my-4 detail-section">
      <legend>Type of Work and Well Class</legend>
      <div class="flex">
        <div>
          <span class="font-weight-bold">Report Type:</span> {{ codeToDescription('activity_types', activity) }}
        </div>
      </div>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Class of Well:</b> {{ codeToDescription('well_classes', form.well_class) }}</span>
        <span><b>Subclass:</b> {{ wellSubclass }}</span>
        <span><b>Intended Water Use:</b> {{ codeToDescription('intended_water_uses', form.intended_water_use) }}</span>
        <span>
          <b>Well Tag Number: </b>
          <router-link :to="{ name: 'SubmissionsEdit', params: { id: form.well }}" v-if="reportSubmitted && canEditWells">
            {{ form.well }}
          </router-link>
          <span v-else>{{ form.well }}</span>
        </span>
        <span><b>Well Identification Plate Number:</b> {{ form.identification_plate_number }}</span>
        <span><b>Where Plate Attached:</b> {{ form.well_identification_plate_attached }}</span>
        <span><b>Work Start Date:</b> {{ form.work_start_date }}</span>
        <span><b>Work End Date:</b> {{ form.work_end_date }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Person Responsible for Work</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Person Responsible for Work:</b> {{ form.person_responsible ? form.person_responsible['name'] : '' }}</span>
        <span><b>Person Who Performed Work:</b> {{ form.driller_name }}</span>
        <span><b>Company of Person Responsible for Work:</b> {{ form.company_of_person_responsible ? form.company_of_person_responsible['org_verbose_name'] : '' }}</span>
        <span><b>Consultant Name:</b> {{ form.consultant_name }}</span>
        <span><b>Consultant Company:</b> {{ form.consultant_company }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Well Owner</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Name:</b> {{ form.owner_full_name }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="3">
        <span><b>Mailing address:</b> {{ form.owner_mailing_address }}</span>
        <span><b>City:</b> {{ form.owner_city }}</span>
        <span><b>Province:</b> {{ form.owner_province_state }}</span>
        <span><b>Postal Code:</b> {{ form.owner_postal_code }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Location Information</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-6 xl:col-span-4">
          <div><span><b>Street Address:</b> {{ form.street_address }}</span></div>
          <div><span><b>Town/City:</b> {{ form.city }}</span></div>
          <div>
            <div>
              <div class="my-4"><span class="font-weight-bold">Legal Description:</span></div>
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
            </div>
          </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-6 xl:col-start-3">
          <div>
            <coords-map :latitude="form.latitude" :longitude="form.longitude" :draggable="false" :drinking_water="form.drinking_water_protection_area_ind"/>
          </div>
          <div class="my-4">&nbsp;</div>
          <div><span class="font-weight-bold">Geographic Coordinates - North American Datum of 1983 (NAD 83)</span></div>
          <!-- I think this table scheme should work, even though each row will have 10/12 columns filled, bc the 4 will overflow -->
          <responsive-grid :cols="12" :lg="[4, 6, 4, 6, 4, 6]">
            <span><b>Latitude:</b> {{form.latitude}}</span>
            <span><b>Longitude:</b> {{form.longitude}}</span>
            <span><b>UTM Easting:</b> {{UTM.easting}}</span>
            <span><b>UTM Northing:</b> {{UTM.northing}}</span>
            <span><b>Zone:</b> {{UTM.zone}}</span>
            <span><b>Location Accuracy Code:</b> {{form.location_accuracy_code}}</span>
          </responsive-grid>
        </div>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Method of Drilling</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Ground elevation:</b> {{ form.ground_elevation }}</span>
        <span><b>Method of determining elevation:</b> {{ codeToDescription('ground_elevation_methods', form.ground_elevation_method) }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Drilling methods:</b> <span v-for="(item, index) in form.drilling_methods" :key="index">{{ codeToDescription('drilling_methods', item) }}</span></span>
        <span><b>Orientation of well:</b> {{ form.well_orientation_status }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.lithology">
      <legend>Lithology</legend>
      <div class="table-responsive">
        <DataTable stripedRows size="small" showGridlines :value="filterBlankRows(form.lithologydescription_set)">
          <Column field="start" header="From"/>
          <Column field="end" header="To"/>
          <Column field="lithology_raw_data" header="Description"/>
          <Column field="lithology_colour" header="Colour">
            <template #body="slotProps">{{ codeToDescription('lithology_colours', slotProps.data.lithology_colour) }}</template>
          </Column>
          <Column field="lithology_hardness" header="Hardness">
            <template #body="slotProps">{{ codeToDescription('lithology_hardness_codes', slotProps.data.lithology_hardness) }}</template>
          </Column>
          <Column field="lithology_moisture" header="Moisture">
            <template #body="slotProps">{{ codeToDescription('lithology_moisture_codes', slotProps.data.lithology_moisture) }}</template>
          </Column>
          <Column field="lithology_description" header="Descriptor">
            <template #body="slotProps">{{ codeToDescription('lithology_descriptors', slotProps.data.lithology_description) }}</template>
          </Column>
          <Column field="water_bearing_estimated_flow"/>
          <Column field="lithology_observation" header="Observations"/>
        </DataTable>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.closureDescription">
      <legend>Decommission Description</legend>
      <div class="table-responsive">
        <DataTable stripedRows size="small" showGridlines :value="filterBlankRows(form.decommission_description_set)">
          <Column field="start"/>
          <Column field="end"/>
          <Column field="material">
            <template #body="slotProps">{{ codeToDescription('decommission_materials', slotProps.data.material) }}</template>
          </Column>
          <Column field="observations">
            <template #body="slotProps">{{ codeToDescription('decommission_materials', slotProps.data.observations) }}</template>
          </Column>
        </DataTable>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Casing Details</legend>
      <div class="table-responsive">
        <DataTable stripedRows size="small" showGridlines :value="filterBlankRows(form.casing_set)">
          <Column field="start" header="From">
            <template #body="slotProps">{{slotProps.data.start}}{{slotProps.data.start ? ' ft' : '' }}</template>
          </Column>
          <Column field="end" header="To">
            <template #body="slotProps">{{slotProps.data.end}}{{slotProps.data.end ? ' ft' : '' }}</template>
          </Column>
          <Column field="casing_code" header="Casing Type">
            <template #body="slotProps">{{codeToDescription('casing_codes', slotProps.data.casing_code)}}</template>
          </Column>
          <Column field="casing_material">
            <template #body="slotProps">{{codeToDescription('casing_materials', slotProps.data.casing_material)}}</template>
          </Column>
          <Column field="diameter"/>
          <Column field="wall_thickness"/>
          <Column field="drive_shoe_status">
            <template #body="slotProps">{{codeToDescription('drive_shoe_status', slotProps.data.drive_shoe_status)}}</template>
          </Column>
        </DataTable>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.backfill">
      <legend>Surface Seal and Backfill Details</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Surface Seal Material:</b> {{ codeToDescription('surface_seal_materials', form.surface_seal_material) }}</span>
        <span><b>Backfill Material Above Surface Seal:</b> {{ codeToDescription('surface_seal_materials', form.backfill_type) }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Surface Seal Installation Method:</b> {{ codeToDescription('surface_seal_methods', form.surface_seal_method) }}</span>
        <span><b>Backfill Depth:</b> {{ form.backfill_depth }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Surface Seal Thickness:</b> {{ form.surface_seal_thickness }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Surface Seal Depth:</b> {{ form.surface_seal_depth }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.liner">
      <legend>Liner Details</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-6">
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Liner Material:</span> {{ codeToDescription('liner_materials', form.liner_material) }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Liner Diameter:</span> {{ form.liner_diameter }}</div>
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Liner Thickness:</span> {{ form.liner_thickness }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Liner from:</span> {{ form.liner_from }}</div>
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Liner to:</span> {{ form.liner_to }}</div>
          </div>
        </div>
        <div class="col-span-12 lg:col-span-6">
          <div class="font-weight-bold">Liner perforations</div>
          <DataTable stripedRows size="small" showGridlines :value="filterBlankRows(form.linerperforation_set)">
            <Column field="start" header="From">
              <template #body="slotProps">{{slotProps.data.start}} ft</template>
            </Column>
            <Column field="end" header="To">
              <template #body="slotProps">{{slotProps.data.end}} ft</template>
            </Column>
          </DataTable>
        </div>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.screens">
      <legend>Screen Details</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-4">
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', form.screen_intake_method) }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Type:</span> {{ codeToDescription('screen_types', form.screen_type) }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Material:</span> {{ codeToDescription('screen_materials', form.screen_material) }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Opening:</span> {{ codeToDescription('screen_openings', form.screen_opening) }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', form.screen_bottom) }}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Other Material:</span> {{form.other_screen_material}}</div>
          </div>
          <div class="grid grid-cols-12">
            <div class="col-span-12 lg:col-span-6"><span class="font-weight-bold">Information:</span> {{form.screen_information}}</div>
          </div>
        </div>
        <div class="col-span-12 lg:col-span-8">
          <div class="font-weight-bold">Installed Screens</div>
          <DataTable stripedRows size="small" showGridlines :value="filterBlankRows(form.screen_set)">
            <Column field="start" header="From">
              <template #body="slotProps">{{slotProps.data.start}} ft</template>
            </Column>
            <Column field="end" header="To">
              <template #body="slotProps">{{slotProps.data.end}} ft</template>
            </Column>
            <Column field="diameter"/>
            <Column field="assembly_type">
              <template #body="slotProps">{{codeToDescription('screen_assemblies', slotProps.data.assembly_type)}}</template>
            </Column>
            <Column field="slot_size"/>
          </DataTable>
        </div>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.filterPack">
      <legend>Filter Pack</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Filter pack from:</b> {{ form.filter_pack_from }}</span>
        <span><b>Filter pack to:</b> {{ form.filter_pack_to }}</span>
        <span><b>Filter pack thickness:</b> {{ form.filter_pack_thickness }}</span>
        <span><b>Filter pack material:</b> {{ codeToDescription('filter_pack_material', form.filter_pack_material) }}</span>
        <span><b>Filter pack material size:</b> {{ form.filter_pack_material_size }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.wellDevelopment">
      <legend>Well Development</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Developed by:</b> <span v-for="(item, index) in form.development_methods" :key="index"> {{ codeToDescription('development_methods', item) }}</span></span>
        <span><b>Development Total Duration:</b> {{ form.development_hours }} {{ form.development_hours ? 'hours':'' }}</span>
        <span><b>Development Notes:</b> {{ form.development_notes }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.wellYield">
      <legend>Well Yield</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Estimation Method:</b> {{codeToDescription('yield_estimation_methods', form.yield_estimation_method)}} </span>
        <span><b>Estimation Rate:</b> {{form.yield_estimation_rate}} </span>
        <span><b>Estimation Duration:</b> {{form.yield_estimation_duration}}</span>
        <span><b>Static Water Level Before Test:</b> {{form.static_level_before_test}}</span>
        <span><b>Drawdown:</b> {{form.drawdown}}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Hydrofracturing Performed:</b> {{ nullBooleanToYesNo(form.hydro_fracturing_performed) }}</span>
        <span><b>Increase in Yield Due to Hydrofracturing:</b> {{form.hydro_fracturing_yield_increase}}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.waterQuality">
      <legend>Water Quality</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Characteristics:</b>
          <span v-for="(item, index) in form.water_quality_characteristics" :key="`previewWaterCharacteristic${index}`">
            <!-- Add a comma before each item except index 0 -->
            {{ index ? ', ': ''}}{{ codeToDescription('water_quality_characteristics', item) }}
          </span>
        </span>
        <span><b>Water Quality Colour:</b> {{ codeToDescription('water_quality_colours', form.water_quality_colour) }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="6">
        <span><b>Water Quality Odour:</b> {{ form.water_quality_odour }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="6">
        <span><b>EMS ID:</b> {{ form.ems }}</span>
      </responsive-grid>
    </fieldset>
    <fieldset class="my-4 detail-section" v-if="sections.wellCompletion">
      <legend>Well Completion Data</legend>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Total Depth Drilled:</b> {{ form.total_depth_drilled }} {{ form.total_depth_drilled ? 'ft bgl':''}}</span>
        <span><b>Static Water Level (BTOC):</b> {{ form.static_water_level }} {{ form.static_water_level ? 'feet': ''}}</span>
        <span><b>Artesian Pressure (head):</b> {{ form.artesian_pressure_head }}</span>
        <span><b>Finished Well Depth:</b> {{ form.finished_well_depth }} {{ form.finished_well_depth ? 'feet':''}}</span>
        <span><b>Estimated Well Yield:</b> {{ form.well_yield }} {{ form.well_yield ? 'USGPM': ''}}</span>
        <span><b>Artesian Pressure (PSI):</b> {{ form.artesian_pressure }}</span>
        <span><b>Final Casing Stick Up:</b> {{ form.final_casing_stick_up }} {{ form.final_casing_stick_up ? 'inches':''}}</span>
        <span><b>Artesian Condition:</b> {{ nullBooleanToYesNo(form.artesian_conditions) }} </span>
        <span><b>Well Cap:</b> {{ form.well_cap_type }}</span>
        <span><b>Depth to Bedrock:</b> {{ form.bedrock_depth }} {{ form.bedrock_depth ? 'feet':''}}</span>
        <span><b>Artesian Flow:</b> {{ form.artesian_flow }} {{ form.artesian_flow ? 'USGPM': ''}}</span>
        <span><b>Well Disinfected:</b> {{ form.well_disinfected_status }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section" v-if="sections.decommissionInformation">
      <legend>Well Decommission Information</legend>

      <responsive-grid :cols="12" :lg="4">
        <span><b>Reason for Decommission:</b> {{ form.decommission_reason }}</span>
        <span><b>Method of Decommission:</b> {{ form.decommission_method }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Sealant Material:</b> {{ form.decommission_sealant_material }}</span>
        <span><b>Backfill Material:</b> {{ form.decommission_backfill_material }}</span>
      </responsive-grid>
      <responsive-grid :cols="12" :lg="4">
        <span><b>Decommission Details:</b> {{ form.decommission_details }}</span>
      </responsive-grid>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Pumping Test Information and Aquifer Parameters</legend>
      <div class="table-responsive">
        <DataTable stripedRows size="small" showGridlines :value="filterBlankRows(form.aquifer_parameters_set)">
          <Column field="start_date_pumping_test"/>
          <Column field="pumping_test_description">
            <template #body="slotProps">{{codeToDescription('pumping_test_description_codes', slotProps.data.pumping_test_description)}}</template>
          </Column>
          <Column field="test_duration" header="Test Duration (min)"/>
          <Column field="boundary_effect">
            <template #body="slotProps">{{codeToDescription('boundary_effect_codes', slotProps.data.boundary_effect)}}</template>
          </Column>
          <Column field="storativity"/>
          <Column field="transmissivity" header="Transmissivity (m²/day)"/>
          <Column field="hydraulic_conductivity" header="Hydraulic Conductivity (m/day)"/>
          <Column field="specific_yield"/>
          <Column field="specific_capacity" header="Specific Capacity (L/s/m)"/>
          <Column field="analysis_method">
            <template #body="slotProps">{{codeToDescription('analysis_method_codes', slotProps.data.analysis_method)}}</template>
          </Column>
          <Column field="comments"/>
        </DataTable>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>Comments</legend>
      <p>{{ form.comments ? form.comments : 'No comments submitted' }}</p>
      <p><b>Alternative Specs Submitted:</b> {{ nullBooleanToYesNo(form.alternative_specs_submitted) }}</p>
      <p><b>Technical Report:</b> {{ nullBooleanToYesNo(form.technical_report) }}</p>
      <p><b>Drinking Water Area Indicator:</b> {{ nullBooleanToYesNo(form.drinking_water_protection_area_ind) }}</p>
    </fieldset>

    <fieldset v-if="commonStore.uploadFiles && commonStore.uploadFiles.length > 0">
      <legend>Documents to Upload</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-8">
          <ul class="border border-gray-200 rounded-lg">
            <li v-for="(f, index) in commonStore.uploadFiles" class="px-4 py-2" :key="index">
              {{f.file ? f.file.name.replace('null', '{ASSIGNED_WELL_ID}') : f.name}}
              <a
                class="fa fa-trash fa-lg"
                variant="primary"
                style="margin-left: 0.5em"
                href="#"
                @click="handleDelete(index)"
              ></a>
            </li>
          </ul>
        </div>
      </div>
    </fieldset>

    <fieldset v-if="uploadedFiles && uploadedFiles.public && uploadedFiles.public.length > 0 && reportSubmitted">
      <legend>Uploaded Documents</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-4">
          <ul class="border border-gray-200 rounded-lg">
            <li v-for="(f, index) in uploadedFiles.public" class="px-4 py-2" :key="index">{{f.name}}</li>
          </ul>
        </div>
      </div>
    </fieldset>

    <fieldset v-if="uploadedFiles && uploadedFiles.private && uploadedFiles.private.length > 0 && reportSubmitted">
      <legend>Uploaded Internal Documentation</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-4">
          <ul class="border border-gray-200 rounded-lg">
            <li v-for="(f, index) in uploadedFiles.private" class="px-4 py-2" :key="index">{{f.name}}</li>
          </ul>
        </div>
      </div>
    </fieldset>

    <fieldset class="my-4 detail-section">
      <legend>General Disclaimer</legend>
      <div class="grid grid-cols-12">
        <div class="col-span-12 lg:col-span-9">
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
          Groundwater Data Specialist, email: <a href = "mailto: groundwater@gov.bc.ca" class="text-blue-500 hover:underline">groundwater@gov.bc.ca.</a>
        </div>
      </div>
    </fieldset>

    <!-- Back / Next / Submit controls -->
    <div v-if="!reportSubmitted" class="mt-12">
      <div>
        <Button label="Back to Edit" @click="$emit('back')"/>
      </div>
      <div class="pr-6 text-right">
        <Button label="Submit" id="formSubmitButton" type="submit" ref="activitySubmitBtn" :disabled="formSubmitLoading"/>
      </div>
    </div>
  </div>
</template>

<script>
import { useCommonStore } from '@/stores/common.js'
import CoordsMap from '@/submissions/components/SubmissionForm/CoordsMap.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import filterBlankRows from '@/common/filterBlankRows'
import codeToDescription from '@/common/codeToDescription.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

export default {
  name: 'SubmissionPreview',
  components: {
    CoordsMap,
    ResponsiveGrid
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
      submissionStore: null
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
    this.fetchFiles()
  },
  methods: {
    fetchFiles () {
      this.$emit('fetchFiles')
    },
    handleDelete (index) {
      this.commonStore.uploadFiles.splice(index, 1)
    }
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    },
    commonStore () { return useCommonStore() },
    canEditWells () {
      return this.commonStore.userRoles.wells.edit
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
