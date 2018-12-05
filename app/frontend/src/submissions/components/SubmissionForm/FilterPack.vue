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
          <legend :id="id">Filter Pack</legend>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackFrom"
          label="Filter Pack From"
          hint="ft"
          type="text"
          v-model="filterPackFromInput"
        ></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackTo"
          label="Filter Pack To"
          hint="ft"
          type="text"
          v-model="filterPackToInput"
        ></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackThickness"
          label="Filter Pack Thickness"
          hint="inches"
          type="text"
          v-model="filterPackThicknessInput"
        ></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackMaterial"
          label="Filter Pack Material"
          select
          :options="codes.filter_pack_material"
          text-field="description"
          value-field="filter_pack_material_code"
          v-model="screenPackMaterialInput"
          placeholder="Select material"
          :errors="errors['filter_pack_material']"
          :loaded="fieldsLoaded['filter_pack_material']"
        ></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackMaterialSize"
          label="Filter Pack Material Size"
          select
          :options="codes.filter_pack_material_size"
          text-field="description"
          value-field="filter_pack_material_size"
          v-model="screenPackMaterialSizeInput"
          placeholder="Select size"
          :errors="errors['filter_pack_material_size']"
          :loaded="fieldsLoaded['filter_pack_material_size']"
        ></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'FilterPack',
  mixins: [inputBindingsMixin],
  props: {
    filterPackFrom: String,
    filterPackTo: String,
    filterPackThickness: String,
    screenPackMaterial: String,
    screenPackMaterialSize: String,
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
  fields: {
    filterPackFromInput: 'filterPackFrom',
    filterPackToInput: 'filterPackTo',
    filterPackThicknessInput: 'filterPackThickness',
    screenPackMaterialInput: 'screenPackMaterial',
    screenPackMaterialSizeInput: 'screenPackMaterialSize'
  },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
