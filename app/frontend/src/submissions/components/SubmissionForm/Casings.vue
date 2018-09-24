<template>
  <fieldset>
    <legend>Casing Details</legend>
    <div class="table-responsive">
      <table class="table table-sm">
        <thead>
          <tr>
            <th class="font-weight-normal">From ft (bgl)</th>
            <th class="font-weight-normal">To ft (bgl)</th>
            <th class="font-weight-normal">Casing Type</th>
            <th class="font-weight-normal">Casing Material</th>
            <th class="font-weight-normal">Diameter (in)</th>
            <th class="font-weight-normal">Wall Thickness (in)</th>
            <th class="font-weight-normal">Drive Shoe</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(casing, index) in casingsInput" :key="casing.id">
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'casing_from_' + index"
                type="number"
                v-model="casing.start"
                :errors="getCasingError(index).start"
                :loaded="getFieldsLoaded(index).start"/>
            </td>
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'casing_to_' + index"
                type="number"
                v-model="casing.end"
                :errors="getCasingError(index).end"
                :loaded="getFieldsLoaded(index).end"/>
            </td>
            <td class="pb-0">
              <b-form-group
                id="'casingCode_' + index"
                class="my-0"
                aria-describedby="casingCodeInvalidFeedback{index}">
                <b-form-select
                    v-model="casing.casing_code"
                    :options="codes.casing_codes"
                    value-field="code"
                    text-field="description"
                    :state="getCasingError(index).casing_code ? false : null">
                  <template slot="first">
                    <option :value="null" disabled>Select a type</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback id="casingCodeInvalidFeedback{index}">
                  <div v-for="(error, error_index) in getCasingError(index).casing_code" :key="`Casing type input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td class="pb-0">
              <b-form-group
                :id="'casingMaterial_' + index"
                class="my-0"
                aria-describedby="casingMaterialInvalidFeedback{index}">
                <b-form-select
                    v-model="casing.casing_material"
                    :options="codes.casing_materials"
                    value-field="code"
                    text-field="description"
                    :state="getCasingError(index).casing_material ? false : null">
                  <template slot="first">
                    <option :value="null" disabled>Select a material</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback id="casingCodeInvalidFeedback{index}">
                  <div v-for="(error, error_index) in getCasingError(index).casing_material" :key="`Material input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'diameter_' + index"
                type="number"
                v-model="casing.diameter"
                :errors="getCasingError(index).diameter"
                :loaded="getFieldsLoaded(index).diameter"/>
            </td>
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'wall_thickness_' + index"
                type="number"
                v-model="casing.wall_thickness"
                :errors="getCasingError(index).wall_thickness"
                :loaded="getFieldsLoaded(index).wall_thickness"/>
            </td>
            <td class="pt-0 py-0">
              <b-form-radio-group v-model="casing.drive_shoe"
                                  :name="'drive_shoe_' + index">
                <b-form-radio value="False">No</b-form-radio>
                <b-form-radio value="True">Yes</b-form-radio>
              </b-form-radio-group>
            </td>
            <td class="align-middle pt-1 py-0">
              <b-btn size="sm" variant="primary" @click="removeRow(casing.id)"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'Casings',
  mixins: [inputBindingsMixin],
  props: {
    casings: {
      type: Array,
      default: () => []
    },
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
    casingsInput: 'casings'
  },
  methods: {
    calcNextId () {
      return this.casings.reduce((accumulator, currentValue) => {
        return accumulator <= currentValue.id ? currentValue.id + 1 : accumulator
      }, 0)
    },
    addRow () {
      this.casings.push({id: this.calcNextId()})
    },
    removeRow (id) {
      this.casings.splice(this.casings.findIndex(item => item.id === id), 1)
    },
    getCasingError (index) {
      if (this.errors && 'casings' in this.errors && index in this.errors['casings']) {
        return this.errors['casings'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'casings' in this.fieldsLoaded && index in this.fieldsLoaded['casings']) {
        return this.fieldsLoaded['casings'][index]
      }
      return {}
    }
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
