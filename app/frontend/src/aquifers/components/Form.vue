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
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="aquifer-status">Aquifer Status</label>
      <Select
        inputId="aquifer-status"
        v-model="status"
        :options="aquiferStatusOptions"
        optionLabel="text"
        optionValue="value"
        :disabled="fieldDisabled"
        @change="statusChanged"
        class="w-full col-span-4"/>
      <label for="aquifer-mapping-year">Year of mapping</label>
      <div>
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
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="aquifer_name">Aquifer name</label>
      <div>
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
      <label for="aquifer-litho-stratigraphic-unit">Litho stratigraphic unit</label>
      <div>
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
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="aquifer-location-description">Descriptive location</label>
      <div>
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
      <label for="aquifer-vulnerability">Vulnerability</label>
      <div>
        <Select
          id="aquifer-vulnerability"
          v-model="record.vulnerability"
          :options="vulnerability_codes"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"
          :invalid="fieldErrorMessages.vulnerability"
          showClear
          class="w-full"/>
        <Message v-if="fieldHasError.vulnerability" severity="error">
          {{  fieldErrorMessages.vulnerability }}
        </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
        <label for="material">Material type</label>
        <div>
          <Select
            id="aquifer-material"
            :options="material_codes"
            optionLabel="description"
            optionValue="code"
            :disabled="fieldDisabled"
            v-model="record.material"
            showClear
            class="w-full"/>
          <Message v-if="fieldHasError.material" severity="error">
            {{  fieldErrorMessages.material }}
          </Message>
        </div>
        <label for="subtype">Subtype</label>
        <div>
          <Select
            id="aquifer-subtype"
            v-model="record.subtype"
            :options="subtype_codes"
            :disabled="fieldDisabled"
            optionLabel="description"
            optionValue="code"
            showClear
            class="w-full"/>
          <Message v-if="fieldHasError.material" severity="error">
            {{  fieldErrorMessages.material }}
          </Message>
        </div>
    </responsive-grid>
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="aquifer-quality-concern">Quality concerns</label>
      <div>
        <Select
          id="aquifer-quality-concern"
          v-model="record.quality_concern"
          :options="quality_concern_codes"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"
          showClear
          class="w-full"/>
        <Message v-if="fieldHasError.material" severity="error">
          {{  fieldErrorMessages.material }}
        </Message>
      </div>
      <label for="productivity">Productivity</label>
      <div>
        <Select
          id="aquifer-productivity"
          v-model="record.productivity"
          :options="productivity_codes"
          optionLabel="description"
          optionValue="code"
          :disabled="fieldDisabled"
          showClear
          class="w-full"/>
        <Message v-if="fieldHasError.productivity" severity="error">
          {{  fieldErrorMessages.productivity }}
        </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="known_water_use">Type of known water use</label>
      <div>
        <Select
          id="aquifer-known-water-use"
          v-model="record.known_water_use"
          :options="known_water_use_codes"
          :disabled="fieldDisabled"
          optionValue="code"
          optionLabel="description"
          showClear
          class="w-full"/>
        <Message v-if="fieldHasError.known_water_use" severity="error">
          {{  fieldErrorMessages.known_water_use }}
        </Message>
      </div>
      <label for="shapefile-upload">Shapefile</label>
      <div>
        <FileUpload
          id="shapefile-upload"
          mode="basic"
          accept=".zip"
          :disabled="fieldDisabled"
          auto
          customUpload
          @uploader="onFileSelect"
          class="w-full"/>
        <small>
          Please upload a shapefile containing only this aquifer in ZIP format.
        </small>
      </div>
    </responsive-grid>
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="notes">Comments</label>
      <div>
        <Textarea
        id="aquifer-notes"
        rows="5"
        cols="30"
        :disabled="fieldDisabled"
        v-model="record.notes"
        class="w-full"/>
        <Message v-if="fieldHasError.notes" severity="error">
          {{  fieldErrorMessages.notes }}
        </Message>
      </div>
    </responsive-grid>
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4">
      <label for="isPrivateCheckbox">Documents</label>
      <div>
        <FileUpload
          id="document-upload"
          mode="basic"
          name="documents"
          :multiple="true"
          :auto="false"
          chooseLabel="Choose"
          @select="onFileSelect"
          class="w-full"/>
          <Checkbox
            v-model="privateDocument"
            inputId="isPrivateCheckbox"
            :binary="true"
            :disabled="fieldDisabled"/>
          <label for="isPrivateCheckbox" class="ml-2">Are these documents private?</label>
      </div>
    </responsive-grid>
    <div class="mt-4">
      <h5 class="w-full">Public documentation</h5>
      <aquifer-documents :files="files"
        :editMode="true"
        :id="id"
        :loading="loadingFiles"
        v-on:fetchFiles="$emit('fetchFiles')">
      </aquifer-documents>
    </div>

    <h4 class="mt-6">Resource Links</h4>
    <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="mt-4"
      v-for="(resource, index) in record.resources" :key="index">
      <div>
        <label for="section">Section</label>
        <Select
          v-model="resource.section_code"
          inputId="section"
          :options="aquifer_resource_sections"
          :disabled="fieldDisabled"
          optionLabel="name"
          optionValue="code"
          showClear
          class="w-full"/>
        <Message v-if="resourceErrorMessages[index].section" severity="error">
          {{  resourceErrorMessages[index].section }}
        </Message>
      </div>
      <div>
        <label for="name">Document Name</label>
        <InputText
          type="text"
          :disabled="fieldDisabled"
          v-model="resource.name"
          class="w-full"/>
        <Message v-if="resourceErrorMessages[index].name" severity="error">
          {{  resourceErrorMessages[index].name }}
        </Message>
      </div>
      <div>
        <label for="url">Document URL</label>
        <InputText
          type="text"
          :disabled="fieldDisabled"
          v-model="resource.url"
          class="w-full"/>
        <Message v-if="resourceErrorMessages[index].url" severity="error">
          {{  resourceErrorMessages[index].url }}
        </Message>
      </div>
      <div cols="auto">
        <br>
        <Button label="Remove" @click="handleDeleteResource(index)"/>
      </div>
    </responsive-grid>
    <div class="mt-4">
        <Button label="Add additional link" :disabled="fieldDisabled" @click="handleAddResource()"/>
    </div>

    <div class="mt-6">
      <Button
        label="Save"
        :loading="loadingData"
        @click="showConfirmSave = true"
        class="mr-2"/>
      <Button
        label="Cancel"
        @click="showConfirmCancel = true"/>

      <Dialog
        v-model:visible="showConfirmSave"
        modal
        header="Confirm Save"
        :style="{ width: '25rem' }">
        <p>Are you sure you would like to save this record?</p>
        <template #footer>
          <Button
            label="Cancel"
            severity="secondary"
            text
            @click="showConfirmSave = false"
          />
          <Button
            label="OK"
            severity="primary"
            @click="handleSave"
          />
        </template>
      </Dialog>
      <Dialog
        v-model:visible="showConfirmCancel"
        modal
        header="Confirm Cancel"
        :style="{ width: '25rem' }">
        <p>Are you sure you want to quit editing this record?</p>
        <template #footer>
          <Button
            label="Cancel"
            severity="secondary"
            text
            @click="showConfirmCancel = false"
          />
          <Button
            label="OK"
            severity="primary"
            @click="handleCancel"
          />
        </template>
      </Dialog>
    </div>
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
      aquiferStatusOptions,
      showConfirmSave: false,
      showConfirmCancel: false
    }
  },
  computed: {
    id () { return this.$route.params.id },
    hasFormData () {
      if(!this.record) {
        return false
      }
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
      this.$nextTick(() => {
        if (!this.record) {
          this.record = {}
        }
        if (!this.record.resources) {
          this.record.resources = []
        }
          this.record.resources.push({
            name: '',
            url: '',
            section_id: '1'
          })
      })
    },
    handleDeleteResource (i) {
      this.record.resources.splice(i, 1)
    },
    handleSave() {
      this.showConfirmSave = false;
      this.$emit('save');
    },
    handleCancel() {
      this.showConfirmCancel = false;
      this.$emit('cancel');
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
