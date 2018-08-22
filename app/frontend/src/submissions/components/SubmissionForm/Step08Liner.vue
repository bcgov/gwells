<template>
  <fieldset>
    <legend>Step 8: Liner Information</legend>
    <b-row>
        <b-col cols="12" md="6">
          <form-input
            id="linerMaterial"
            label="Liner Material"
            select
            :options="codes.liner_material_codes"
            v-model="linerMaterialInput"
            text-field="description"
            value-field="code"
            :errors="errors['liner_material']"
            :loaded="fieldsLoaded['liner_material']"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="6" md="6">
          <form-input
            id="linerDiameter"
            label="Liner Diameter"
            hint="inches"
            type="number"
            v-model.number="linerDiameterInput"
            :errors="errors['liner_diameter']"
            :loaded="fieldsLoaded['liner_diameter']"
            />
        </b-col>
        <b-col cols="6" md="6">
          <form-input
            id="linerThickness"
            label="Liner Thickness"
            hint="inches"
            type="number"
            v-model.number="linerThicknessInput"
            :errors="errors['liner_thickness']"
            :loaded="fieldsLoaded['liner_thickness']"
            />
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="6" md="6">
          <form-input
            id="linerFrom"
            label="Liner From"
            hint="feet (below ground level)"
            type="number"
            v-model.number="linerFromInput"
            :errors="errors['liner_from']"
            :loaded="fieldsLoaded['liner_from']"
            />
        </b-col>
        <b-col cols="6" md="6">
          <form-input
            id="linerTo"
            label="Liner To"
            hint="feet (below ground level)"
            type="number"
            v-model.number="linerToInput"
            :errors="errors['liner_to']"
            :loaded="fieldsLoaded['liner_to']"
            />
        </b-col>
      </b-row>
      <b-row>
        <b-col>Liner Perforations</b-col>
      </b-row>
      <b-row>
        <b-col>
          <table class="table">
            <thead>
              <tr>
                <th>Perforated From</th>
                <th>Perforated To</th>
                <th></th>
              </tr>
              <tr v-for="(liner, index) in linerPerforationsInput" :key="index">
                <td>
                  <form-input
                    :id="`liner_perforated_from_${index}`"
                    type="number"
                    hint="feet (below ground level)"
                    v-model.number="liner.liner_perforation_from"
                    :errors="getLinerPerforationError(index).liner_perforation_from"
                    :loaded="getFieldsLoaded(index).liner_perforation_from"/>
                </td>
                <td>
                  <form-input
                    :id="`liner_perforated_to_${index}`"
                    type="number"
                    hint="feet (below ground level)"
                    v-model.number="liner.liner_perforation_to"
                    :errors="getLinerPerforationError(index).liner_perforation_to"
                    :loaded="getFieldsLoaded(index).liner_perforation_to"/>
                </td>
                <td>
                  <a href="#" v-on:click.prevent="removeRow(index)">remove</a>
                </td>
              </tr>
            </thead>
            <tbody>
            </tbody>
          </table>
          <a href="#" v-on:click.prevent="addRow">add another row</a>
        </b-col>
      </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'

export default {
  name: 'Step08LinerInformation',
  mixins: [inputBindingsMixin],
  props: {
    linerMaterial: String,
    linerDiameter: Number,
    linerThickness: Number,
    linerFrom: Number,
    linerTo: Number,
    linerPerforations: {
      type: Array,
      default: () => []
    },
    errors: {
      type: Object,
      default: () => ({}),
      isInput: false
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({}),
      isInput: false
    }
  },
  methods: {
    getLinerPerforationError (index) {
      if (this.errors && 'linerPerforations' in this.errors && index in this.errors['linerPerforations']) {
        return this.errors['linerPerforations'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'linerPerforations' in this.fieldsLoaded && index in this.fieldsLoaded['linerPerforations']) {
        return this.fieldsLoaded['linerPerforations'][index]
      }
      return {}
    },
    addRow () {
      this.linerPerforations.push({})
    },
    removeRow (index) {
      this.linerPerforations.splice(index, 1)
    }
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>
</style>
