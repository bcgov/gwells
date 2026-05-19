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
  <form-subsection
    title="Decommission Description"
    subtitle="Enter depth intervals from the top of the hole to the bottom."
    :id="id" :isStaffEdit="isStaffEdit"
    :saveDisabled="saveDisabled">
    <div class="grid grid-cols-12">
      <div class="col-span-12">
        <div class="table-responsive">
          <table class="table table-sm" aria-describedby="decommissionDescriptions">
            <thead>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Decommission Material</th>
                <th>Observations</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(item, index) in closureDescriptionSetData"
                :key="`closureDescription${index}`"
                :id="`closureDescription${index}`">
                <td class="input-width-small">
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="`closureFrom${index}`"
                    type="number"
                    v-model="item.start"
                    :errors="getClosureError(index).start"
                    :loaded="getFieldsLoaded(index).start"/>
                </td>
                <td class="input-width-small">
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="`closureTo${index}`"
                    v-model="item.end"
                    type="number"
                    :errors="getClosureError(index).end"
                    :loaded="getFieldsLoaded(index).end"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    select
                    :id="`decommissionMaterial${index}`"
                    :options="codes?.decommission_materials"
                    text-field="description"
                    value-field="code"
                    placeholder="Select material"
                    value="Select material"
                    v-model="item.material"
                    :errors="getClosureError(index).material"
                    :loaded="getFieldsLoaded(index).material"/>
                </td>
                <td>
                  <form-input
                    group-class="mt-1 mb-0"
                    :id="`closureObservations${index}`"
                    v-model="item.observations"
                    :errors="getClosureError(index).observations"
                    :loaded="getFieldsLoaded(index).observations"/>
                </td>
                <td class="pt-1 py-0">
                  <Button label="Remove" icon="fa fa-minus-square-o" size="small" :id="`removeClosureDescriptionRowBtn${index}`" @click="removeRowIfOk(item)" class="mt-2 float-right"/>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <Button label="Add row" icon="fa fa-plus-square-o" size="small" @click="addClosureRow" id="addClosureRowButton"/>
      </div>
    </div>
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

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  mixins: [inputBindingsMixin],
  props: {
    closureDescriptionSet: {
      type: Array,
      default: () => ([])
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: Object,
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
      closureDescriptionSetData: [],
      rowIndexToRemove: null
    }
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    },
    computedClosureDescriptionSet () {
      return [...this.closureDescriptionSetData]
    }
  },
  watch: {
    computedClosureDescriptionSet: {
      deep: true,
      handler: function (n, o) {
        const closures = this.closureDescriptionSetData
          .filter((d) => !this.closureDescriptionIsEmpty(d))
        this.$emit('update:closureDescriptionSet', closures)
      }
    }
  },
  methods: {
    addClosureRow () {
      this.closureDescriptionSetData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        start: null,
        end: null,
        material: null,
        observations: ''
      }
    },
    removeRowByIndex (rowNumber) {
      this.closureDescriptionSetData.splice(rowNumber, 1)
    },
    removeRowIfOk (instance) {
      const index = this.closureDescriptionSetData.findIndex(item => item === instance)
      if (this.rowHasValues(this.closureDescriptionSetData[index])) {
        this.rowIndexToRemove = index
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(index)
      }
    },
    getClosureError (index) {
      if (this.errors && 'decommission_description_set' in this.errors && index in this.errors['decommission_description_set']) {
        return this.errors['decommission_description_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'decommission_description_set' in this.fieldsLoaded && index in this.fieldsLoaded['decommission_description_set']) {
        return this.fieldsLoaded['decommission_description_set'][index]
      }
      return {}
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      if (keys.length === 0) return false
      // Check that all fields are not empty.
      return !this.closureDescriptionIsEmpty(row)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    closureDescriptionIsEmpty (closureDescription) {
      return Object.values(closureDescription).every((x) => !x)
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
    if (!this.closureDescriptionSet.length) {
      for (let i = 0; i < 10; i++) {
        this.addClosureRow()
      }
    } else {
      this.closureDescriptionSet.forEach((closureDescription) => {
        this.closureDescriptionSetData.push({ ...closureDescription })
      })
      this.addClosureRow()
    }
  }
}
</script>

<style>

</style>
