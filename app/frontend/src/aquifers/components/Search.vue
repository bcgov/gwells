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
  <b-card no-body class="p-3 mb-4">
    <h5>Aquifer Search</h5>
    <b-form
      v-on:submit.prevent="search(query)"
      v-on:reset="reset">
      <b-form-row>
        <b-col cols="12" md="4">
          <b-form-group label="Aquifer name">
            <b-form-input
              type="text"
              v-model="query.search"/>
          </b-form-group>
          <b-form-group label="Aquifer number">
            <b-form-input
              type="text"
              v-model="query.aquifer_id"/>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col>
          <b-form-group>
            <b-button variant="primary" type="submit">Search</b-button>
            <b-button variant="default" type="reset">Reset</b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
    </b-form>

    <b-table
      v-if="aquiferList"
      :show-empty="emptyResults"
      empty-text="No aquifers could be found"
      :items="aquiferList"
      :fields="aquiferListFields">
      <template slot="aquifer_id" slot-scope="data">
        <router-link :to="`${data.value}/`">{{data.value}}</router-link>
      </template>
    </b-table>
  </b-card>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'

export default {
  data() {
    return {
      query: {},
      response: {},
      aquiferListFields: [
        { key: 'aquifer_id', label: 'Aquifer number' },
        { key: 'aquifer_name', label: 'Aquifer name' },
        { key: 'location_description', label: 'Descriptive location' },
        { key: 'material_description', label: 'Material' },
        { key: 'litho_stratographic_unit', label: 'Litho stratigraphic unit' },
        { key: 'subtype_description', label: 'Subtype' },
        { key: 'vulnerability_description', label: 'Vulnerability' },
        { key: 'area', label: 'Size-km²' },
        { key: 'productivity_description', label: 'Productivity' },
        { key: 'demand_description', label: 'Demand' },
        { key: 'mapping_year', label: 'Year of mapping' },
        { key: 'publication_status', label: 'Publication status' }
      ]
    }
  },
  computed: {
    aquiferList() { return this.response && this.response.results },
    emptyResults() { return this.response && this.response.count == 0 }
  },
  methods: {
    reset() {
      this.response = {}
      this.query = {}
    },
    search() {
      ApiService.query('aquifers/', this.query)
        .then((response) => {
          this.response = response.data
        })
    }
  }
}
</script>
