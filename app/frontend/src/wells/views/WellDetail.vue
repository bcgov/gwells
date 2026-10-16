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
  <div class="container mb-4 !px-0">
    <Breadcrumb class="p-0" :model="breadcrumbs">
      <template #item="{ item }">
        <router-link v-if="!item.active" :to="item.route">{{ item.label }}</router-link>
        <span v-else>{{ item.label }}</span>
      </template>
    </Breadcrumb>
  </div>
  <div v-if="loading" class="ml-20 mr-20 bg-white">
    <div class="fa-2x text-center">
      <i class="fa fa-circle-o-notch fa-spin"></i>
    </div>
  </div>
  <Card v-else class="container">
    <template #content>
      <div v-if="errorNotFound" class="m-3">
        <h1>Not Found</h1>
        <p>The page you are looking for was not found.</p>
      </div>
      <div v-else class="p-1">
        <Message
            severity="info"
            class="mb-4"
            v-for="(survey, index) in surveys"
            :key="`survey ${index}`">
          <p class="m-0">
            <a :href="survey.survey_link">
              {{ survey.survey_introduction_text }}
            </a>
          </p>
        </Message>
        <Message v-if="show.edit && isUnpublished" severity="warn">
          This well is unpublished and will be hidden from DataBC, iMapBC, GWELLS Well Search, and the CSV/XLS export.
        </Message>
        <!-- SUMMARY -->
        <fieldset id="summary_fieldset" class="detail-section mb-4">
          <legend class="w-full mb-2">
            <div class="float-left mt-2">
              <span class="h2">Well Summary</span>
            </div>
            <div class="float-right m-1">
              <Button id="addNewEntryButton" asChild v-slot="slotProps" v-if="commonStore.authenticated">
                <RouterLink :to="{ name: 'SubmissionsEdit', params: { id } }" :class="slotProps.class">Edit</RouterLink>
              </Button>
              <span class="text-sm mr-4 ml-4">For best print results, use the Chrome browser</span>
              <Button severity="secondary" aria-label="Print" @click="handlePrint"><i class="fa fa-lg fa-print"></i></Button>
            </div>
          </legend>
          <responsive-grid :cols="12" :md="4">
            <span><b>Well Tag Number:</b> {{ well_tag_number }}</span>
            <span><b>Well Status:</b> {{ well_status }}</span>
            <span>
              <b>Observation Well Number: </b>
              <a
                v-if="observation_well_number"
                id="obs_well_number"
                :href="`https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20${observation_well_number}`"
                target="_blank"
              >{{ observation_well_number }}</a>
            </span>

            <span><b>Well Identification Plate Number:</b> {{ identification_plate_number }}</span>
            <span><b>Well Class:</b> {{ well_class }}</span>
            <span><b>Observation Well Status:</b> {{ observation_well_status }}</span>

            <span><b>Owner Name:</b> {{ owner_full_name }}</span>
            <span><b>Well Subclass:</b> {{ well_subclass }}</span>
            <span><b>Environmental Monitoring System (EMS) ID:</b> {{ ems }}</span>

            <span><b>Intended Water Use:</b> {{ intended_water_use }}</span>
            <span>
              <b>Aquifer Number: </b>
              <router-link v-if="aquifer" :to="{ name: 'aquifers-view', params: { id: aquifer } }">
                {{ aquifer }}
              </router-link>
            </span>
            <span><b>Alternative specs submitted:</b> {{ alternative_specs_submitted }}</span>

            <span><b>Artesian Condition:</b> {{ booleanToYesNo(artesian_conditions) }}</span>
            <span>
              <b>Technical Report:</b>
              <a
                v-if="technical_report"
                id="technical_report"
                href='https://foirequestform.gov.bc.ca/?general='
                target="_blank"
                rel="noopener noreferrer"
              > Report Available</a>
              <span v-if="!technical_report"> N/A</span>
            </span>
            <span><b>Drinking Water Area Indicator:</b> {{ booleanToYesNo(drinking_water_protection_area_ind) }}</span>
          </responsive-grid>
        </fieldset>

        <!-- LINKS -->
        <fieldset id="jump_links_fieldset" class="print:hidden detail-section my-4">
          <legend class="w-full mb-2">Sections</legend>
          <responsive-grid :cols="12" :md="4">
            <a class="jump_link" href="#location_information_fieldset">Location Information</a>
            <a class="jump_link" href="#well_activity_fieldset">Well Activity</a>
            <a class="jump_link" href="#well_work_dates_fieldset">Well Work Dates</a>

            <a class="jump_link" href="#well_completion_data_fieldset">Well Completion Data and Artesian Flow</a>
            <a class="jump_link" href="#lithology_fieldset">Lithology</a>
            <a class="jump_link" href="#casing_fieldset">Casing Details</a>

            <a class="jump_link" href="#aquifer_parameters_fieldset">Aquifer Parameters</a>
            <a class="jump_link" href="#surface_seal_fieldset">Surface Seal and Backfill Details</a>
            <a class="jump_link" href="#liner_details_fieldset">Liner Details</a>

            <a class="jump_link" href="#screen_details_fieldset">Screen Details</a>
            <a class="jump_link" href="#well_development_fieldset">Well Development</a>
            <a class="jump_link" href="#well_yield_fieldset">Well Yield</a>
          </responsive-grid>
          <div class="grid grid-cols-12">
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_decommissioning_fieldset">Well Decommissioning</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_comments_fieldset">Comments</a></div>
            <!-- Can't put in reponsive grid bc of this v-if; it doesn't support conditional col display -->
            <div v-if="commonStore.config && commonStore.config.enable_documents" class="col-span-12 md:col-span-4"><a class="jump_link" href="#documents_fieldset">Documentation</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#disclaimer_fieldset">Disclaimer</a></div>
          </div>
        </fieldset>

        <!-- LICENSING -->
        <fieldset id="well_licensing_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Licensing Information</legend>
          <responsive-grid :cols="12" :md="4">
            <span><b>Licensed Status:</b> {{ recordLicence?.status }}</span>
            <span>
              <b>Licence Number{{ recordLicence.number.length > 1 ? "s" : "" }}:</b>&nbsp;
              <a v-for="(licence, index) in recordLicence.number" :key="index" :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${licence}`" target="_blank">
                {{ licence}}{{ index + 1 < recordLicence.number.length ? ", " : ""}}
              </a>
            </span>
          </responsive-grid>
        </fieldset>

        <!-- LOCATION -->
        <fieldset id="location_information_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Location Information</legend>
          <div class="grid grid-cols-12">
            <div class="col-span-12 md:col-span-6">
              <div>
                <span class="font-bold">Street Address:</span> {{ well.street_address }}
              </div>
              <div>
                <span class="font-bold">Town/City:</span> {{ well.city }}
              </div>
              <div>
                <div class="my-4"><span class="font-bold">Legal Description:</span></div>
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
                    <span class="font-bold">Description of Well Location:</span> {{ well.well_location_description }}
                  </div>
                </div>
              </div>
            </div>
            <div class="col-span-12 md:col-span-6">
              <single-well-map :latitude="latitude" :longitude="longitude"/>
              <div class="font-bold mt-12">
                Geographic Coordinates - North American Datum of 1983 (NAD 83)
              </div>
              <div>
                <div><span class="font-bold">Latitude:</span> {{ well.latitude }}</div>
                <div><span class="font-bold">Longitude:</span> {{ well.longitude }}</div>
              </div>
              <div>
                <div><span class="font-bold">UTM Easting:</span> {{ UTM.easting ? Math.round(UTM.easting) : ''}}</div>
                <div><span class="font-bold">UTM Northing:</span> {{ UTM.northing ? Math.round(UTM.northing) : ''}}</div>
              </div>
              <div>
                <div><span class="font-bold">Zone:</span> {{UTM.zone}}</div>
                <div><span class="font-bold">Coordinate Acquisition Code:</span> {{coordinate_acquisition_code}}</div>
              </div>
            </div>
          </div>
        </fieldset>

        <fieldset id="well_activity_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Activity</legend>
          <DataTable
            id="submissionActivityTable"
            ref="submissionActivityTable"
            stripedRows
            showGridlines
            size="small"
            class="border border-gray-200"
            :value="submission_work_dates"
            tableStyle="min-width: 50rem"
            paginator
            :rows="submissionsPerPage"
            :alwaysShowPaginator="false"
            responsiveLayout="scroll"
          >
            <Column
              v-for="field of activity_fields"
              :key="field.key"
              :field="field.key"
              :header="field.label"
              :sortable="field.sortable"
            >
              <template v-if="create_date" v-slot:cell(create_date)="data">
                <div>
                  {{ DateTime.fromISO(data.item.create_date).toLocaleString(DateTime.DATETIME_FULL) }}
                </div>
              </template>
            </Column>
            <template #empty>
              There has been no activity related to this well.
            </template>
          </DataTable>
        </fieldset>

        <fieldset id="well_work_dates_fieldset" class="my-4 detail-section">
          <legend>Well Work Dates</legend>
          <DataTable
            id="wellWorkDatesTable"
            ref="wellWorkDatesTable"
            stripedRows
            showGridlines
            size="small"
            class="border border-gray-200"
            :value="wellDates"
            tableStyle="min-width: 50rem"
          >
            <Column
              v-for="field of work_date_fields"
              :key="field.key"
              :field="field.key"
              :header="field.label"
            />
          </DataTable>
        </fieldset>

        <fieldset id="well_completion_data_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Completion Data</legend>
          <responsive-grid :cols="12" :md="4">
            <span><b>Total Depth Drilled:</b> {{ excludeZeroDecimals(well.total_depth_drilled) }} {{ well.total_depth_drilled ? 'ft bgl':''}}</span>
            <span><b>Estimated Well Yield:</b> {{ excludeZeroDecimals(well.well_yield) }} {{ well.well_yield ? 'USgpm':'' }}</span>
            <span><b>Static Water Level (BTOC):</b> {{ excludeZeroDecimals(well.static_water_level) }} {{ well.static_water_level ? 'feet btoc': ''}}</span>

            <span><b>Finished Well Depth:</b> {{ excludeZeroDecimals(well.finished_well_depth) }} {{ well.finished_well_depth ? 'ft bgl':''}}</span>
            <span><b>Well Cap:</b> {{ well.well_cap_type }}</span>
            <span><b>Artesian Flow:</b> {{ excludeZeroDecimals(well.artesian_flow) }} {{ well.artesian_flow ? 'USgpm':'' }}</span>

            <span><b>Final Casing Stick Up:</b> {{ excludeZeroDecimals(well.final_casing_stick_up) }} {{ well.final_casing_stick_up ? 'inches':''}}</span>
            <span><b>Well Disinfected Status:</b> {{ well.well_disinfected_status }}</span>
            <span><b>Artesian Pressure (head):</b> {{ excludeZeroDecimals(well.artesian_pressure_head) }}</span>

            <span><b>Depth to Bedrock:</b> {{ excludeZeroDecimals(well.bedrock_depth) }} {{ well.bedrock_depth ? 'feet bgl':''}}</span>
            <span>
              <b>Drilling Method<span v-if="well.drilling_methods && well.drilling_methods.length > 1">s</span>:</b>
              <span v-for="(method, index) in well.drilling_methods" :key="`drillingMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </span>
            <span><b>Artesian Pressure (PSI):</b> {{ excludeZeroDecimals(well.artesian_pressure) }}</span>

            <span><b>Ground elevation:</b> {{ excludeZeroDecimals(well.ground_elevation) }} {{ well.ground_elevation ? 'feet':'' }}</span>
            <span><b>Method of determining elevation:</b> {{ well.ground_elevation_method }}</span>
            <span><b>Orientation of Well:</b> {{ well.well_orientation_status }}</span>
          </responsive-grid>
        </fieldset>

        <fieldset id="lithology_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Lithology</legend>
          <DataTable
            id="wellWorkDatesTable"
            ref="wellWorkDatesTable"
            stripedRows
            showGridlines
            size="small"
            class="border border-gray-200"
            :value="lithologydescription_set"
            tableStyle="min-width: 50rem"
          >
            <Column
              v-for="field of lithology_fields"
              :key="field.key"
              :field="field.key"
              :header="field.label"
            >
              <template #body="{ data, field: columnField }">
                <template v-if="['start', 'end', 'water_bearing_estimated_flow'].includes(columnField)">
                {{ excludeZeroDecimals(data[columnField]) }}
                </template>
                <template v-else>
                  {{ data[columnField] }}
                </template>
              </template>
            </Column>
          </DataTable>
        </fieldset>

        <fieldset id="casing_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Casing Details</legend>
          <DataTable
            id="wellWorkDatesTable"
            ref="wellWorkDatesTable"
            stripedRows
            showGridlines
            size="small"
            class="border border-gray-200"
            :value="well.casing_set"
            tableStyle="min-width: 50rem"
          >
            <Column field="start" header="From (ft bgl)">
              <template #body="{ data }">{{ excludeZeroDecimals(data.start) }}</template>
            </Column>
            <Column field="end" header="To (ft bgl)">
              <template #body="{ data }">{{ excludeZeroDecimals(data.end) }}</template>
            </Column>
            <Column field="casing_code" header="Casing Type">
              <template #body="{ data }">{{ codeToDescription('casing_codes', data.casing_code) }}</template>
            </Column>
            <Column field="casing_material" header="Casing Material">
              <template #body="{ data }">{{ codeToDescription('casing_materials', data.casing_material) }}</template>
            </Column>
            <Column field="diameter" header="Diameter (in)">
              <template #body="{ data }">{{ excludeZeroDecimals(data.diameter) }}</template>
            </Column>
            <Column field="wall_thickness" header="Wall Thickness (in)">
              <template #body="{ data }">{{ excludeZeroDecimals(data.wall_thickness) }}</template>
            </Column>
            <Column field="drive_shoe_status" header="Drive Shoe">
              <template #body="{ data }">{{ codeToDescription('drive_shoe', data.drive_shoe_status) }}</template>
            </Column>
          </DataTable>
        </fieldset>

        <fieldset id="surface_seal_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Surface Seal and Backfill Details</legend>
          <responsive-grid :cols="12" :md="4">
            <span><b>Surface Seal Material:</b> {{ codeToDescription('surface_seal_materials', well.surface_seal_material) }}</span>
            <span><b>Backfill Material Above Surface Seal:</b> {{ codeToDescription('surface_seal_materials', well.backfill_above_surface_seal) }}</span>
          </responsive-grid>
          <responsive-grid :cols="12" :md="4">
            <span><b>Surface Seal Installation Method:</b> {{ codeToDescription('surface_seal_methods', well.surface_seal_method) }}</span>
            <span><b>Backfill Depth:</b> {{ excludeZeroDecimals(well.backfill_depth) }} {{ well.backfill_depth ? 'feet':'' }}</span>
          </responsive-grid>
          <responsive-grid :cols="12" :md="4">
            <span><b>Surface Seal Thickness:</b> {{ excludeZeroDecimals(well.surface_seal_thickness) }} {{ well.surface_seal_thickness ? 'inches':'' }}</span>
          </responsive-grid>
          <responsive-grid :cols="12" :md="4">
            <span><b>Surface Seal Depth:</b> {{ excludeZeroDecimals(well.surface_seal_depth) }} {{ well.surface_seal_depth ? 'feet':''}}</span>
          </responsive-grid>
        </fieldset>

        <fieldset id="liner_details_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Liner Details</legend>
          <div class="grid grid-cols-12">
            <div class="col-span-12 md:col-span-6">
              <div><span class="font-bold">Liner Material:</span> {{ codeToDescription('liner_materials', well.liner_material) }}</div>
              <div class="grid grid-cols-2">
                <div><span class="font-bold">Liner Diameter:</span> {{ excludeZeroDecimals(well.liner_diameter) }} {{ well.liner_diameter ? 'inches':'' }}</div>
                <div><span class="font-bold">Liner Thickness:</span> {{ excludeZeroDecimals(well.liner_thickness) }} {{ well.liner_thickness ? 'inches':'' }}</div>
                <div><span class="font-bold">Liner from:</span> {{ excludeZeroDecimals(well.liner_from) }} {{ well.liner_from ? '(ft bgl)':'' }}</div>
                <div><span class="font-bold">Liner to:</span> {{ excludeZeroDecimals(well.liner_to) }} {{ well.liner_to ? '(ft bgl)':'' }}</div>
              </div>
            </div>
            <div class="col-span-12 md:col-span-6">
              <legend class="font-bold mb-2">Liner perforations</legend>
              <DataTable
                stripedRows
                showGridlines
                size="small"
                class="border border-gray-200"
                :value="well.linerperforation_set"
                responsiveLayout="scroll"
                tableStyle="min-width: 30rem"
              >
                <Column field="start" header="From">
                  <template #body="{ data }">{{ excludeZeroDecimals(data.item.start) }}</template>
                </Column>
                <Column field="end" header="To">
                  <template #body="{ data }">{{ excludeZeroDecimals(data.item.end) }}</template>
                </Column>
                <template #empty>
                  <div>There are no records to show</div>
                </template>
              </DataTable>
            </div>
          </div>
        </fieldset>

        <fieldset id="screen_details_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Screen Details</legend>
          <div class="grid grid-cols-12">
            <div class="col-span-12 md:col-span-3">
              <div><span class="font-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', well.screen_intake_method) }}</div>
              <div><span class="font-bold">Type:</span> {{ codeToDescription('screen_types', well.screen_type) }}</div>
              <div><span class="font-bold">Material:</span> {{ codeToDescription('screen_materials', well.screen_material) }}</div>
              <div><span class="font-bold">Opening:</span> {{ codeToDescription('screen_openings', well.screen_opening) }}
              <div><span class="font-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', well.screen_bottom) }}</div>
              </div>
            </div>
            <div class="col-span-12 md:col-span-9">
              <div class="font-bold">Installed Screens</div>
              <DataTable
                stripedRows
                showGridlines
                size="small"
                class="border border-gray-200"
                :value="well.screen_set"
                responsiveLayout="scroll"
                tableStyle="min-width: 30rem"
                >
                <Column field="from" header="From">
                  <template #body="{ data }">{{data.item.start}}</template>
                </Column>
                <Column field="to" header="To">
                  <template #body="{ data }">{{data.item.end}}</template>
                </Column>
                <Column field="diameter" header="Diameter">
                  <template #body="{ data }">{{data.item.diameter}}</template>
                </Column>
                <Column field="assembly_type" header="Assembly Type">
                  <template #body="{ data }">{{codeToDescription('screen_assemblies', data.item.assembly_type)}}</template>
                </Column>
                <Column field="slot_size" header="Slot Size"/>
                <template #empty>
                  <div>There are no records to show</div>
                </template>
              </DataTable>
            </div>
          </div>
        </fieldset>

        <fieldset id="well_development_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Development</legend>
          <responsive-grid :cols="12" :md="4">
            <span>
              <b>Developed by:</b>
              <span v-for="(method, index) in well.development_methods" :key="`developmentMethod${index}`"><span v-if="index > 0">,</span> {{ method }}</span>
            </span>
            <span><b>Development Total Duration:</b> {{ excludeZeroDecimals(well.development_hours) }} {{ well.development_hours ? 'hours':'' }}</span>
          </responsive-grid>
        </fieldset>

        <fieldset id="well_yield_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Yield</legend>
          <responsive-grid :cols="12" :md="4">
            <span><b>Estimation Method:</b> {{codeToDescription('yield_estimation_methods', well.yield_estimation_method)}}</span>
            <span><b>Estimation Rate:</b> {{ excludeZeroDecimals(well.yield_estimation_rate) }} {{ well.yield_estimation_rate ? 'USgpm':'' }}</span>
            <span><b>Estimation Duration:</b> {{ excludeZeroDecimals(well.yield_estimation_duration) }} {{ well.yield_estimation_duration ? 'hours':'' }}</span>
            <span><b>Static Water Level Before Test:</b> {{ excludeZeroDecimals(well.static_level_before_test) }} {{ well.static_level_before_test ? 'ft (btoc)':'' }}</span>
            <span><b>Drawdown:</b> {{ excludeZeroDecimals(well.drawdown) }} {{ well.drawdown ? 'ft (btoc)':'' }}</span>
          </responsive-grid>
          <responsive-grid :cols="12" :md="4">
            <span><b>Hydrofracturing Performed:</b> {{booleanToYesNo(well.hydro_fracturing_performed)}}</span>
            <span><b>Increase in Yield Due to Hydrofracturing:</b> {{ excludeZeroDecimals(well.hydro_fracturing_yield_increase) }} {{ well.hydro_fracturing_yield_increase ? 'USgpm':'' }}</span>
          </responsive-grid>
        </fieldset>

        <fieldset id="well_decommissioning_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Decommission Information</legend>
          <responsive-grid :cols="12" :md="4">
            <span><b>Reason for Decommission:</b> {{ well.decommission_reason }}</span>
            <span><b>Method of Decommission:</b> {{ well.decommission_method }}</span>
          </responsive-grid>
          <responsive-grid :cols="12" :md="4">
            <span><b>Sealant Material:</b> {{ well.decommission_sealant_material }}</span>
            <span><b>Backfill Material:</b> {{ well.decommission_backfill_material }}</span>
          </responsive-grid>
          <responsive-grid :cols="12" :md="4">
            <span><b>Decommission Details:</b> {{ well.decommission_details }}</span>
          </responsive-grid>
        </fieldset>

        <fieldset id="aquifer_parameters_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Pumping Test Information and Aquifer Parameters</legend>
          <DataTable
            stripedRows
            showGridlines
            size="small"
            class="border border-gray-200"
            :value="well.aquifer_parameters_set"
            tableStyle="min-width: 50rem"
            >
            <Column v-for="field in aquifer_parameters_fields" :key="field.key" :field="field.key">
              <template #header>
                <span>{{ field.label }}</span>&nbsp;
                <i v-if="TOOLTIP_TEXT.pumping_test_information[field.key]"
                  class="fa fa-question-circle color-info print:hidden"
                  v-tooltip="TOOLTIP_TEXT.pumping_test_information[field.key]">
                </i>
              </template>
              <template #body="{ data }">
                <template v-if="['pumping_test_description', 'boundary_effect', 'analysis_method'].includes(field.key)">
                  {{ codeToDescription(`${field.key}_codes`, data[field.key]) }}
                </template>
                <template v-else-if="['storativity', 'transmissivity', 'hydraulic_conductivity'].includes(field.key)">
                  {{ data[field.key] ? parseFloat(data[field.key]).toString() : '' }}
                </template>
                <template v-else>
                  {{ data[field.key] }}
                </template>
              </template>
            </Column>
            <template #empty>
              There are no records to show
            </template>
          </DataTable>
        </fieldset>

        <fieldset id="well_comments_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Comments</legend>
          <p>
            {{ well.comments ? well.comments : 'No comments submitted' }}
          </p>
        </fieldset>

        <fieldset id="documents_fieldset" class="detail-section my-4">
          <legend class="w-full mb-2">Documents</legend>
          <documents :well="id"/>
        </fieldset>

        <fieldset id="disclaimer_fieldset" class="detail-section my-4">
          <legend class="w-full mb-2">Disclaimer</legend>
          <p>
            The information provided should not be used as a basis for making financial or any other commitments. The Government of British Columbia accepts no liability for the accuracy, availability, suitability, reliability, usability, completeness or timeliness of the data or graphical depictions rendered from the data.
          </p>
        </fieldset>

      </div>
    </template>
  </Card>
