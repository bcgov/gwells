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
    <legend :id="id">Screen Information</legend>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
          id="screenIntake"
          label="Intake"
          select
          :options="codes.screen_intake_methods"
          text-field="description"
          value-field="screen_intake_code"
          placeholder="Select intake"
          v-model="screenIntakeMethodInput"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
          id="screenType"
          label="Screen Type"
          select
          :options="codes.screen_types"
          text-field="description"
          value-field="screen_type_code"
          placeholder="Select type"
          v-model="screenTypeInput"></form-input>
      </b-col>
      <b-col cols="12" md="4" lg="3">
        <form-input
          id="screenMaterial"
          label="Screen Material"
          select
          :options="codes.screen_materials"
          text-field="description"
          value-field="screen_material_code"
          placeholder="Select material"
          v-model="screenMaterialInput"></form-input>
      </b-col>
      <b-col cols="12" md="4" lg="3">
        <form-input
          id="otherScreenMaterial"
          label="Specify Other Screen Material"
          v-model="otherScreenMaterialInput"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
          id="screenOpening"
          label="Screen Opening"
          select
          :options="codes.screen_openings"
          text-field="description"
          value-field="screen_opening_code"
          placeholder="Select opening"
          v-model="screenOpeningInput"></form-input>
      </b-col>
      <b-col cols="12" md="4" lg="3">
        <form-input
          id="screenBottom"
          label="Screen Bottom"
          select
          :options="codes.screen_bottoms"
          text-field="description"
          value-field="screen_bottom_code"
          placeholder="Select bottom"
          v-model="screenBottomInput"></form-input>
      </b-col>
    </b-row>
    <p class="mt-3 mb-2">Screen Details</p>
    <div class="table-responsive">
      <table class="table table-sm">
        <thead>
          <th class="font-weight-normal">
            <div>From ft (bgl)</div>
          </th>
          <th class="font-weight-normal">
            <div>To ft (bgl)</div>
          </th>
          <th class="font-weight-normal">
            Diameter (in)
          </th>
          <th class="font-weight-normal">
            Screen Assembly Type
          </th>
          <th class="font-weight-normal">
            Slot Size
          </th>
          <th>
          </th>
        </thead>
        <tbody>
          <template v-for="(row, index) in screens.length">
            <tr :key="`screen row ${index}`" :id="`screenRow${index}`">
              <td class="input-width-small py-0">
                <form-input
                  group-class="my-1"
                  :id="`screenDepthFrom_${index}`"
                  aria-label="Depth from (feet)"
                  v-model="screens[index].start"
                  :errors="getScreenError(index).start"
                  :loaded="getScreenLoaded(index).start"
                  />
              </td>
              <td class="input-width-small py-0">
                <form-input
                  group-class="my-1"
                  :id="`screenDepthTo_${index}`"
                  aria-label="Depth to (feet)"
                  v-model="screens[index].end"
                  :errors="getScreenError(index).end"
                  :loaded="getScreenLoaded(index).end"
                  />
              </td>
              <td class="input-width-small py-0">
                <form-input
                  group-class="my-1"
                  :id="`screenDiameter_${index}`"
                  aria-label="Diameter (inches)"
                  v-model="screens[index].internal_diameter"
                  :errors="getScreenError(index).internal_diameter"
                  :loaded="getScreenLoaded(index).internal_diameter"
                  />
              </td>
              <td class="input-width-small py-0">
                <form-input
                    group-class="my-1"
                    :id="`screenAssemblyType_${index}`"
                    aria-label="Screen Assembly Type"
                    v-model="screens[index].assembly_type"
                    select
                    :options="codes.screen_assemblies"
                    text-field="description"
                    value-field="screen_assembly_type_code"
                    placeholder="Select type"
                    :errors="getScreenError(index).assembly_type"
                    :loaded="getScreenLoaded(index).assembly_type"
                    />
              </td>
              <td class="input-width-small py-0">
                <form-input
                  list="screenSlotSizeList"
                  group-class="my-1"
                  :id="`screenSlotSize_${index}`"
                  aria-label="Screen Slot Size"
                  v-model="screens[index].slot_size"
                  :errors="getScreenError(index).slot_size"
                  :loaded="getScreenLoaded(index).slot_size"
                  />
              </td>
              <td class="py-0">
                <b-btn size="sm" variant="primary" @click="removeRowIfOk(index)" :id="`removeScreenRowButton${index}`" class="mt-2"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <datalist id="screenSlotSizeList">
      <option v-for="size in screenSlotSizeSuggestions" :key="`screenSlotSizeListOption-${size}`">{{size}}</option>
    </datalist>
    <b-btn size="sm" variant="primary" @click="addScreenRow" id="addScreenRowButton"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
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
    screenIntakeMethod: String,
    screenType: String,
    screenMaterial: String,
    otherScreenMaterial: String,
    screenOpening: String,
    screenBottom: String,
    screens: {
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
      screenSlotSizeSuggestions: ['10', '20', '40', '80'],
      confirmRemoveModal: false,
      rowIndexToRemove: null
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    addScreenRow () {
      this.screensInput.push({})
    },
    removeRowByIndex (index) {
      this.screensInput.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.screensInput[rowNumber])) {
        this.rowIndexToRemove = rowNumber
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(rowNumber)
      }
    },
    getScreenError (index) {
      if (this.errors && 'screen_set' in this.errors && index in this.errors['screen_set']) {
        return this.errors['screen_set'][index]
      }
      return {}
    },
    getScreenLoaded (index) {
      if (this.fieldsLoaded && 'screen_set' in this.fieldsLoaded && index in this.fieldsLoaded['screen_set']) {
        return this.fieldsLoaded['screen_set'][index]
      }
      return {}
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
    // when component created, add an initial row of screens
    if (!this.screensInput.length) {
      this.screensInput.push({}, {}, {})
    }
  }
}
</script>

<style>

</style>
