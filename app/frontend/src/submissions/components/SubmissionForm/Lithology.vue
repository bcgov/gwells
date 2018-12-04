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
    <legend :id="id">Lithology</legend>
    <div class="table-responsive">
      <table class="table table-sm">
        <thead>
          <tr>
            <th class="font-weight-normal">
              <div>From</div><div>ft (bgl)</div>
            </th>
            <th class="font-weight-normal">
              <div>To</div><div>ft (bgl)</div>
            </th>
            <th class="font-weight-normal">
              Description
            </th>
            <th class="font-weight-normal">
              Materials
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
            <th></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(row, index) in lithology.length">
            <tr :key="`lithology row ${index}`" :id="`lithologyRow${index}`">
              <td class="input-width-small">
                <form-input :id="`lithologyDepthFrom${index}`" aria-label="Depth from (feet)" v-model="lithology[index].lithology_from" group-class="mt-1 mb-0"/>
              </td>
              <td class="input-width-small">
                <form-input :id="`lithologyDepthTo${index}`" aria-label="Depth to (feet)" v-model="lithology[index].lithology_to" group-class="mt-1 mb-0"/>
              </td>
              <td>
                <form-input
                    :id="`lithologyDescription${index}`"
                    aria-label="Description"
                    v-model="lithology[index].lithology_raw_data"
                    group-class="mt-1 mb-0"
                    @input="parseDescription(index, $event)"
                ></form-input>
              </td>
              <td>
                <div class="material-badges">
                  <b-badge v-for="(soil, j) in lithSoils[index]" variant="light" class="font-weight-normal" :key="`soilTerm-${index}-${j}`">
                    {{ soil }}
                  </b-badge>
                </div>
              </td>
              <td class="input-width-small">
                <!-- <form-input
                    :id="`lithologyMoisture${index}`"
                    aria-label="Moisture"
                    select
                    :options="codes.lithology_moisture_codes"
                    text-field="description"
                    value-field="lithology_moisture_code"
                    v-model="lithology[index].lithology_moisture"
                    group-class="mt-1 mb-0"></form-input> -->
                  <!-- <div class="material-badges">
                    <b-badge variant="light" class="font-weight-normal">Wet</b-badge>
                  </div> -->
              </td>
              <td>
                  <!-- <div class="material-badges">
                    <b-badge variant="light" class="font-weight-normal">Reddish-brown</b-badge>
                  </div> -->
              </td>
              <td>
                  <!-- <div class="material-badges">
                    <b-badge variant="light" class="font-weight-normal">Dense</b-badge>
                  </div> -->
              </td>
              <td>
                <form-input :id="`lithologyFlowEstimate${index}`" aria-label="Water bearing flow" v-model="lithology[index].water_bearing_estimated_flow" group-class="mt-1 mb-0"></form-input>
              </td>
              <td class="pt-1">
                <b-btn size="sm" variant="primary" @click="removeRowIfOk(index)" :id="`removeRowButton${index}`" class="mt-2"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
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

export default {
  name: 'Lithology',
  mixins: [inputBindingsMixin],
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
    }
  },
  data () {
    return {
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      lithSoils: []
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    addLithologyRow () {
      this.lithologyInput.push({})
    },
    removeRowByIndex (index) {
      this.lithologyInput.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.lithologyInput[rowNumber])) {
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
      return !keys.every((key) => !row[key])
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    parseDescription (index, value) {
      const soils = new Lithology(value)
      this.lithSoils[index] = soils.parseSoilTerms()
    }
  },
  created () {
    // When component created, add an initial row of lithology.
    if (!this.lithologyInput.length) {
      this.lithologyInput.push({}, {}, {})
    }
  }
}
</script>

<style lang="scss">
.material-badges {
  font-size: 1.3rem;
}
</style>
