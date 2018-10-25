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
  <div>
    <b-card no-body class="p-3 mb-4">
      <api-error v-if="error" :error="error"/>
      <b-alert variant="success" :show="showSaveSuccess">Record successfully updated</b-alert>

      <b-container>
        <b-row v-if="!loading" class="border-bottom mb-3 pb-2">
          <b-col><h5>Aquifer {{record.aquifer_id}} Summary - Edit</h5></b-col>
        </b-row>

        <b-row v-if="loading" class="border-bottom mb-3 pb-2">
          <b-col><h5>Loading...</h5></b-col>
        </b-row>

        <b-row>
          <b-col md="6">
            <b-row>
              <b-col md="4" class="col-form-label">
                Aquifer number
              </b-col>
              <b-col md="8" class="col-form-label">
                {{record.aquifer_id}}
              </b-col>
            </b-row>
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
                  id="mapping_year"
                  type="text"
                  v-model="record.mapping_year"
                  required/>
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
                  id="aquifer_name"
                  type="text"
                  v-model="record.aquifer_name"
                  required/>
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
                  id="litho_stratographic_unit"
                  type="text"
                  v-model="record.litho_stratographic_unit"
                  required/>
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
                  id="location_description"
                  type="text"
                  v-model="record.location_description"
                  required/>
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
                :options="vulnerability_codes"
                id="vulnerability"
                text-field="description"
                v-model="record.vulnerability"
                value-field="code"
                required/>
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
                :options="material_codes"
                id="material"
                text-field="description"
                v-model="record.material"
                value-field="code"
                required/>
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
                id="subtype"
                v-model="record.subtype"
                :options="subtype_codes"
                value-field="code"
                text-field="description"
                required/>
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
                id="quality_concern"
                v-model="record.quality_concern"
                :options="quality_concern_codes"
                value-field="code"
                text-field="description"
                required/>
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
                id="productivity"
                v-model="record.productivity"
                :options="productivity_codes"
                value-field="code"
                text-field="description"
                required/>
            </b-form-group>
          </b-col>
        </b-row>

        <b-row>
          <b-col md="6">
            <b-form-group
              horizontal
              label-cols="4"
              label="Size (km²)"
              label-for="area"
              :invalid-feedback="fieldErrorMessages.area"
              :state="fieldHasError.area">
              <b-form-input
                id="area"
                type="text"
                v-model="record.area"
                required/>
            </b-form-group>
          </b-col>

          <b-col md="6">
            <b-form-group
              horizontal
              label-cols="4"
              label="Demand"
              label-for="demand"
              :invalid-feedback="fieldErrorMessages.demand"
              :state="fieldHasError.demand">
              <b-form-select
                id="demand"
                v-model="record.demand"
                :options="demand_codes"
                value-field="code"
                text-field="description"
                required/>
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
                id="known_water_use"
                v-model="record.known_water_use"
                :options="known_water_use_codes"
                  value-field="code"
                text-field="description"
                required/>
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
                id="notes"
                v-model="record.notes"/>
            </b-form-group>
          </b-col>
        </b-row>

        <b-row class="mt-4">
          <b-col cols="auto">
            <b-button
              :disabled="loading"
              variant="secondary"
              v-b-modal.confirmSave>
              Save
            </b-button>

            <b-button
              :disabled="loading"
              variant="secondary"
              v-b-modal.confirmCancel>
              Cancel
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-card>

    <b-modal
      v-on:ok="save()"
      id="confirmSave">
      <p>Are you sure you would like to save this record?</p>
    </b-modal>

    <b-modal
      v-on:ok="view"
      id="confirmCancel">
      <p>Are you sure you want to quit editing this record?</p>
    </b-modal>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'
import { isEmpty, mapValues } from 'lodash'

export default {
  components: {
    'api-error': APIErrorMessage
  },
  created () {
    this.fetch()
    this.fetchCodes()
  },
  computed: {
    formState:
    () => isEmpty(this.fieldErrors),
    fieldErrorMessages () {
      return mapValues(this.fieldErrors, (messages) => messages.join(', '))
    },
    fieldHasError () {
      return mapValues(this.fieldErrors, (messages) => isEmpty(messages))
    }
  },
  data () {
    return {
      demand_codes: [],
      error: undefined,
      fieldErrors: {},
      known_water_use_codes: [],
      loading: false,
      material_codes: [],
      productivity_codes: [],
      quality_concern_codes: [],
      record: {},
      showSaveSuccess: false,
      subtype_codes: [],
      vulnerability_codes: []
    }
  },
  methods: {
    handlePatchError (error) {
      if (error.response) {
        if (error.response.status === 400) {
          this.fieldErrors = error.response.data
        } else {
          this.error = error.response
        }
      } else {
        this.error = error.message
      }
    },
    save (id = this.id) {
      this.showSaveSuccess = false
      this.fieldErrors = {}

      ApiService.patch('aquifers', id, this.record)
        .then(() => { this.showSaveSuccess = true })
        .catch(this.handlePatchError)
    },
    view () {
      this.$router.push({ name: 'view', params: { id: this.id } })
    },
    fetch (id = this.id) {
      this.loading = true
      this.error = undefined

      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        })
        .then(() => { this.loading = false })
        .catch((error) => { this.error = error.response })
    },
    fetchCode (code, key) {
      ApiService.query(code).then((response) => {
        this[key] = response.data.results
      })
    },
    fetchCodes () {
      this.fetchCode('aquifer-codes/materials', 'material_codes')
      this.fetchCode('aquifer-codes/quality-concerns', 'quality_concern_codes')
      this.fetchCode('aquifer-codes/vulnerability', 'vulnerability_codes')
      this.fetchCode('aquifer-codes/subtypes', 'subtype_codes')
      this.fetchCode('aquifer-codes/productivity', 'productivity_codes')
      this.fetchCode('aquifer-codes/demand', 'demand_codes')
      this.fetchCode('aquifer-codes/water-use', 'known_water_use_codes')
    }
  },
  props: ['id']
}
</script>
