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
  <fieldset :id="id">
      <b-row>
        <b-col cols="12" lg="6">
          <legend :id="id">Yield</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
    <b-card class="mt-2" v-for="(data, index) in productionData" :key="`productionDataSet${index}`">
      <b-row>
        <b-col>
          <h5 class="card-title">Production data set {{index + 1}}
            <b-btn size="sm" :id="`removeProductionDataBtn${index}`" variant="primary" @click="removeRowIfOk(index)" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
          </h5>
        </b-col>
      </b-row>
      <b-row class="mt-3">
        <b-col cols="12" md="4" lg="3">
          <form-input
              id="yieldEstimationMethod"
              label="Yield Estimation Method"
              select
              :options="codes.yield_estimation_methods"
              text-field="description"
              value-field="yield_estimation_method_code"
              v-model="productionData[index].yield_estimation_method"
              placeholder="Select method"></form-input>
        </b-col>
        <b-col cols="12" md="4" lg="2">
          <form-input
              id="yieldEstimationRate"
              label="Yield Estimation Rate"
              hint="USgpm"
              v-model="productionData[index].yield_estimation_rate"></form-input>
        </b-col>
        <b-col cols="12" md="4" lg="2">
          <form-input
              id="yieldEstimationDuration"
              label="Yield Estimation Duration"
              hint="Hours"
              v-model="productionData[index].yield_estimation_duration"></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="4" lg="2">
          <form-input
              id="staticWaterLevelTest"
              label="SWL Before Test"
              v-model="productionData[index].static_level"
              hint="ft (btoc)"></form-input>
        </b-col>
        <b-col cols="12" md="4" lg="2" offset-md="1">
          <form-input
              id="drawdown"
              label="Drawdown"
              v-model="productionData[index].drawdown"
              hint="ft (btoc)"
              ></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="4" lg="2">
          <b-form-group label="Hydro-fracturing Performed">
            <b-form-radio-group id="hydroFracPerformedOptions" v-model="productionData[index].hydro_fracturing_performed" name="hydroFracturingPerformed" class="mt-2">
              <b-form-radio :value="false">No</b-form-radio>
              <b-form-radio :value="true">Yes</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="4" lg="4" offset-md="1">
          <form-input
              id="hydroFracturingYieldIncrease"
              label="Increase in Well Yield Due to Hydro-fracturing"
              v-model="productionData[index].hydro_fracturing_yield_increase"
              hint="USgpm"
              ></form-input>
        </b-col>
      </b-row>
    </b-card>
    <b-btn size="sm" variant="primary" id="addlinerPerforationRowBtn" @click="addRow" class="mt-3"><i class="fa fa-plus-square-o"></i> Add production data</b-btn>
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
export default {
  mixins: [inputBindingsMixin],
  props: {
    productionData: {
      type: Array,
      default: () => ([])
    },
    yieldEstimationMethod: String,
    yieldEstimationRate: String,
    yieldEstimationDuration: String,
    staticLevel: String,
    drawdown: String,
    hydroFracturingPerformed: null,
    hydroFracturingYieldIncrease: String,
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
  fields: {
    productionDataInput: 'productionData'
  },
  data () {
    return {
      confirmRemoveModal: false
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    addProductionData () {
      const blankData = {
        yield_estimation_method: '',
        yield_estimation_rate: '',
        yield_estimation_duration: '',
        static_level: '',
        drawdown: '',
        hydro_fracturing_performed: '',
        hydro_fracturing_yield_increase: ''
      }
      this.productionDataInput.push(blankData)
    },
    addRow () {
      this.addProductionData()
    },
    removeRowByIndex (index) {
      this.productionDataInput.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.productionDataInput[rowNumber])) {
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
    }
  },
  created () {
    if (this.productionData.length === 0) {
      this.addProductionData()
    }
  }
}
</script>

<style>

</style>
