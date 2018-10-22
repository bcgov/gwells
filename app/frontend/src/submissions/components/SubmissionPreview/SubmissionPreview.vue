<template>
  <div>
    <fieldset class="my-3 detail-section">
      <legend>Type of Work and Well Class</legend>
      <b-row>
        <b-col>
          <span class="font-weight-bold">Report Type:</span> {{ activity }}
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Class of Well:</span> {{ form.well_class }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Subclass:</span> {{ wellSubclass }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Intended Water Use:</span> {{ form.intended_water_use }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Tag Number:</span> {{ form.well ? form.well['well_tag_number']: '' }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Well Identification Plate Number:</span> {{ form.identification_plate_number }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Where Plate Attached:</span> {{ form.well_plate_attached }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Work Start Date:</span> {{ form.work_start_date }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Work End Date:</span> {{ form.work_end_date }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Person Responsible for Work</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Person Responsible for Work:</span> {{ form.driller_responsible ? form.driller_responsible['name'] : '' }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Person Who Performed Work:</span> {{ form.driller_name }}</b-col>
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
          <div class="mb-5">
            <preview-map :latitude="form.latitude" :longitude="form.longitude"></preview-map>
          </div>
          <div class="my-5">&nbsp;</div>
          <div><span class="font-weight-bold">Geographic Coordinates - North American Datum of 1983 (NAD 83)</span></div>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Latitude:</span> {{form.latitude}}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Longitude:</span> {{form.longitude}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">UTM Easting:</span> {{form.easting}}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">UTM Northing:</span> {{form.northing}}</b-col>
          </b-row>
          <b-row>
            <b-col cols="12" lg="4"><span class="font-weight-bold">Zone:</span> {{form.utm_zone}}</b-col>
            <b-col cols="12" lg="6"><span class="font-weight-bold">Location Accuracy Code:</span> {{form.location_accuracy_code}}</b-col>
          </b-row>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Method of Drilling</legend>
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
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.lithology">
      <legend>Lithology</legend>
      <div class="table-responsive">
        <b-table
          :items="filterBlankRows(form.lithology_set)"
          show-empty
          :fields="[
            'from',
            'to',
            'primary',
            'secondary',
            'bedrock',
            'descriptor',
            'colour',
            'hardness',
            'moisture',
            'water_bearing_flow',
            'observations'
          ]"></b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.closureDescription">
      <legend>Decommission Description</legend>
      <div class="table-responsive">
        <b-table
          :items="filterBlankRows(form.decommission_description_set)"
          :fields="['start', 'end', 'material', 'observations']"
          show-empty
        ></b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Casing Details</legend>
      <div class="table-responsive">
        <b-table
            :items="filterBlankRows(form.casing_set)"
            :fields="['from', 'to', 'casing_code', 'casing_material', 'diameter', 'wall_thickness', 'drive_shoe']"
            show-empty>

          <template slot="from" slot-scope="data">{{data.item.start}} ft</template>
          <template slot="to" slot-scope="data">{{data.item.end}} ft</template>
        </b-table>
      </div>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.backfill">
      <legend>Surface Seal and Backfill Details</legend>
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
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.liner">
      <legend>Liner Details</legend>
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
          <b-table
              :items="filterBlankRows(form.linerperforation_set)"
              :fields="['from', 'to']"
              show-empty
          >
            <template slot="from" slot-scope="data">{{data.item.start}} ft</template>
            <template slot="to" slot-scope="data">{{data.item.end}} ft</template>
          </b-table>
        </b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.screens">
      <legend>Screen Details</legend>
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
          <div class="font-weight-bold">Installed Screens</div>
          <b-table
              :items="filterBlankRows(form.screen_set)"
              :fields="['from', 'to', 'internal_diameter', 'assembly_type', 'slot_size']"
              show-empty
              >
            <template slot="from" slot-scope="data">{{data.item.start}} ft</template>
            <template slot="to" slot-scope="data">{{data.item.end}} ft</template>
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
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack material:</span> {{ form.filter_pack_material }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Filter pack material size:</span> {{ form.filter_pack_material_size }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.wellDevelopment">
      <legend>Well Development</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Developed by:</span> {{ form.development_method }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Development Total Duration:</span> {{ form.development_hours }} {{ form.development_hours ? 'hours':'' }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.wellYield">
      <legend>Well Yield</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Method:</span> </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Rate:</span> </b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Estimation Duration:</span></b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.waterQuality">
      <legend>Water Quality</legend>
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
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.wellCompletion">
      <legend>Well Completion Data</legend>
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
    </fieldset>

    <fieldset class="my-3 detail-section" v-if="sections.decommissionInformation">
      <legend>Well Decommission Information</legend>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Finished Well Depth:</span> {{ form.finished_well_depth }} {{ form.finished_well_depth ? 'feet':''}}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Sealant Material:</span> {{ form.sealant_material }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Reason for Decommission:</span> {{ form.decommission_reason }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Backfill Material:</span> {{ form.backfill_material }}</b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Method of Decommission:</span> {{ form.decommission_method }}</b-col>
        <b-col cols="12" lg="4"><span class="font-weight-bold">Decommission Details:</span> {{ form.decommission_details }}</b-col>
      </b-row>
    </fieldset>

    <fieldset class="my-3 detail-section">
      <legend>Comments</legend>
      <p>
        {{ form.comments ? form.comments : 'No comments submitted' }}
      </p>
      <p>
        <span class="font-weight-bold">Alternative Specs Submitted:</span> {{ form.alternative_specs_submitted }}
      </p>
    </fieldset>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PreviewMap from '@/submissions/components/SubmissionPreview/PreviewMap.vue'
import filterBlankRows from '@/common/filterBlankRows'
export default {
  name: 'SubmissionPreview',
  components: {
    PreviewMap
  },
  mixins: [filterBlankRows],
  props: [
    'form',
    'activity',
    'sections'
  ],
  computed: {
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
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
