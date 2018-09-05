<template>
  <fieldset>
    <legend>Step 10: Filter Pack</legend>
    <b-row>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackFrom"
          label="Filter Pack From"
          hint="ft."
          type="text"
          v-model="filterPackFromInput"
        ></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackTo"
          label="Filter Pack To"
          hint="ft."
          type="text"
          v-model="filterPackToInput"
        ></form-input>
      </b-col>
      <b-col cols="12" md="6" lg="3">
        <form-input
          id="filterPackThickness"
          label="Filter Pack Thickness"
          hint="in."
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
  name: 'Step10FilterPack',
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
