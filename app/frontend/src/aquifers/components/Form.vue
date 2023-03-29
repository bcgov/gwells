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
  <div class="container p-1">
    <b-alert show v-if="statusMessage" variant="info">
      {{statusMessage}}
    </b-alert>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Aquifer Status"
          label-for="aquifer-status">
          <b-form-select
            :options="aquiferStatusOptions"
            :disabled="fieldDisabled"
            id="aquifer-status"
            v-model="status"
            @change="statusChanged"/>
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
              id="aquifer-mapping-year"
              type="text"
              :disabled="fieldDisabled"
              v-model="record.mapping_year"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Aquifer name"
          label-for="aquifer_name"
          :invalid-feedback="fieldErrorMessages.aquifer_name"
          :state="fieldHasError.aquifer_name">
            <b-form-input
              id="aquifer-name"
              type="text"
              :disabled="fieldDisabled"
              v-model="record.aquifer_name"/>
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Litho stratigraphic unit"
          label-for="litho_stratographic_unit"
          :invalid-feedback="fieldErrorMessages.litho_stratographic_unit"
          :state="fieldHasError.litho_stratographic_unit">
            <b-form-input
              id="aquifer-litho-stratigraphic-unit"
              type="text"
              :disabled="fieldDisabled"
              v-model="record.litho_stratographic_unit"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Descriptive location"
          label-for="location_description"
          :invalid-feedback="fieldErrorMessages.location_description"
          :state="fieldHasError.location_description">
            <b-form-input
              id="aquifer-location-description"
              type="text"
              :disabled="fieldDisabled"
              v-model="record.location_description"/>
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Vulnerability"
          label-for="vulnerability"
          :invalid-feedback="fieldErrorMessages.vulnerability"
          :state="fieldHasError.vulnerability">
          <b-form-select
            :options="[''].concat(vulnerability_codes)"
            :disabled="fieldDisabled"
            id="aquifer-vulnerability"
            text-field="description"
            v-model="record.vulnerability"
            value-field="code"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Material type"
          label-for="material"
          :invalid-feedback="fieldErrorMessages.material"
          :state="fieldHasError.material">
          <b-form-select
            :options="[''].concat(material_codes)"
            :disabled="fieldDisabled"
            id="aquifer-material"
            text-field="description"
            v-model="record.material"
            value-field="code"/>
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Subtype"
          label-for="subtype"
          :invalid-feedback="fieldErrorMessages.subtype"
          :state="fieldHasError.subtype">
          <b-form-select
            id="aquifer-subtype"
            v-model="record.subtype"
            :options="[''].concat(subtype_codes)"
            :disabled="fieldDisabled"
            value-field="code"
            text-field="description"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Quality concerns"
          label-for="quality_concern"
          :invalid-feedback="fieldErrorMessages.quality_concern"
          :state="fieldHasError.quality_concern">
          <b-form-select
            id="aquifer-quality-concern"
            v-model="record.quality_concern"
            :options="[''].concat(quality_concern_codes)"
            :disabled="fieldDisabled"
            value-field="code"
            text-field="description"/>
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Productivity"
          label-for="productivity"
          :invalid-feedback="fieldErrorMessages.productivity"
          :state="fieldHasError.productivity">
          <b-form-select
            id="aquifer-productivity"
            v-model="record.productivity"
            :options="[''].concat(productivity_codes)"
            :disabled="fieldDisabled"
            value-field="code"
            text-field="description"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Type of known water use"
          label-for="known_water_use"
          :invalid-feedback="fieldErrorMessages.known_water_use"
          :state="fieldHasError.known_water_use">
          <b-form-select
            id="aquifer-known-water-use"
            v-model="record.known_water_use"
            :options="[''].concat(known_water_use_codes)"
            :disabled="fieldDisabled"
            value-field="code"
            text-field="description"/>
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          description="Please upload a shapefile containing only this aqufier in ZIP format."
          label="Shapefile">
          <b-form-file
            :disabled="fieldDisabled"
            v-model="shape"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Comments"
          label-for="notes"
          :invalid-feedback="fieldErrorMessages.notes"
          :state="fieldHasError.notes">
          <b-form-textarea
            rows="4"
            id="aquifer-notes"
            :disabled="fieldDisabled"
            v-model="record.notes"/>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6">
        <b-form-group
          horizontal
          label-cols="4"
          label="Documents">
          <b-form-file
            v-model="uploadFiles"
            multiple
            plain/>
          <div class="mt-3">
            <b-form-checkbox
             id="isPrivateCheckbox"
            :disabled="fieldDisabled"
             v-model="privateDocument">Are these documents private?</b-form-checkbox>
          </div>
        </b-form-group>
        <h5>Public documentation</h5>
        <aquifer-documents :files="files"
          :editMode="true"
          :id="id"
          :loading="loadingFiles"
          v-on:fetchFiles="$emit('fetchFiles')">
        </aquifer-documents>
      </b-col>
    </b-row>

    <h4 class="mt-4">Resource Links</h4>
    <b-row
      v-for="(resource, index) in record.resources" :key="index">
      <b-col cols="auto">
        <b-form-group
          label="Section"
          label-for="section"
          :invalid-feedback="resourceErrorMessages[index].section"
          :state="!resourceErrorMessages[index].section">
          <b-form-select
            v-model="resource.section_code"
            :options="['-- Section --'].concat(aquifer_resource_sections)"
            :disabled="fieldDisabled"
            value-field="code"
            text-field="name"/>
        </b-form-group>
      </b-col>
      <b-col cols="auto">
        <b-form-group
          label="Document Name"
          label-for="name"
          :invalid-feedback="resourceErrorMessages[index].name"
          :state="!resourceErrorMessages[index].name">
          <b-form-input
            type="text"
            :disabled="fieldDisabled"
            v-model="resource.name"/>
        </b-form-group>
      </b-col>
      <b-col cols="auto">
        <b-form-group
          label="Document URL"
          label-for="url"
          :invalid-feedback="resourceErrorMessages[index].url"
          :state="!resourceErrorMessages[index].url">
          <b-form-input
            type="text"
            :disabled="fieldDisabled"
            v-model="resource.url"/>
        </b-form-group>
      </b-col>
      <b-col cols="auto">
        <br>
        <b-button variant="primary" @click="handleDeleteResource(index)">Remove</b-button>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="auto">
        <b-button
          variant="primary"
          :disabled="fieldDisabled"
          v-on:click="handleAddResource">
          Add additional link
        </b-button>
      </b-col>
    </b-row>

    <div class="mt-4">
      <b-button
        variant="primary"
        :disabled="loadingData"
        v-b-modal.confirmSave>
        Save
      </b-button>

      <b-button
        variant="default"
        v-b-modal.confirmCancel>
        Cancel
      </b-button>
    </div>

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
  </div>
