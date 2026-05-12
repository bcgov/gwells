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
    <Breadcrumb :model="breadcrumbs"/>
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
              <Button id="addNewEntryButton" asChild v-slot="slotProps">
                <RouterLink :to="{ name: 'SubmissionsEdit', params: { id } }" :class="slotProps.class">Edit</RouterLink>
              </Button>
              <span class="text-sm mr-4 ml-4">For best print results, use the Chrome browser</span>
              <Button severity="secondary" aria-label="Print" @click="handlePrint"><i class="fa fa-lg fa-print"></i></Button>
            </div>
          </legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Tag Number:</span> {{ well_tag_number }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Status:</span> {{ well_status }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Observation Well Number: </span>
              <a
                v-if="observation_well_number"
                id="obs_well_number"
                :href="`https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS%20WELL%20${observation_well_number}`"
                target="_blank"
              >{{ observation_well_number }}</a>
            </div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Identification Plate Number:</span> {{ identification_plate_number }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Class:</span> {{ well_class }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Observation Well Status:</span> {{ observation_well_status }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Owner Name:</span> {{ owner_full_name }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Subclass:</span> {{ well_subclass }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Environmental Monitoring System (EMS) ID:</span> {{ ems }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Intended Water Use:</span> {{ intended_water_use }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Aquifer Number: </span>
              <router-link v-if="aquifer" :to="{ name: 'aquifers-view', params: { id: aquifer } }">
                {{ aquifer }}
              </router-link>
            </div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Alternative specs submitted:</span> {{ alternative_specs_submitted }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Artesian Condition:</span> {{ booleanToYesNo(artesian_conditions) }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Technical Report:</span>
              <a
                v-if="technical_report"
                id="technical_report"
                href='https://foirequestform.gov.bc.ca/?general='
                target="_blank"
                rel="noopener noreferrer"
              > Report Available</a>
              <span v-if="!technical_report"> N/A</span>
            </div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Drinking Water Area Indicator:</span> {{ booleanToYesNo(drinking_water_protection_area_ind) }}</div>
          </div>
        </fieldset>

        <!-- LINKS -->
        <fieldset id="jump_links_fieldset" class="d-print-none detail-section my-4">
          <legend class="w-full mb-2">Sections</legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#location_information_fieldset">Location Information</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_activity_fieldset">Well Activity</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_work_dates_fieldset">Well Work Dates</a></div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_completion_data_fieldset">Well Completion Data and Artesian Flow</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#lithology_fieldset">Lithology</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#casing_fieldset">Casing Details</a></div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#aquifer_parameters_fieldset">Aquifer Parameters</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#surface_seal_fieldset">Surface Seal and Backfill Details</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#liner_details_fieldset">Liner Details</a></div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#screen_details_fieldset">Screen Details</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_development_fieldset">Well Development</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_yield_fieldset">Well Yield</a></div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_decommissioning_fieldset">Well Decommissioning</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#well_comments_fieldset">Comments</a></div>
            <div v-if="commonStore.config && commonStore.config.enable_documents" class="col-span-12 md:col-span-4"><a class="jump_link" href="#documents_fieldset">Documentation</a></div>
            <div class="col-span-12 md:col-span-4"><a class="jump_link" href="#disclaimer_fieldset">Disclaimer</a></div>
          </div>
        </fieldset>

        <!-- LICENSING -->
        <fieldset id="well_licensing_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Licensing Information</legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Licensed Status:</span> {{ recordLicence?.status }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Licence Number{{ recordLicence.number.length > 1 ? "s" : "" }}:</span>&nbsp;
              <a v-for="(licence, index) in recordLicence.number" :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${licence}`" target="_blank">
                {{ licence}}{{ index + 1 < recordLicence.number.length ? ", " : ""}}
              </a>
            </div>
          </div>
        </fieldset>

        <!-- LOCATION -->
        <fieldset id="location_information_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Location Information</legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-6">
              <div>
                <span class="font-bold">Street Address:</span> {{ street_address }}
              </div>
              <div>
                <span class="font-bold">Town/City:</span> {{ city }}
              </div>
              <div>
                <div class="my-4"><span class="font-bold">Legal Description:</span></div>
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
                    <span class="font-bold">Description of Well Location:</span> {{ well_location_description }}
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
                <div><span class="font-bold">Latitude:</span> {{latitude}}</div>
                <div><span class="font-bold">Longitude:</span> {{longitude}}</div>
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
              sortable
            >
              <template v-if="create_date" v-slot:cell(create_date)="data">
                <div>
                  {{ formatDate(data.item.create_date, "MMMM Do YYYY [at] LT") }}
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
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Total Depth Drilled:</span> {{ excludeZeroDecimals(total_depth_drilled) }} {{ total_depth_drilled ? 'ft bgl':''}}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Estimated Well Yield:</span> {{ excludeZeroDecimals(well_yield) }} {{ well_yield ? 'USgpm':'' }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Static Water Level (BTOC):</span> {{ excludeZeroDecimals(static_water_level) }} {{ static_water_level ? 'feet btoc': ''}}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Finished Well Depth:</span> {{ excludeZeroDecimals(finished_well_depth) }} {{ finished_well_depth ? 'ft bgl':''}}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Cap:</span> {{ well_cap_type }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Artesian Flow:</span> {{ excludeZeroDecimals(artesian_flow) }} {{ artesian_flow ? 'USgpm':'' }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Final Casing Stick Up:</span> {{ excludeZeroDecimals(final_casing_stick_up) }} {{ final_casing_stick_up ? 'inches':''}}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Well Disinfected Status:</span> {{ well_disinfected_status }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Artesian Pressure (head):</span> {{ excludeZeroDecimals(artesian_pressure_head) }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Depth to Bedrock:</span> {{ excludeZeroDecimals(bedrock_depth) }} {{ bedrock_depth ? 'feet bgl':''}}</div>
            <div class="col-span-12 md:col-span-4">
              <span class="font-bold">Drilling Method<span v-if="drilling_methods && drilling_methods.length > 1">s</span>:</span>
              <span v-for="(method, index) in drilling_methods" :key="`drillingMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Artesian Pressure (PSI):</span> {{ excludeZeroDecimals(artesian_pressure) }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Ground elevation:</span> {{ excludeZeroDecimals(ground_elevation) }} {{ ground_elevation ? 'feet':'' }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Method of determining elevation:</span> {{ ground_elevation_method }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Orientation of Well:</span> {{ well_orientation_status }}</div>
          </div>
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
            :value="casing_set"
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
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Surface Seal Material:</span> {{ codeToDescription('surface_seal_materials', surface_seal_material) }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Backfill Material Above Surface Seal:</span> {{ codeToDescription('surface_seal_materials', backfill_above_surface_seal) }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Surface Seal Installation Method:</span> {{ codeToDescription('surface_seal_methods', surface_seal_method) }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Backfill Depth:</span> {{ excludeZeroDecimals(backfill_depth) }} {{ backfill_depth ? 'feet':'' }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Surface Seal Thickness:</span> {{ excludeZeroDecimals(surface_seal_thickness) }} {{ surface_seal_thickness ? 'inches':'' }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Surface Seal Depth:</span> {{ excludeZeroDecimals(surface_seal_depth) }} {{ surface_seal_depth ? 'feet':''}}</div>
          </div>
        </fieldset>

        <fieldset id="liner_details_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Liner Details</legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-6">
              <div><span class="font-bold">Liner Material:</span> {{ codeToDescription('liner_materials', liner_material) }}</div>
              <div class="grid grid-cols-2">
                <div><span class="font-bold">Liner Diameter:</span> {{ excludeZeroDecimals(liner_diameter) }} {{ liner_diameter ? 'inches':'' }}</div>
                <div><span class="font-bold">Liner Thickness:</span> {{ excludeZeroDecimals(liner_thickness) }} {{ liner_thickness ? 'inches':'' }}</div>
                <div><span class="font-bold">Liner from:</span> {{ excludeZeroDecimals(liner_from) }} {{ liner_from ? '(ft bgl)':'' }}</div>
                <div><span class="font-bold">Liner to:</span> {{ excludeZeroDecimals(liner_to) }} {{ liner_to ? '(ft bgl)':'' }}</div>
              </div>
            </div>
            <div class="col-span-12 md:col-span-6">
              <legend class="font-bold mb-2">Liner perforations</legend>
              <DataTable
                stripedRows
                showGridlines
                size="small"
                class="border border-gray-200"
                :value="linerperforation_set"
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
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-3">
              <div><span class="font-bold">Intake Method:</span> {{ codeToDescription('screen_intake_methods', screen_intake_method) }}</div>
              <div><span class="font-bold">Type:</span> {{ codeToDescription('screen_types', screen_type) }}</div>
              <div><span class="font-bold">Material:</span> {{ codeToDescription('screen_materials', screen_material) }}</div>
              <div><span class="font-bold">Opening:</span> {{ codeToDescription('screen_openings', screen_opening) }}
              <div><span class="font-bold">Bottom:</span> {{ codeToDescription('screen_bottoms', screen_bottom) }}</div>
              </div>
            </div>
            <div class="col-span-12 md:col-span-9">
              <div class="font-bold">Installed Screens</div>
              <DataTable
                stripedRows
                showGridlines
                size="small"
                class="border border-gray-200"
                :value="screen_set"
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
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4">
              <span class="font-bold">Developed by:</span>
              <span v-for="(method, index) in development_methods" :key="`developmentMethod${index}`"><span v-if="index > 0">,</span> {{ method.description }}</span>
            </div>
            <div class="col-span-12 md:col-span-4">
              <span class="font-bold">Development Total Duration:</span> {{ excludeZeroDecimals(development_hours) }} {{ development_hours ? 'hours':'' }}
            </div>
          </div>
        </fieldset>

        <fieldset id="well_yield_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Yield</legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Estimation Method:</span> {{codeToDescription('yield_estimation_methods', yield_estimation_method)}} </div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Estimation Rate:</span> {{ excludeZeroDecimals(yield_estimation_rate) }} {{ yield_estimation_rate ? 'USgpm':'' }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Estimation Duration:</span> {{ excludeZeroDecimals(yield_estimation_duration) }} {{ yield_estimation_duration ? 'hours':'' }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Static Water Level Before Test:</span> {{ excludeZeroDecimals(static_level_before_test) }} {{ static_level_before_test ? 'ft (btoc)':'' }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Drawdown:</span> {{ excludeZeroDecimals(drawdown) }} {{ drawdown ? 'ft (btoc)':'' }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Hydrofracturing Performed:</span> {{booleanToYesNo(hydro_fracturing_performed)}}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Increase in Yield Due to Hydrofracturing:</span> {{ excludeZeroDecimals(hydro_fracturing_yield_increase) }} {{ hydro_fracturing_yield_increase ? 'USgpm':'' }}</div>
          </div>
        </fieldset>

        <fieldset id="well_decommissioning_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Well Decommission Information</legend>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Reason for Decommission:</span> {{ decommission_reason }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Method of Decommission:</span> {{ decommission_method }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Sealant Material:</span> {{ decommission_sealant_material }}</div>
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Backfill Material:</span> {{ decommission_backfill_material }}</div>
          </div>
          <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 md:col-span-4"><span class="font-bold">Decommission Details:</span> {{ decommission_details }}</div>
          </div>
        </fieldset>

        <fieldset id="aquifer_parameters_fieldset" class="my-4 detail-section">
          <legend class="w-full mb-2">Pumping Test Information and Aquifer Parameters</legend>
          <DataTable
            stripedRows
            showGridlines
            size="small"
            class="border border-gray-200"
            :value="aquifer_parameters_set"
            tableStyle="min-width: 50rem"
            >
            <Column v-for="field in aquifer_parameters_fields" :key="field.key" :field="field.key">
              <template #header>
                <span>{{ field.label }}</span>&nbsp;
                <i v-if="TOOLTIP_TEXT.pumping_test_information[field.key]"
                  class="fa fa-question-circle color-info d-print-none"
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
            {{ comments ? comments : 'No comments submitted' }}
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

import moment from 'moment'

import SingleWellMap from '@/wells/components/SingleWellMap.vue'
import Documents from '@/wells/components/Documents.vue'
import convertCoordinatesMixin from '@/common/convertCoordinatesMixin.js'
import ApiService from '@/common/services/ApiService.js'
import codeToDescription from '@/common/codeToDescription.js'
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
      submissionsPerPage: 5,
      submissionsPage: 1,
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapStores(useCommonStore, useSubmissionStore, useWellsStore),
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
    breadcrumbs () {
      return [
        {
          label: 'Well Search',
          url: '/'
        },
        {
          label: this.errorNotFound ? 'Not found' : 'Well Summary'
        }
      ]
    },
    isUnpublished () {
      //  TypeError: Cannot read properties of undefined (reading 'is_published')
      return !this.well?.is_published
    },
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