</template>

<script>
import { mapStores } from 'pinia'
import { useCommonStore } from '@/stores/common.js'
import { useSubmissionStore } from '@/stores/submission.js'

import { DateTime } from 'luxon'

import SingleWellMap from '@/wells/components/SingleWellMap.vue'
import Documents from '@/wells/components/Documents.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue';
import ApiService from '@/common/services/ApiService.js'
import codeToDescription from '@/common/codeToDescription.js'
import { TOOLTIP_TEXT } from '@/common/constants.js'
import { useWellsStore } from '@/stores/wells.js'
import { booleanToYesNo, excludeZeroDecimals } from '../../common/filters'

export default {
  name: 'WellDetail',
  components: {
    SingleWellMap,
    Documents,
    ResponsiveGrid
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
      aquifer_parameters_fields: [
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
      ],
      breadcrumbs: [
        {
          label: 'Well Search',
          route: { name: 'wells-home' }
        },
        {
          label: this.errorNotFound ? 'Not found' : 'Well Summary',
          active: true
        }
      ],
      submissionsPerPage: 5,
      submissionsPage: 1,
      recordLicence: { status: '', number: [] },
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapStores(useCommonStore, useSubmissionStore, useWellsStore),
    well () { return this.wellsStore.wellRecord ?? {} },
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
    id () { return parseInt(this.$route.params.id) || null },
    wellDates () {
      return [{
        construction_start_date: this.wellsStore.wellRecord?.construction_start_date,
        construction_end_date: this.wellsStore.wellRecord?.construction_end_date,
        alteration_start_date: this.wellsStore.wellRecord?.alteration_start_date,
        alteration_end_date: this.wellsStore.wellRecord?.alteration_end_date,
        decommission_start_date: this.wellsStore.wellRecord?.decommission_start_date,
        decommission_end_date: this.wellsStore.wellRecord?.decommission_end_date
      }]
    },
    errorNotFound () {
      return this.error && this.error.status === 404
    },
    show () {
      return {
        edit: !!this.commonStore.config && this.commonStore.userRoles.wells.edit === true
      }
    },
    UTM () {
      // converts form lat/long and returns an object containing UTM easting, northing, and zone
      if (this.well && this.well.latitude && this.well.longitude) {
        return this.convertToUTM(Number(this.well.longitude), Number(this.well.latitude))
      }
      return {}
    },
    isUnpublished () { return !this.wellsStore.wellRecord?.is_published},
  },
  methods: {
    booleanToYesNo (value) {
      return booleanToYesNo(value)
    },
    excludeZeroDecimals (value) {
      return excludeZeroDecimals(value)
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
    this.fetchSurveys()
    this.submissionStore.fetchCodes()
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
.jump_link {
  color: #1a5a96;
  text-decoration: none;
}
.jump_link:hover {
  text-decoration: underline;
}

@media print {
  .well-detail {
    fieldset {
      page-break-inside: avoid;
    }

    .card {
      border: none;
    }
  }
}
</style>