</template>

<script>
// import AquiferResources from './AquiferResources.vue'
import { isEmpty, mapValues, cloneDeep } from 'lodash'
import { mapMutations, mapState } from 'vuex'

import ApiService from '@/common/services/ApiService.js'
import { END_OF_TIME_ISO_8601 } from '@/common/helpers/dates.js'

import Documents from './Documents.vue'

export default {
  components: {
    'aquifer-documents': Documents
  },
  props: {
    isNew: Boolean,
    fieldErrors: Object,
    record: Object,
    files: Object,
    loadingFiles: Boolean,
    loadingData: Boolean
  },
  data () {
    const aquiferStatusOptions = [
      { value: 'unpublished', text: 'Unpublished' },
      { value: 'published', text: 'Published' }
    ]

    if (!this.isNew) {
      aquiferStatusOptions.push({ value: 'retired', text: 'Retired' })
    }

    // set default status on new aquifers to unpublished
    if (this.isNew) {
      this.statusChanged('unpublished')
    }

    return {
      recordCopy: this.hasFormData ? cloneDeep(this.record) : {}, // keep a copy of the record
      status: this.isNew ? 'unpublished' : null,
      aquiferStatusOptions
    }
  },
  computed: {
    id () { return this.$route.params.id },
    hasFormData () {
      return Object.keys(this.record).length > 0
    },
    resourceErrorMessages () {
      let messages
      if (this.fieldErrors.resources) {
        console.log(JSON.stringify(this.fieldErrors.resources))
        messages = this.fieldErrors.resources.map((resource) => {
          return mapValues(resource, (messages) => messages.join(','))
        })
      } else {
        messages = this.record.resources.map(function (r) {
          return {}
        })
      }
      return messages
    },
    fieldErrorMessages () {
      return mapValues(this.fieldErrors, (messages) => messages.join(','))
    },
    fieldHasError () {
      return mapValues(this.fieldErrors, (messages) => isEmpty(messages))
    },
    uploadFiles: {
      get: function () {
        return this.upload_files
      },
      set: function (value) {
        this.setFiles(value)
      }
    },
    shape: {
      get: function () {
        return this.shapefile
      },
      set: function (value) {
        this.setShapefile(value)
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
    statusMessage () {
      if (this.status === 'unpublished') {
        return `
          An unpublished aquifer will be hidden from DataBC, iMapBC, the GWELLS Aquifer Search, the GWELLS
          Aquifer Summary and the CSV/XLS export.
        `
      } else if (this.status === 'retired') {
        return `
          A retired aquifer will not exist in DataBC, iMapBC, or the CSV/XLS export. However it still can be
          viewed on the GWELLS Aquifer Search and the GWELLS Aquifer Summary pages.
        `
      }
      return ''
    },
    ...mapState('aquiferStore/aquiferCodes', [
      'demand_codes',
      'aquifer_resource_sections',
      'known_water_use_codes',
      'material_codes',
      'productivity_codes',
      'quality_concern_codes',
      'subtype_codes',
      'vulnerability_codes'
    ]),
    ...mapState('documentState', [
      'isPrivate',
      'upload_files',
      'shapefile'
    ]),
    fieldDisabled () {
      return this.loadingData
    }
  },
  methods: {
    ...mapMutations('aquiferStore/aquiferCodes', ['addCodes']),
    ...mapMutations('documentState', [
      'setFiles',
      'setPrivate',
      'setShapefile'
    ]),
    handleAddResource () {
      this.record.resources.push({
        name: '',
        url: '',
        section_id: '1'
      })
    },
    handleDeleteResource (i) {
      this.record.resources.splice(i, 1)
    },
    fetchCode (codePath, key) {
      ApiService.query(codePath).then((response) => {
        this.addCodes({ key, codeTable: response.data.results })
      })
    },
    fetchCodes () {
      this.fetchCode('aquifers/sections', 'aquifer_resource_sections')
      this.fetchCode('aquifer-codes/materials', 'material_codes')
      this.fetchCode('aquifer-codes/quality-concerns', 'quality_concern_codes')
      this.fetchCode('aquifer-codes/vulnerability', 'vulnerability_codes')
      this.fetchCode('aquifer-codes/subtypes', 'subtype_codes')
      this.fetchCode('aquifer-codes/productivity', 'productivity_codes')
      this.fetchCode('aquifer-codes/demand', 'demand_codes')
      this.fetchCode('aquifer-codes/water-use', 'known_water_use_codes')
    },
    statusChanged (val) {
      const now = new Date().toISOString()
      switch (val) {
        case 'unpublished':
          // if !isNew then reset to initial value
          this.record.effective_date = this.isNew ? END_OF_TIME_ISO_8601 : this.recordCopy.effective_date
          this.record.expiry_date = now
          this.record.retire_date = END_OF_TIME_ISO_8601
          break
        case 'published':
          this.record.effective_date = now
          this.record.expiry_date = END_OF_TIME_ISO_8601
          this.record.retire_date = END_OF_TIME_ISO_8601
          break
        case 'retired':
          this.record.retire_date = now
          break
      }
    },
    setStatus (record) {
      if (!this.hasFormData) { return }

      const now = new Date()
      if ((new Date(record.effective_date) <= now) && (new Date(record.expiry_date) >= now)) {
        if (record.retire_date && new Date(record.retire_date) <= now) { // retired
          this.status = 'retired'
        } else {
          this.status = 'published'
        }
      } else {
        // unpublished
        this.status = 'unpublished'
      }
    }
  },
  created () {
    this.fetchCodes()

    if (this.hasFormData) {
      this.setStatus(this.record)
    }
  },
  watch: {
    record (record) {
      if (this.hasFormData) {
        this.recordCopy = cloneDeep(record) // keep a copy of the loaded data to compare with later
        this.setStatus(record)
      }
    }
  }
}
</script>

<style>
.aquifer-id {
  padding-top: calc(.375rem + 1px) !important;
  padding-bottom: calc(.375rem + 1px) !important;
}
</style>
