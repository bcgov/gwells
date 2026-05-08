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
  <form-subsection title="Filter Pack" :id="id" :isStaffEdit="isStaffEdit" :saveDisabled="saveDisabled">
    <div class="grid grid-cols-12">
      <div class="col-span-12 md:col-span-6 lg:col-span-3">
        <form-input
          id="filterPackFrom"
          label="Filter Pack From"
          hint="ft"
          type="number"
          v-model="filterPackFromInput"
        ></form-input>
      </div>
      <div class="col-span-12 md:col-span-6 lg:col-span-3">
        <form-input
          id="filterPackTo"
          label="Filter Pack To"
          hint="ft"
          type="number"
          v-model="filterPackToInput"
        ></form-input>
      </div>
      <div class="col-span-12 md:col-span-6 lg:col-span-3">
        <form-input
          id="filterPackThickness"
          label="Filter Pack Thickness"
          hint="inches"
          type="number"
          v-model="filterPackThicknessInput"
        ></form-input>
      </div>
    </div>
    <div class="grid grid-cols-12">
      <div class="col-span-12 md:col-span-6 lg:col-span-3">
        <form-input
          id="filterPackMaterial"
          label="Filter Pack Material"
          select
          :options="codes?.filter_pack_material"
          text-field="description"
          value-field="filter_pack_material_code"
          v-model="filterPackMaterialInput"
          placeholder="Select material"
          :errors="errors['filter_pack_material']"
          :loaded="fieldsLoaded['filter_pack_material']"
        ></form-input>
      </div>
      <div class="col-span-12 md:col-span-6 lg:col-span-3">
        <form-input
          id="filterPackMaterialSize"
          label="Filter Pack Material Size"
          select
          :options="codes?.filter_pack_material_size"
          text-field="description"
          value-field="filter_pack_material_size_code"
          v-model="filterPackMaterialSizeInput"
          placeholder="Select size"
          :errors="errors['filter_pack_material_size']"
          :loaded="fieldsLoaded['filter_pack_material_size']"
        ></form-input>
      </div>
    </div>
  </form-subsection>
</template>

<script>
import { useSubmissionStore } from '@/stores/submission'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import FormSubsection from '../FormSubcomponents/FormSubsection.vue'

export default {
  name: 'FilterPack',
  mixins: [inputBindingsMixin],
  props: {
    filterPackFrom: String,
    filterPackTo: String,
    filterPackThickness: String,
    filterPackMaterial: String,
    filterPackMaterialSize: String,
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
  fields: {
    filterPackFromInput: 'filterPackFrom',
    filterPackToInput: 'filterPackTo',
    filterPackThicknessInput: 'filterPackThickness',
    filterPackMaterialInput: 'filterPackMaterial',
    filterPackMaterialSizeInput: 'filterPackMaterialSize'
  },
  data () {
    return {
      submissionStore: null
    }
  },
  created () {
    this.submissionStore = useSubmissionStore()
  },
  computed: {
    codes () {
      return this.submissionStore.codes
    }
  }
}
</script>

<style>

</style>
