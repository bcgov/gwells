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
        <b-col md="6">
          <table class="table table-sm no-border">
            <thead>
              <tr>
                <th class="font-weight-normal no-border">Perforated From ft (bgl)</th>
                <th class="font-weight-normal">Perforated To ft (bgl)</th>
                <th></th>
              </tr>
              <tr v-for="(liner, index) in linerPerforationsInput" :key="index">
                <td class="pb-0 pt-1">
                  <form-input
                    :id="`liner_perforated_from_${index}`"
                    type="number"
                    class="mb-0"
                    v-model.number="liner.start"
                    :errors="getLinerPerforationError(index).start"
                    :loaded="getFieldsLoaded(index).start"/>
                </td>
                <td class="pb-0 pt-1">
                  <form-input
                    :id="`liner_perforated_to_${index}`"
                    type="number"
                    class="mb-0"
                    v-model.number="liner.end"
                    :errors="getLinerPerforationError(index).end"
                    :loaded="getFieldsLoaded(index).end"/>
                </td>
                <td class="py-0">
                  <b-btn size="sm" :id="`removeLinerPerfRowBtn${index}`" variant="primary" @click="removeRowIfOk(index)" class="mt-2"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                </td>
              </tr>
            </thead>
            <tbody>
            </tbody>
          </table>
          <b-btn size="sm" variant="primary" id="addlinerPerforationRowBtn" @click="addRow"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
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
    }
  },
  data () {
    return {
      confirmRemoveModal: false,
      rowIndexToRemove: null
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
    removeRowByIndex (index) {
      this.linerPerforations.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.linerPerforations[rowNumber])) {
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
  computed: {
    ...mapGetters(['codes'])
  },
  created () {
    // When component created, add an initial row of lithology.
    if (!this.linerPerforationsInput.length) {
      this.linerPerforationsInput.push({}, {}, {})
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
