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
          :options="codes.filter_pack_materials"
          text-field="description"
          value-field="filter_pack_material_code"
          placeholder="Select material"
          v-model="screenPackMaterialInput"
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
          placeholder="Select size"
          v-model="screenPackMaterialSizeInput"
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
  // The fields property helps to bind v-model (on the form input components) to a prop.
  // Set v-model to the key (see the form input above); the value corresponds to a prop declared on this component
  // Prop values will then be synced with the parent component. This way we can break apart a large form
  // into smaller components. Normally this is not necessary but we are composing a large POST request
  // out of many small components.
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
