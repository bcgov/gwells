<template>
  <fieldset>
    <legend>Liner Information</legend>
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
            hint="ft (bgl)"
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
            hint="ft (bgl)"
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
          <table class="table table-sm">
            <thead>
              <tr>
                <th class="font-weight-normal">Perforated From ft (bgl)</th>
                <th class="font-weight-normal">Perforated To ft (bgl)</th>
                <th></th>
              </tr>
              <tr v-for="(liner, index) in linerPerforationsInput" :key="index">
                <td>
                  <form-input
                    :id="`liner_perforated_from_${index}`"
                    type="number"
                    v-model.number="liner.start"
                    :errors="getLinerPerforationError(index).start"
                    :loaded="getFieldsLoaded(index).start"/>
                </td>
                <td>
                  <form-input
                    :id="`liner_perforated_to_${index}`"
                    type="number"
                    v-model.number="liner.end"
                    :errors="getLinerPerforationError(index).end"
                    :loaded="getFieldsLoaded(index).end"/>
                </td>
                <td>
                  <b-btn size="sm" variant="primary" @click="removeRow(index)" class="mt-2"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                </td>
              </tr>
            </thead>
            <tbody>
            </tbody>
          </table>
          <b-btn size="sm" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
        </b-col>
      </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'

export default {
  name: 'LinerInformation',
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
      isInput: true
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({}),
      isInput: true
    }
  },
  methods: {
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
