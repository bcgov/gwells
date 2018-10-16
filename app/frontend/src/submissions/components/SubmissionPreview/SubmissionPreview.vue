<template>
  <div>
    <h2>Well Submission Preview</h2>
    <div class="my-3">
      <h3>Type of Work and Well Class</h3>
      <b-row>
        <b-col>
          <span class="font-weight-bold">Report Type:</span> {{ activity }}
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Class of Well:</span> {{ form.well_class }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Subclass:</span> {{ form.well_subclass }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Intended Water Use:</span> {{ form.intended_water_use }}</b-col>

      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Tag Number:</span> {{ form.well }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ form.identification_plate_number }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Where Plate Attached:</span> {{ form.well_plate_attached }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Work Start Date:</span> {{ form.work_start_date }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Work End Date:</span> {{ form.work_end_date }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Person Responsible for Work</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Person Responsible for Work:</span> {{ form.driller_responsible }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Person Who Performed Work:</span> {{ form.driller_name }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Consultant Name:</span> {{ form.consultant_name }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Consultant Company:</span> {{ form.consultant_company }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Well Owner</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Name:</span> {{ form.owner_full_name }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="3"><span class="font-weight-bold">Mailing address:</span> {{ form.owner_mailing_address }}</b-col>
        <b-col cols="12" lg="3"><span class="font-weight-bold">City:</span> {{ form.owner_city }}</b-col>
        <b-col cols="12" lg="3"><span class="font-weight-bold">Province:</span> {{ form.owner_province_state }}</b-col>
        <b-col cols="12" lg="3"><span class="font-weight-bold">Postal Code:</span> {{ form.owner_postal_code }}</b-col>

      </b-row>
    </div>

    <div class="my-3">
      <h3>Location Information</h3>
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
                <table class="table table-sm table-striped">
                  <tbody>
                    <tr>
                      <th>Lot</th>
                      <td>{{ form.legal_lot }}</td>
                    </tr>
                    <tr>
                      <th>Plan</th>
                      <td>{{ form.legal_plan }}</td>
                    </tr>
                    <tr>
                      <th>District Lot</th>
                      <td>{{ form.legal_district_lot }}</td>
                    </tr>
                    <tr>
                      <th>Block</th>
                      <td>{{ form.legal_block }}</td>
                    </tr>
                    <tr>
                      <th>Section</th>
                      <td>{{ form.legal_section }}</td>
                    </tr>
                    <tr>
                      <th>Township</th>
                      <td>{{ form.legal_township }}</td>
                    </tr>
                    <tr>
                      <th>Range</th>
                      <td>{{ form.legal_range }}</td>
                    </tr>
                    <tr>
                      <th>Land District</th>
                      <td>{{ form.land_district }}</td>
                    </tr>
                    <tr>
                      <th>Property Identification Description (PID)</th>
                      <td>{{ form.legal_pid }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="12" lg="6" xl="6" offset-xl="2">
          <div class="mb-5">This is a map.</div>
          <div class="my-5">&nbsp;</div>
          <div><span class="font-weight-bold">Geographic Coordinates - North American Datum of 1983 (NAD 83)</span></div>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Latitude:</span> 11222</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Longitude:</span> 11222</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">UTM Easting:</span> 11222</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">UTM Northing:</span> 11222</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Zone:</span> 7</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Location Accuracy Code:</span> J</b-col>
          </b-row>
        </b-col>
      </b-row>
    </div>
    <div class="my-3">
      <h3>Method of Drilling</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Ground elevation:</span> {{ form.ground_elevation }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ form.ground_elevation_method }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Drilling method:</span> {{ form.drilling_method }}</b-col>
        <!-- <b-col cols="12" lg="3"><span class="font-weight-bold">Specify other method:</span> {{ form.other_drilling_method }}</b-col> -->
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Orientation of well:</span> {{ form.well_orientation }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Lithology</h3>
      <div class="table-responsive">
        <b-table :items="form.lithology_set" show-empty></b-table>
      </div>
    </div>

    <div class="my-3">
      <h3>Casing Details</h3>
      <div class="table-responsive">
        <b-table :items="form.casing_set" :fields="['start', 'end']" show-empty></b-table>
      </div>
    </div>

    <div class="my-3">
      <h3>Surface Seal and Backfill Details</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Material:</span> {{ form.surface_seal_material }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Method of determining elevation:</span> {{ form.backfill_above_surface_seal }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Installation Method:</span> {{ form.surface_seal_method }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Depth:</span> {{ form.backfill_above_surface_seal_depth }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Thickness:</span> {{ form.surface_seal_thickness }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Surface Seal Depth:</span> {{ form.surface_seal_depth }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Liner Details</h3>
      <b-row>
        <b-col cols="12" lg="6">
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Liner Material:</span> {{ form.liner_material }}</b-col>
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
          <b-table :items="form.linerperforation_set" :fields="['from', 'to']"></b-table>
        </b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Screen Details</h3>
      <b-row>
        <b-col cols="12" lg="4">
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Intake Method:</span> {{ form.screen_intake_method }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Type:</span> {{ form.screen_type }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Material:</span> {{ form.screen_material }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Opening:</span> {{ form.screen_opening }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Bottom:</span> {{ form.screen_bottom }}</b-col>
          </b-row>
        </b-col>
        <b-col cols="12" lg="8">
          <b-table :items="form.screen_set" :fields="['from', 'to']"></b-table>
        </b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Filter Pack</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack from:</span> {{ form.filter_pack_from }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack to:</span> {{ form.filter_pack_to }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack thickness:</span> {{ form.filter_pack_thickness }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack material:</span> {{ form.filter_pack_material }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack material size:</span> {{ form.filter_pack_material_size }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Well Development</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Developed by:</span> {{ form.development_method }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Development Total Duration:</span> {{ form.development_hours }} {{ form.development_hours ? 'hours':'' }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Well Yield</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Method:</span> </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Rate:</span> </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Duration:</span></b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Water Quality</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Characteristics:</span>
          <span v-for="(item, index) in form.water_quality_characteristics" :key="`previewWaterCharacteristic${index}`">
            <!-- Add a comma before each item except index 0 -->
            {{ index ? ', ': ''}}{{ item }}
          </span>
        </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Water Quality Colour:</span> {{ form.water_quality_colour }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6"><span class="font-weight-bold">Water Quality Odour:</span> {{ form.water_quality_odour }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6"><span class="font-weight-bold">EMS ID:</span> {{ form.ems_id }}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Well Completion Data</h3>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Total Depth Drilled:</span> {{ form.total_depth_drilled }} {{ form.total_depth_drilled ? 'feet':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Static Water Level (BTOC):</span> {{ form.static_water_level }} {{ form.static_water_level ? 'feet': ''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Cap:</span> {{ form.well_cap_type }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ form.finished_well_depth }} {{ form.finished_well_depth ? 'feet':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimated Well Yield:</span> {{ form.well_yield }} {{ form.well_yield ? 'USGPM': ''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Disinfected:</span> {{ form.well_disinfected }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Final Casing Stick Up:</span> {{ form.final_casing_stick_up }} {{ form.final_casing_stick_up ? 'inches':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Flow:</span> {{ form.artesian_flow }} {{ form.artesian_flow ? 'USGPM': ''}}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Depth to Bedrock:</span> {{ form.depth_to_bedrock }} {{ form.depth_to_bedrock ? 'feet':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Artesian Pressure:</span> {{ form.artesian_pressure }} {{ form.artesian_pressure ? 'feet': ''}}</b-col>
      </b-row>
    </div>

    <div class="my-3">
      <h3>Comments</h3>
      <p>
        {{ form.comments ? form.comments : 'No comments submitted' }}
      </p>
      <p>
        <span class="font-weight-bold">Alternative Specs Submitted:</span> {{ form.alternative_specs_submitted }}
      </p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SubmissionPreview',
  props: [
    'form',
    'activity'
  ]
}
</script>

<style>

</style>
