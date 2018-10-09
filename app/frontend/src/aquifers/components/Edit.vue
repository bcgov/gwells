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

      <b-container>
        <b-row v-if="!loading">
          <b-col><h5>Aquifer {{record.aquifer_id}} Summary - Edit</h5></b-col>
        </b-row>

        <b-row v-if="loading">
          <b-col><h5>Loading...</h5></b-col>
        </b-row>

        <b-form-row class="mt-3">
          <b-col md="2">
            Aquifer number
          </b-col>
          <b-col md="4">
            {{record.aquifer_id}}
          </b-col>

          <b-col md="2">
            <label for="mapping_year">Year of mapping</label>
          </b-col>
          <b-col md="2">
            <b-form-input
              id="mapping_year"
              type="text"
              v-model="record.mapping_year"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="2">
            <label for="aquifer_name">Aquifer name</label>
          </b-col>
          <b-col md="4">
            <b-form-input
              id="aquifer_name"
              type="text"
              v-model="record.aquifer_name"
              required/>
          </b-col>

          <b-col md="2">
            <label for="litho_stratographic_unit">Litho stratigraphic unit</label>
          </b-col>
          <b-col md="4">
            <b-form-input
              id="litho_stratographic_unit"
              type="text"
              v-model="record.litho_stratographic_unit"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="2">
            <label for="descriptive_location">Descriptive location</label>
          </b-col>
          <b-col md="4">
            <b-form-input
              id="descriptive_location"
              type="text"
              v-model="record.descriptive_location"
              required/>
          </b-col>

          <b-col md="2">
            <label for="vulnerability">Vulnerability</label>
          </b-col>
          <b-col md="4">
            <b-form-select
              :options="vulnerability_codes"
              id="vulnerability"
              text-field="description"
              v-model="record.vulnerability"
              value-field="code"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="2">
            <label for="material">Material type</label>
          </b-col>
          <b-col md="4">
            <b-form-select
              :options="material_codes"
              id="material"
              text-field="description"
              v-model="record.material"
              value-field="code"
              required/>
          </b-col>

          <b-col md="2">
            <label for="subtype">Subtype</label>
          </b-col>
          <b-col md="4">
            <b-form-select
              id="subtype"
              v-model="record.subtype"
              :options="subtype_codes"
              value-field="code"
              text-field="description"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="2">
            <label for="quality_concerns">Quality concerns</label>
          </b-col>
          <b-col md="4">
            <b-form-select
              id="quality_concerns"
              v-model="record.quality_concert"
              :options="quality_concern_codes"
              value-field="code"
              text-field="description"
              required/>
          </b-col>

          <b-col md="2">
            <label for="productivity">Productivity</label>
          </b-col>
          <b-col md="4">
            <b-form-select
              id="productivity"
              v-model="record.productivity"
              :options="productivity_codes"
              value-field="code"
              text-field="description"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="2">
            <label for="area">Size (km²)</label>
          </b-col>
          <b-col md="4">
            <b-form-input
              id="area"
              type="text"
              v-model="record.area"
              required/>
          </b-col>

          <b-col md="2">
            <label for="demand">Demand</label>
          </b-col>
          <b-col md="4">
            <b-form-select
              id="demand"
              v-model="record.demand"
              :options="demand_codes"
              value-field="code"
              text-field="description"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="3">
            <label for="known_water_use">Type of known water use</label>
          </b-col>
          <b-col md="3">
            <b-form-select
              id="known_water_use"
              v-model="record.known_water_use"
              :options="known_water_use_codes"
                value-field="code"
              text-field="description"
              required/>
          </b-col>
        </b-form-row>

        <b-form-row class="mt-3">
          <b-col md="6">
            <b-row>
              <b-col>
                <label for="notes">Comments</label>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-textarea
                  rows="4"
                  id="notes"
                  v-model="record.notes"/>
              </b-col>
            </b-row>
          </b-col>
        </b-form-row>

        <b-row class="mt-4">
          <b-col cols="auto">
            <b-button variant="secondary" v-on:click.prevent="save()">
              Save
            </b-button>

            <b-button variant="secondary" v-on:click.prevent="">
              Cancel
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-card>

    <b-modal id="confirmSave">
      <p>Are you sure you would like to save this record?</p>
    </b-modal>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'

export default {
  components: {
    'api-error': APIErrorMessage
  },
  created() {
    this.fetch()
    this.fetchCodes()
  },
  data() {
    return {
      loading: false,
      error: undefined,
      record: {},
      material_codes: [],
      quality_concern_codes: [],
      vulnerability_codes: [],
      subtype_codes: [],
      productivity_codes: [],
      demand_codes: [],
      known_water_use_codes: []
    }
  },
  methods: {
    save(id = this.id) {
      ApiService.post(`aquifers/${id}`, this.record)
        .catch((error) => this.error = error.response)
    },
    fetch(id = this.id) {
      this.loading = true
      this.error = undefined

      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        })
        .then(() => this.loading = false)
        .catch((error) => this.error = error.response)
    },
    fetchCodes() {
      ApiService.query(`aquifer-codes/materials`)
        .then((response) => {
          this.material_codes = response.data.results
        })

      ApiService.query(`aquifer-codes/quality-concerns`)
        .then((response) => {
          this.quality_concern_codes = response.data.results
        })

      ApiService.query(`aquifer-codes/vulnerability`)
        .then((response) => {
          this.vulnerability_codes = response.data.results
        })

      ApiService.query(`aquifer-codes/subtypes`)
        .then((response) => {
          this.subtype_codes = response.data.results
        })

      ApiService.query(`aquifer-codes/productivity`)
        .then((response) => {
          this.productivity_codes = response.data.results
        })

      ApiService.query(`aquifer-codes/demand`)
        .then((response) => {
          this.demand_codes = response.data.results
        })

      ApiService.query(`aquifer-codes/water-use`)
        .then((response) => {
          this.known_water_use_codes = response.data.results
        })
    }
  },
  props: ['id']
}
</script>
