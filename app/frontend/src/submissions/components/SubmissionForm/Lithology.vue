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
  <fieldset>
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Lithology</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive">
      <table class="table table-sm" aria-describedby="lithologyDetails">
        <thead>
          <tr>
            <th class="font-weight-normal">
              <div>From</div><div>ft (bgl)</div>
            </th>
            <th class="font-weight-normal">
              <div>To</div><div>ft (bgl)</div>
            </th>
            <th class="font-weight-normal">
              Soil or Bedrock Description
            </th>
            <th class="font-weight-normal">
              Materials
            </th>
            <th class="font-weight-normal">
              Descriptor
            </th>
            <th class="font-weight-normal">
              Moisture
            </th>
            <th class="font-weight-normal">
              Colour
            </th>
            <th class="font-weight-normal">
              Hardness
            </th>
            <th class="font-weight-normal input-width-medium">
              Water Bearing Flow Estimate (USGPM)
            </th>
            <th class="font-weight-normal">
              Observations
            </th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(row, index) in lithologyData">
            <tr :key="`lithology row ${index}`" :id="`lithologyRow${index}`">
              <td class="input-width-small">
                <form-input
                  :id="`lithologyDepthFrom${index}`"
                  aria-label="Depth from (feet)"
                  type="number"
                  v-model="lithologyData[index].start"
                  group-class="mt-1 mb-0"/>
              </td>
              <td class="input-width-small">
                <form-input
                  :id="`lithologyDepthTo${index}`"
                  aria-label="Depth to (feet)"
                  type="number"
                  v-model="lithologyData[index].end"
                  group-class="mt-1 mb-0"/>
              </td>
              <td>
                <form-input
                    :id="`lithologyDescription${index}`"
                    aria-label="Soil or Bedrock Description"
                    v-model="lithologyData[index].lithology_raw_data"
                    group-class="mt-1 mb-0"
                    @input="parseDescription(index, $event)"
                ></form-input>
              </td>
              <td class="input-width-medium">
                <div class="material-badges">
                  <b-badge v-for="(soil, j) in lithSoils[index]" variant="light" class="font-weight-normal" :key="`soilTerm-${index}-${j}`">
                    {{ soil }}
                  </b-badge>
                </div>
              </td>
              <td class="input-width-medium">
                <form-input
                    :id="`lithologyDescriptor${index}`"
                    aria-label="Descriptor"
                    select
                    :options="codes.lithology_descriptors"
                    text-field="description"
                    value-field="lithology_description_code"
                    placeholder="Select descriptor"
                    v-model="lithologyData[index].lithology_description"
                    group-class="mt-1 mb-0"
                />
              </td>
              <td class="input-width-medium">
                <form-input
                    :id="`lithologyMoisture${index}`"
                    aria-label="Moisture"
                    select
                    :options="codes.lithology_moisture_codes"
                    text-field="description"
                    value-field="lithology_moisture_code"
                    placeholder="Select moisture"
                    v-model="lithologyData[index].lithology_moisture"
                    group-class="mt-1 mb-0"></form-input>
              </td>
              <td class="input-width-medium">
                <form-input
                    :id="`lithologyColour${index}`"
                    aria-label="Colour"
                    select
                    :options="codes.lithology_colours"
                    text-field="description"
                    placeholder="Select colour"
                    value-field="lithology_colour_code"
                    v-model="lithologyData[index].lithology_colour"
                    group-class="mt-1 mb-0"></form-input>
              </td>
              <td class="input-width-medium">
                <form-input
                    :id="`lithologyHardness${index}`"
                    aria-label="Hardness"
                    select
                    :options="codes.lithology_hardness_codes"
                    text-field="description"
                    placeholder="Select hardness"
                    value-field="lithology_hardness_code"
                    v-model="lithologyData[index].lithology_hardness"
                    group-class="mt-1 mb-0"></form-input>
              </td>
              <td class="input-width-medium">
                <form-input
                  :id="`lithologyFlowEstimate${index}`"
                  aria-label="Water bearing flow"
                  type="number"
                  v-model="lithologyData[index].water_bearing_estimated_flow"
                  group-class="mt-1 mb-0"
                ></form-input>
              </td>
              <td class="input-width-medium">
                <form-input
                    :id="`lithologyObservations${index}`"
                    aria-label="Observations"
                    v-model="lithologyData[index].lithology_observation"
                    group-class="mt-1 mb-0"></form-input>
              </td>
              <td class="pt-1">
                <b-btn size="sm" variant="primary" @click="removeRowIfOk(index)" :id="`removeRowButton${index}`" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" variant="primary" @click="addLithologyRow" id="addLithologyRowButton"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
    <b-modal
        v-model="confirmRemoveModal"
        centered
        title="Confirm remove"
        @shown="focusRemoveModal">
      Are you sure you want to remove this row?
      <div slot="modal-footer">
        <b-btn variant="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn">
          Cancel
        </b-btn>
        <b-btn variant="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)">
          Remove
        </b-btn>
      </div>
    </b-modal>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'

import Lithology from '@/submissions/components/lithology.js'
import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  name: 'Lithology',
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    lithology: {
      type: Array,
      default: () => ([])
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: String,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      lithSoils: [],
      lithologyData: []
    }
  },
  computed: {
    ...mapGetters(['codes']),
    computedLithology () {
      return [...this.lithologyData]
    }
  },
  watch: {
    computedLithology: {
      deep: true,
      handler: function (n, o) {
        const lithology = this.lithologyData.filter((d) => !this.lithologyIsEmpty(d))
        this.$emit('update:lithology', lithology)
      }
    }
  },
  methods: {
    addLithologyRow () {
      this.lithologyData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        lithology_raw_data: null,
        lithology_colour: null,
        lithology_hardness: null,
        lithology_moisture: null,
        lithology_observation: null,
        // lithology_description is a "descriptor" (containing an additional descriptive term like 'weathered', 'competent')
        lithology_description: null
      }
    },
    removeRowByIndex (index) {
      this.lithologyData.splice(index, 1)
      this.lithSoils.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.lithologyData[rowNumber])) {
        this.rowIndexToRemove = rowNumber
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(rowNumber)
      }
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      if (keys.length === 0) return false
      // Check that all fields are not empty.
      return !this.lithologyIsEmpty(row)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    parseDescription (index, value) {
      const lithology = new Lithology(value)
      this.lithSoils[index] = lithology.parseSoilTerms()
    },
    lithologyIsEmpty (lithology) {
      return Object.values(lithology).every((x) => !x)
    }
  },
  created () {
    // When component created, add an initial row of lithology.
    if (!this.lithology.length) {
      for (let i = 0; i < 10; i++) {
        this.addLithologyRow()
      }
    } else {
      this.lithology.forEach((lithology) => {
        this.lithologyData.push({ ...lithology })
      })
      this.addLithologyRow()
    }
  }
}
</script>

<style lang="scss">
.material-badges {
  font-size: 1.3rem;
}
</style>
