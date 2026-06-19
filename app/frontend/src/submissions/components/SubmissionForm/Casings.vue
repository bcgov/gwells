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
  <form-subsection title="Casing Details" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
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
              <Checkbox
                v-model="casing.length_not_required"
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
                :disabled="casing.length_not_required"
                :errors="getCasingError(index).start"
                :loaded="getFieldsLoaded(index).start"/>
            </td>
            <td>
              <form-input
                group-class="mt-1 mb-0"
                :id="'casingTo_' + index"
                type="number"
                v-model="casing.end"
                :disabled="casing.length_not_required"
                :errors="getCasingError(index).end"
                :loaded="getFieldsLoaded(index).end"/>
            </td>
            <td>
              <div class="flex flex-col gap-2 mt-1 mb-0" :aria-describedby="`casingCodeInvalidFeedback${index}`">
                <Select
                  :id="'casingCode_' + index"
                  v-model="casing.casing_code"
                  :options="codes?.casing_codes"
                  optionValue="code"
                  optionLabel="description"
                  :invalid="getCasingError(index).casing_code ? true : false"
                  placeholder="Select a type"/>
                <div :id="`casingCodeInvalidFeedback${index}`">
                  <div v-for="(error, e_index) in getCasingError(index).casing_code" class="mt-1 text-sm text-red-600" :key="`Casing type input error ${e_index}`">
                    {{ error }}
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div class="flex flex-col gap-2 mt-1 mb-0" :aria-describedby="`casingMaterialInvalidFeedback${index}`">
                <Select
                  :id="'casingMaterial_' + index"
                  v-model="casing.casing_material"
                  :options="codes?.casing_materials"
                  optionValue="code"
                  optionLabel="description"
                  :invalid="getCasingError(index).casing_material ? true : false"
                  placeholder="Select a material"/>
                <div :id="`casingCodeInvalidFeedback${index}`">
                  <div v-for="(error, e_index) in getCasingError(index).casing_material" class="mt-1 text-sm text-red-600" :key="`Material input error ${e_index}`">
                    {{ error }}
                  </div>
                </div>
              </div>
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
              <Select
                :id="'casingDriveShoe_' + index"
                class="mt-1 mb-0"
                v-model="casing.drive_shoe_status"
                optionValue="drive_shoe_code"
                optionLabel="drive_shoe_code"
                :options="codes?.drive_shoe_codes"
                :loading="!fieldsLoaded['drive_shoe_status']"
                placeholder="Select drive shoe"/>
            </td>
            <td class="pt-1 py-0">
              <Button label="Remove" icon="fa fa-minus-square-o" size="small" :id="`removeCasingRowBtn${index}`" @click="removeRowIfOk(casing)" class="mt-2 float-right"/>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <Button label="Add row" icon="fa fa-plus-square-o" size="small" id="addCasingRowBtn" @click="addRow"/>
    <Dialog v-model:visible="confirmRemoveModal" modal header="Confirm remove" @show="focusRemoveModal">
      Are you sure you want to remove this row?
      <template #footer>
        <Button label="Cancel" severity="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn"/>
        <Button label="Remove" severity="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)"/>
      </template>
    </Dialog>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'
import { omit } from 'lodash'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  name: 'Casings',
  mixins: [inputBindingsMixin],
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
  components: {
    FormSubsection
  },
  data () {
    return {
      submissionStore: null,
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
        length_not_required: false
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
      instance.length_not_required = !instance.length_not_required
      this.casingsData[index] = instance
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
      this.$refs.cancelRemoveBtn.$el.focus()
    },
    casingIsEmpty (casing) {
      const fieldsToTest = omit(casing, 'length_not_required')
      return Object.values(fieldsToTest).every((x) => !x)
    }
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    },
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
    this.submissionStore = useSubmissionStore()
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
