<template>
  <fieldset>
    <legend>Well Yield Estimation</legend>
    <div v-for="(data, index) in productionData" :key="`productionDataSet${index}`">
      <b-row>
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
              id="staticWaterLevel"
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
              <b-form-radio value="No">No</b-form-radio>
              <b-form-radio value="Yes">Yes</b-form-radio>
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
    </div>
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
    hydroFracturingPerformed: String,
    hydroFracturingYieldIncrease: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    productionDataInput: 'productionData'
  },
  data () {
    return {}
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
