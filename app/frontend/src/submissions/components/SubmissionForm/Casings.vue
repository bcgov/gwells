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
        <legend :id="id">Casing Details</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive" id="casingTable">
      <table class="table table-sm" aria-describedby="casingsDetails">
        <thead>
          <tr>
            <th class="font-weight-normal">Unknown Length</th>
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
          <tr v-for="(casing, index) in casingsData" :key="casing.id">
            <td>
              <b-form-checkbox
                :checked="!casing.length_required"
                inline
                class="mr-0 mt-2"
                @change="toggleCasingLengthRequired(index)"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'casingFrom_' + index"
                type="number"
                v-model="casing.start"
                :disabled="!casing.length_required"
                :errors="getCasingError(index).start"
                :loaded="getFieldsLoaded(index).start"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'casingTo_' + index"
                type="number"
                v-model="casing.end"
                :disabled="!casing.length_required"
                :errors="getCasingError(index).end"
                :loaded="getFieldsLoaded(index).end"/>
            </td>
            <td>
              <b-form-group
                :id="'casingCode_' + index"
                class="mt-1 mb-0"
                :aria-describedby="`casingCodeInvalidFeedback${index}`">
                <b-form-select
                    v-model="casing.casing_code"
                    :options="codes.casing_codes"
                    value-field="code"
                    text-field="description"
                    :state="getCasingError(index).casing_code ? false : null">
                  <template slot="first">
                    <option :value="null">Select a type</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback :id="`casingCodeInvalidFeedback${index}`">
                  <div v-for="(error, error_index) in getCasingError(index).casing_code" :key="`Casing type input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td>
              <b-form-group
                :id="'casingMaterial_' + index"
                class="mt-1 mb-0"
                :aria-describedby="`casingMaterialInvalidFeedback${index}`">
                <b-form-select
                    v-model="casing.casing_material"
                    :options="codes.casing_materials"
                    value-field="code"
                    text-field="description"
                    :state="getCasingError(index).casing_material ? false : null">
                  <template slot="first">
                    <option :value="null" enabled>Select a material</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback :id="`casingCodeInvalidFeedback${index}`">
                  <div v-for="(error, error_index) in getCasingError(index).casing_material" :key="`Material input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'casingDiameter_' + index"
                type="number"
                v-model="casing.diameter"
                :errors="getCasingError(index).diameter"
                :loaded="getFieldsLoaded(index).diameter"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'casingWallThickness_' + index"
                type="number"
                v-model="casing.wall_thickness"
                :errors="getCasingError(index).wall_thickness"
                :loaded="getFieldsLoaded(index).wall_thickness"/>
            </td>
            <td>
              <b-form-group :id="'casingDriveShoe_' + index" class="mt-1 mb-0">
                <b-form-select
                  v-model="casing.drive_shoe_status"
                  value-field="drive_shoe_code"
                  text-field="drive_shoe_code"
                  :options="codes.drive_shoe_codes"
                  :errors="errors['drive_shoe_status']"
                  :loaded="fieldsLoaded['drive_shoe_status']">
                  <template slot="first">
                    <option :value="null" enabled>Select drive shoe</option>
                  </template>
                </b-form-select>
              </b-form-group>
            </td>
            <td class="pt-1 py-0">
              <b-btn size="sm" variant="primary" :id="`removeCasingRowBtn${index}`" @click="removeRowIfOk(casing)" class="mt-2 float-right"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" id="addCasingRowBtn" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
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
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { omit } from 'lodash'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  name: 'Casings',
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    casings: Array,
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
      casingsData: []
    }
  },
  methods: {
    addRow () {
      this.casingsData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        start: null,
        end: null,
        casing_code: null,
        casing_material: null,
        drive_shoe_status: null,
        length_required: true
      }
    },
    removeRowByIndex (index) {
      this.casingsData.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (instance) {
      const index = this.casingsData.findIndex(item => item === instance)
      if (this.rowHasValues(this.casingsData[index])) {
        this.rowIndexToRemove = index
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(index)
      }
    },
    toggleCasingLengthRequired (index) {
      const instance = this.casingsData[index]
      instance.length_required = !instance.length_required
      Vue.set(this.casingsData, index, instance)
    },
    getCasingError (index) {
      if (this.errors && 'casing_set' in this.errors && index in this.errors['casing_set']) {
        return this.errors['casing_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'casing_set' in this.fieldsLoaded && index in this.fieldsLoaded['casing_set']) {
        return this.fieldsLoaded['casing_set'][index]
      }
      return {}
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      if (keys.length === 0) return false
      // Check that all fields are not empty.
      return !this.casingIsEmpty(row)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    casingIsEmpty (casing) {
      const fieldsToTest = omit(casing, 'length_required')
      return Object.values(fieldsToTest).every((x) => !x)
    }
  },
  computed: {
    ...mapGetters(['codes']),
    computedCasings () {
      return [...this.casingsData]
    }
  },
  watch: {
    computedCasings: {
      deep: true,
      handler: function (n, o) {
        const casings = this.casingsData.filter((d) => !this.casingIsEmpty(d))
        this.$emit('update:casings', casings)
      }
    }
  },
  created () {
    // When component created, add an initial row of casings.
    if (!this.casings.length) {
      for (let i = 0; i < 3; i++) {
        this.addRow()
      }
    } else {
      this.casings.forEach((casing) => {
        this.casingsData.push({ ...casing })
      })
      this.addRow()
    }
  }
}
</script>

<style>

</style>
