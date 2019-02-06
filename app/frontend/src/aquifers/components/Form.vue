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
  <b-container>
    <b-row>
      <b-col md="6">
        <b-row v-if="showId">
          <b-col md="4" class="aquifer-id col-form-label">
            Aquifer number
          </b-col>
          <b-col class="aquifer-id" md="8">
            {{record.aquifer_id}}
          </b-col>
        </b-row>

        <b-form-group
          horizontal
          label-cols="4"
          label="Aquifer name"
          label-for="aquifer_name"
          :invalid-feedback="fieldErrorMessages.aquifer_name"
          :state="fieldHasError.aquifer_name">
            <b-form-input
              tabindex="1"
              id="aquifer-name"
              type="text"
              v-model="record.aquifer_name"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Descriptive location"
          label-for="location_description"
          :invalid-feedback="fieldErrorMessages.location_description"
          :state="fieldHasError.location_description">
            <b-form-input
              tabindex="3"
              id="aquifer-location-description"
              type="text"
              v-model="record.location_description"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Material type"
          label-for="material"
          :invalid-feedback="fieldErrorMessages.material"
          :state="fieldHasError.material">
          <b-form-select
            tabindex="5"
            :options="[''].concat(material_codes)"
            id="aquifer-material"
            text-field="description"
            v-model="record.material"
            value-field="code"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Quality concerns"
          label-for="quality_concern"
          :invalid-feedback="fieldErrorMessages.quality_concern"
          :state="fieldHasError.quality_concern">
          <b-form-select
            tabindex="7"
            id="aquifer-quality-concern"
            v-model="record.quality_concern"
            :options="[''].concat(quality_concern_codes)"
            value-field="code"
            text-field="description"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Size (km²)"
          label-for="area"
          :invalid-feedback="fieldErrorMessages.area"
          :state="fieldHasError.area">
          <b-form-input
            tabindex="9"
            id="aquifer-area"
            type="text"
            v-model="record.area"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Type of known water use"
          label-for="known_water_use"
          :invalid-feedback="fieldErrorMessages.known_water_use"
          :state="fieldHasError.known_water_use">
          <b-form-select
            tabindex="11"
            id="aquifer-known-water-use"
            v-model="record.known_water_use"
            :options="[''].concat(known_water_use_codes)"
            value-field="code"
            text-field="description"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Comments"
          label-for="notes"
          :invalid-feedback="fieldErrorMessages.notes"
          :state="fieldHasError.notes">
          <b-form-textarea
            tabindex="13"
            rows="4"
            id="aquifer-notes"
            v-model="record.notes"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Documents">
          <b-form-file
            v-model="files"
            multiple
            plain/>
          <div class="mt-3">
            <b-form-checkbox
             id="isPrivateCheckbox"
             v-model="privateDocument">Are these documents private?</b-form-checkbox>
          </div>
          <div class="mt-3" v-if="upload_files.length > 0">
            <b-list-group>
              <b-list-group-item v-for="(f, index) in upload_files" :key="index">{{f.name}}</b-list-group-item>
            </b-list-group>
          </div>
        </b-form-group>
      </b-col>

      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Year of mapping"
          label-for="mapping_year"
          :invalid-feedback="fieldErrorMessages.mapping_year"
          :state="fieldHasError.mapping_year">
            <b-form-input
              tabindex="2"
              id="aquifer-mapping-year"
              type="text"
              v-model="record.mapping_year"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Litho stratigraphic unit"
          label-for="litho_stratographic_unit"
          :invalid-feedback="fieldErrorMessages.litho_stratographic_unit"
          :state="fieldHasError.litho_stratographic_unit">
            <b-form-input
              tabindex="4"
              id="aquifer-litho-stratigraphic-unit"
              type="text"
              v-model="record.litho_stratographic_unit"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Vulnerability"
          label-for="vulnerability"
          :invalid-feedback="fieldErrorMessages.vulnerability"
          :state="fieldHasError.vulnerability">
          <b-form-select
            tabindex="6"
            :options="[''].concat(vulnerability_codes)"
            id="aquifer-vulnerability"
            text-field="description"
            v-model="record.vulnerability"
            value-field="code"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Subtype"
          label-for="subtype"
          :invalid-feedback="fieldErrorMessages.subtype"
          :state="fieldHasError.subtype">
          <b-form-select
            tabindex="8"
            id="aquifer-subtype"
            v-model="record.subtype"
            :options="[''].concat(subtype_codes)"
            value-field="code"
            text-field="description"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Productivity"
          label-for="productivity"
          :invalid-feedback="fieldErrorMessages.productivity"
          :state="fieldHasError.productivity">
          <b-form-select
            tabindex="10"
            id="aquifer-productivity"
            v-model="record.productivity"
            :options="[''].concat(productivity_codes)"
            value-field="code"
            text-field="description"/>
        </b-form-group>

        <b-form-group
          horizontal
          label-cols="4"
          label="Demand"
          label-for="demand"
          :invalid-feedback="fieldErrorMessages.demand"
          :state="fieldHasError.demand">
          <b-form-select
            tabindex="12"
            id="aquifer-demand"
            v-model="record.demand"
            :options="[''].concat(demand_codes)"
            value-field="code"
            text-field="description"/>
        </b-form-group>
      </b-col>
    </b-row>

    <b-row class="mt-4">
      <b-col cols="auto">
        <b-button
          variant="primary"
          v-b-modal.confirmSave>
          Save
        </b-button>

        <b-button
          variant="default"
          v-b-modal.confirmCancel>
          Cancel
        </b-button>
      </b-col>
    </b-row>

    <b-modal
      ok-variant="primary"
      cancel-variant="default"
      v-on:ok="$emit('save')"
      id="confirmSave">
      <p>Are you sure you would like to save this record?</p>
    </b-modal>

    <b-modal
      ok-variant="primary"
      cancel-variant="default"
      v-on:ok="$emit('cancel')"
      id="confirmCancel">
      <p>Are you sure you want to quit editing this record?</p>
    </b-modal>
  </b-container>
</template>

<style>
.aquifer-id {
  padding-top: 1rem !important;
  padding-bottom: 1rem !important;
}
</style>

<script>
import { isEmpty, mapValues } from 'lodash'
import { mapMutations, mapState } from 'vuex'

export default {
  computed: {
    fieldErrorMessages () {
      return mapValues(this.fieldErrors, (messages) => messages.join(', '))
    },
    fieldHasError () {
      return mapValues(this.fieldErrors, (messages) => isEmpty(messages))
    },
    files: {
      get: function () {
        return this.upload_files
      },
      set: function (value) {
        this.setFiles(value)
      }
    },
    privateDocument: {
      get: function () {
        return this.isPrivate
      },
      set: function (value) {
        this.setPrivate(value)
      }
    },
    ...mapState('aquiferCodes', [
      'demand_codes',
      'known_water_use_codes',
      'material_codes',
      'productivity_codes',
      'quality_concern_codes',
      'subtype_codes',
      'vulnerability_codes'
    ]),
    ...mapState('documentState', [
      'isPrivate',
      'upload_files'
    ])
  },
  methods: {
    ...mapMutations('documentState', [
      'setFiles',
      'setPrivate'
    ])
  },
  props: {
    fieldErrors: Object,
    record: Object,
    showId: Boolean
  }
}
</script>
