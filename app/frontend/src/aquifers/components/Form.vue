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
    <Message v-if="statusMessage" severity="info">
      {{statusMessage}}
    </Message>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div class="flex flex-col">
        <label for="aquifer-status">Aquifer Status</label>
        <Select
          id="aquifer-status"
          v-model="status"
          :options="aquiferStatusOptions"
          optionLabel="text"
          optionValue="value"
          :disabled="fieldDisabled"
          @change="statusChanged"/>
      </div>
      <div class="flex flex-col">
        <label for="aquifer-mapping-year">Year of mapping</label>
          <InputText
            id="aquifer-mapping-year"
            type="text"
            :disabled="fieldDisabled"
            :invalid="fieldErrorMessages.mapping_year"
            v-model="record.mapping_year"/>
          <Message v-if="fieldHasError.mapping_year" severity="error">
            {{  fieldErrorMessages.mapping_year }}
          </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div class="flex flex-col">
        <label for="aquifer_name">Aquifer name</label>
          <InputText
            id="aquifer_name"
            type="text"
            :disabled="fieldDisabled"
            :invalid="fieldErrorMessages.aquifer_name"
            v-model="record.aquifer_name"/>
          <Message v-if="fieldHasError.aquifer_name" severity="error">
            {{  fieldErrorMessages.aquifer_name }}
          </Message>
      </div>
      <div class="flex flex-col">
        <label for="aquifer-litho-stratigraphic-unit">Litho stratigraphic unit</label>
          <InputText
            id="aquifer-litho-stratigraphic-unit"
            type="text"
            :disabled="fieldDisabled"
            :invalid="fieldErrorMessages.litho_stratographic_unit"
            v-model="record.litho_stratographic_unit"/>
          <Message v-if="fieldHasError.litho_stratographic_unit" severity="error">
            {{  fieldErrorMessages.litho_stratographic_unit }}
          </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div class="flex flex-col">
        <label for="aquifer-location-description">Descriptive location</label>
          <InputText
            id="aquifer-location-description"
            type="text"
            :disabled="fieldDisabled"
            :invalid="fieldErrorMessages.location_description"
            v-model="record.location_description"/>
          <Message v-if="fieldHasError.location_description" severity="error">
            {{  fieldErrorMessages.location_description }}
          </Message>
      </div>
      <div class="flex flex-col">
        <label for="aquifer-vulnerability">Vulnerability</label>
        <Select
          id="aquifer-vulnerability"
          v-model="record.vulnerability"
          :options="[''].concat(vulnerability_codes)"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"
          :invalid="fieldErrorMessages.vulnerability"/>
        <Message v-if="fieldHasError.vulnerability" severity="error">
          {{  fieldErrorMessages.vulnerability }}
        </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div class="flex flex-col">
        <label for="material">Material type</label>
        <Select
          id="aquifer-material"
          :options="[''].concat(material_codes)"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"
          v-model="record.material"/>
        <Message v-if="fieldHasError.material" severity="error">
          {{  fieldErrorMessages.material }}
        </Message>
      </div>
      <div class="flex flex-col">
        <label for="subtype">Subtype</label>
        <Select
          id="aquifer-subtype"
          v-model="record.subtype"
          :options="[''].concat(subtype_codes)"
          :disabled="fieldDisabled"
          optionLabel="description"
          optionValue="code"/>
        <Message v-if="fieldHasError.material" severity="error">
          {{  fieldErrorMessages.material }}
        </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div class="flex flex-col">
        <label for="quality_concern">Quality concerns</label>
        <Select
          id="aquifer-quality-concern"
          v-model="record.quality_concern"
          :options="[''].concat(quality_concern_codes)"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"/>
        <Message v-if="fieldHasError.material" severity="error">
          {{  fieldErrorMessages.material }}
        </Message>
      </div>
      <div class="flex flex-col">
        <label for="productivity">Productivity</label>
        <Select
          id="aquifer-productivity"
          v-model="record.productivity"
          :options="[''].concat(productivity_codes)"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"/>
        <Message v-if="fieldHasError.productivity" severity="error">
          {{  fieldErrorMessages.productivity }}
        </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div>
        <label for="known_water_use">Type of known water use</label>
        <Select
          id="aquifer-known-water-use"
          v-model="record.known_water_use"
          :options="[''].concat(known_water_use_codes)"
          :disabled="fieldDisabled"
          optionValue="code"
          optionLabel="description"/>
        <Message v-if="fieldHasError.known_water_use" severity="error">
          {{  fieldErrorMessages.known_water_use }}
        </Message>
      </div>
      <div>
        <label for="shapefile-upload">Shapefile</label>
        <FileUpload
          id="shapefile-upload"
          mode="basic"
          accept=".zip"
          :disabled="fieldDisabled"
          auto
          customUpload
          @uploader="onFileSelect"
        />
        <small>
          Please upload a shapefile containing only this aquifer in ZIP format.
        </small>
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6" gap="4">
      <div>
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
      </div>
    </responsive-grid>
    <responsive-grid :cols="4" :md="6">
      <div>
        <b-form-group
          horizontal
          label-cols="4"
          label="Documents">
          <b-form-file
            v-model="uploadFiles"
            multiple
            plain/>
          <div class="mt-4">
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
      </div>
    </responsive-grid>

    <h4 class="mt-6">Resource Links</h4>
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

    <div class="mt-6">
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
import { isEmpty, mapValues, cloneDeep } from 'lodash-es'
import { useAquiferStore } from '@/stores/aquifers.js'
import { useCommonStore } from '@/stores/common.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

import ApiService from '@/common/services/ApiService.js'
import { END_OF_TIME_ISO_8601 } from '@/common/helpers/dates.js'

import Documents from './Documents.vue'

export default {
  components: {
    'aquifer-documents': Documents,
    ResponsiveGrid
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
        return this.commonStore.uploadFiles
      },
      set: function (value) {
        this.commonStore.setFiles(value)
      }
    },
    shape: {
      get: function () {
        return this.commonStore.shapefile
      },
      set: function (value) {
        this.commonStore.setShapefile(value)
      }
    },
    privateDocument: {
      get: function () {
        return this.commonStore.isPrivate
      },
      set: function (value) {
        this.commonStore.setPrivate(value)
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
    aquiferStore () { return useAquiferStore() },
    commonStore () { return useCommonStore() },
    demand_codes () { return this.aquiferStore.demand_codes },
    aquifer_resource_sections () { return this.aquiferStore.aquifer_resource_sections },
    known_water_use_codes () { return this.aquiferStore.known_water_use_codes },
    material_codes () { return this.aquiferStore.material_codes },
    productivity_codes () { return this.aquiferStore.productivity_codes },
    quality_concern_codes () { return this.aquiferStore.quality_concern_codes },
    subtype_codes () { return this.aquiferStore.subtype_codes },
    vulnerability_codes () { return this.aquiferStore.vulnerability_codes },
    fieldDisabled () {
      return this.loadingData
    }
  },
  methods: {
    addCodes (payload) { this.aquiferStore.addCodes(payload) },
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
