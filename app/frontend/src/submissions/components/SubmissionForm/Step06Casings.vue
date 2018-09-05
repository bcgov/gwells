<template>
  <fieldset>
    <legend>Step 6: Casing Details</legend>
    <table class="table table-sm">
      <thead>
        <tr>
          <th>From ft (bgl)</th>
          <th>To ft (bgl)</th>
          <th>Casing Type</th>
          <th>Casing Material</th>
          <th>Diameter (in)</th>
          <th>Wall Thickness (in)</th>
          <th>Drive Shoe</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(casing, index) in casings" :key="casing.id">
          <td>
            <form-input
              group-class="my-1"
              :id="'casing_from' + index"
              type="number"
              v-model="casing.casing_from"
              :errors="getCasingError(index).casing_from"
              :loaded="getFieldsLoaded(index).casing_from"/>
          </td>
          <td>
            <form-input
              group-class="my-1"
              :id="'casing_to_' + index"
              type="number"
              v-model="casing.casing_to"
              :errors="getCasingError(index).casing_to"
              :loaded="getFieldsLoaded(index).casing_to"/>
          </td>
          <td>
            <b-form-group
              id="'casingCode_' + index"
              class="my-1"
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
          <td>
            <b-form-group
              :id="'casingMaterial_' + index"
              class="my-1"
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
          <td>
            <form-input
              group-class="my-1"
              :id="'diameter_' + index"
              type="number"
              v-model="casing.diameter"
              :errors="getCasingError(index).diameter"
              :loaded="getFieldsLoaded(index).diameter"/>
          </td>
          <td>
            <form-input
              group-class="my-1"
              :id="'wall_thickness_' + index"
              type="number"
              v-model="casing.wall_thickness"
              :errors="getCasingError(index).wall_thickness"
              :loaded="getFieldsLoaded(index).wall_thickness"/>
          </td>
          <td>
            <b-form-radio-group v-model="casing.drive_shoe"
                                :name="'drive_shoe_' + index">
              <b-form-radio value="False">No</b-form-radio>
              <b-form-radio value="True">Yes</b-form-radio>
            </b-form-radio-group>
          </td>
          <td>
            <a href="#" v-on:click.prevent="removeRow(casing.id)">remove</a>
          </td>
        </tr>
      </tbody>
    </table>
    <a href="#" v-on:click.prevent="addRow">add another row</a>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'Step06Casings',
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
