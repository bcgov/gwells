<template>
  <fieldset>
    <legend>Screen Information</legend>
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
          v-model="screenIntakeInput"></form-input>
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
                <form-input group-class="my-1" :id="`screen${index}DepthFrom`" aria-label="Depth from (feet)" v-model="screens[index].start"/>
              </td>
              <td class="input-width-small py-0">
                <form-input group-class="my-1" :id="`screen${index}DepthTo`" aria-label="Depth to (feet)" v-model="screens[index].end"/>
              </td>
              <td class="input-width-small py-0">
                <form-input group-class="my-1" :id="`screen${index}Diameter`" aria-label="Diameter (inches)" v-model="screens[index].internal_diameter"/>
              </td>
              <td class="input-width-small py-0">
                <form-input
                    group-class="my-1"
                    :id="`screen${index}Assembly`"
                    aria-label="Screen Assembly Type"
                    v-model="screens[index].assembly_type"
                    select
                    :options="codes.screen_assemblies"
                    text-field="description"
                    value-field="screen_assembly_type_code"
                    placeholder="Select type"/>
              </td>
              <td class="input-width-small py-0">
                <form-input list="screenSlotSizeList" group-class="my-1" :id="`screen${index}SlotSize`" aria-label="Screen Slot Size" v-model="screens[index].slot_size"/>
              </td>
              <td class="align-middle py-0">
                <b-btn size="sm" variant="primary" @click="removeRowIfOk(index)" :id="`removeScreenRowButton${index}`"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
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
      default: () => ([{}])
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
  // The fields property helps to bind v-model (on the form input components) to a prop.
  // Set v-model to the key (see the form input above); the value corresponds to a prop declared on this component
  // Prop values will then be synced with the parent component. This way we can break apart a large form
  // into smaller components. Normally this is not necessary but we are composing a large POST request
  // out of many small components.
  fields: {
    screenIntakeInput: 'screenIntakeMethod',
    screenTypeInput: 'screenType',
    screenMaterialInput: 'screenMaterial',
    otherScreenMaterialInput: 'otherScreenMaterial',
    screenOpeningInput: 'screenOpening',
    screenBottomInput: 'screenBottom',
    screensInput: 'screens'
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
      this.screensInput.push({
        start: '',
        end: '',
        internal_diameter: '',
        assembly_type: '',
        slot_size: ''
      })
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
    if (!this.screens.length) {
      this.addScreenRow()
    }
  }
}
</script>

<style>

</style>
