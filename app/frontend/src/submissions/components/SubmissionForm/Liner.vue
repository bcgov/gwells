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
  <form-subsection title="Liner Information" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <responsive-grid :cols="12" :md="6">
      <form-input
        id="linerMaterial"
        label="Liner Material"
        select
        :options="codes?.liner_material_codes"
        v-model="linerMaterialInput"
        text-field="description"
        value-field="code"
        placeholder="Select material"
        :errors="errors['liner_material']"
        :loaded="fieldsLoaded['liner_material']"/>
    </responsive-grid>
    <responsive-grid :cols="6" :md="6">
      <form-input
        id="linerDiameter"
        label="Liner Diameter"
        hint="inches"
        type="number"
        v-model.number="linerDiameterInput"
        :errors="errors['liner_diameter']"
        :loaded="fieldsLoaded['liner_diameter']"/>
      <form-input
        id="linerThickness"
        label="Liner Thickness"
        hint="inches"
        type="number"
        v-model.number="linerThicknessInput"
        :errors="errors['liner_thickness']"
        :loaded="fieldsLoaded['liner_thickness']"/>
      <form-input
        id="linerFrom"
        label="Liner From"
        hint="ft (bgl)"
        type="number"
        v-model.number="linerFromInput"
        :errors="errors['liner_from']"
        :loaded="fieldsLoaded['liner_from']"/>
      <form-input
        id="linerTo"
        label="Liner To"
        hint="ft (bgl)"
        type="number"
        v-model.number="linerToInput"
        :errors="errors['liner_to']"
        :loaded="fieldsLoaded['liner_to']"/>
    </responsive-grid>
    <div class="flex">>Liner Perforations</div>
    <div class="grid grid-cols-2">
      <div class="md:col-span-1">
        <table class="table table-sm no-border">
          <thead>
            <tr>
              <th class="font-weight-normal no-border">Perforated From ft (bgl)</th>
              <th class="font-weight-normal">Perforated To ft (bgl)</th>
              <th></th>
            </tr>
            <tr v-for="(liner, index) in linerPerforationsData" :key="index">
              <td class="pb-0 pt-1">
                <form-input
                  :id="`liner_perforated_from_${index}`"
                  type="number"
                  class="mb-0"
                  v-model="liner.start"
                  :errors="getLinerPerforationError(index).start"
                  :loaded="getFieldsLoaded(index).start"/>
              </td>
              <td class="pb-0 pt-1">
                <form-input
                  :id="`liner_perforated_to_${index}`"
                  type="number"
                  class="mb-0"
                  v-model="liner.end"
                  :errors="getLinerPerforationError(index).end"
                  :loaded="getFieldsLoaded(index).end"/>
              </td>
              <td class="py-0">
                <Button label="Remove" icon="fa fa-minus-square-o" size="small" :id="`removeLinerPerfRowBtn${index}`" @click="removeRowIfOk(index)" class="mt-2"/>
              </td>
            </tr>
          </thead>
          <tbody>
          </tbody>
        </table>
        <Button label="Add row" icon="fa fa-plus-square-o" size="small" id="addlinerPerforationRowBtn" @click="addRow"/>
        <Dialog v-model:visible="confirmRemoveModal" modal header="Confirm remove" @show="focusRemoveModal">
          Are you sure you want to remove this row?
          <template #footer>
            <Button label="Cancel" severity="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn"/>
            <Button label="Remove" severity="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)"/>
          </template>
        </Dialog>
      </div>
    </div>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  name: 'LinerInformation',
  mixins: [inputBindingsMixin],
  props: {
    linerMaterial: String,
    linerDiameter: null,
    linerThickness: null,
    linerFrom: null,
    linerTo: null,
    linerPerforations: Array,
    errors: {
      type: Object,
      default: () => ({}),
      isInput: true
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({}),
      isInput: true
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
    FormSubsection,
    ResponsiveGrid
  },
  data () {
    return {
      submissionStore: null,
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      linerPerforationsData: []
    }
  },
  methods: {
    emptyObject () {
      return {
        start: null,
        end: null
      }
    },
    getLinerPerforationError (index) {
      if (this.errors && 'linerperforation_set' in this.errors && index in this.errors['linerperforation_set']) {
        return this.errors['linerperforation_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'linerperforation_set' in this.fieldsLoaded && index in this.fieldsLoaded['linerperforation_set']) {
        return this.fieldsLoaded['linerperforation_set'][index]
      }
      return {}
    },
    addRow () {
      this.linerPerforationsData.push(this.emptyObject())
    },
    removeRowByIndex (index) {
      this.linerPerforationsData.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.linerPerforationsData[rowNumber])) {
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
      return !this.linerIsEmpty(row)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.$el.focus()
    },
    linerIsEmpty (liner) {
      return Object.values(liner).every((x) => !x)
    }
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    },
    computedLinerPerforations () {
      return [...this.linerPerforationsData]
    }
  },
  watch: {
    computedLinerPerforations: {
      deep: true,
      handler: function (n, o) {
        const perforations = this.linerPerforationsData.filter((d) => !this.linerIsEmpty(d))
        this.$emit('update:linerPerforations', perforations)
      }
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
    // When component created, add an initial row of lithology.
    if (!this.linerPerforations.length) {
      for (let i = 0; i < 3; i++) {
        this.addRow()
      }
    } else {
      this.linerPerforations.forEach((liner) => {
        this.linerPerforationsData.push({ ...liner })
      })
      this.addRow()
    }
  }
}
</script>
<style lang="scss" scoped>
%no-border {
  border: 0px;
  border-bottom: 0px;
  border-top: 0px;
}

.no-border {
  th {
    @extend %no-border;
  }
  td {
    @extend %no-border;
  }
}
</style>
