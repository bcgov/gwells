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
      v-on:submit.prevent="updateQueryParams"
      v-on:reset="reset">
      <b-form-row>
        <b-col cols="12" md="4">
          <b-form-group label="Aquifer name">
            <b-form-input
              id="search"
              type="text"
              v-model="searchParams.search"/>
          </b-form-group>
          <b-form-group label="Aquifer number">
            <b-form-input
              id="aquifer_id"
              type="text"
              v-model="searchParams.aquifer_id"/>
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
      striped
      v-if="aquiferList"
      :show-empty="emptyResults"
      empty-text="No aquifers could be found"
      :items="aquiferList"
      :fields="aquiferListFields">
      <template slot="aquifer_id" slot-scope="data">
        <router-link :to="`${data.value}/`">{{data.value}}</router-link>
      </template>
    </b-table>

    <b-container v-if="displayPagination">
      <b-row align-h="end">
        <b-pagination :total-rows="response.count" :per-page="limit" v-model="currentPage" />
      </b-row>
    </b-container>

  </b-card>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { isNil, isEmpty, omitBy } from 'lodash'

const LIMIT = 30

export default {
  data () {
    return {
      limit: LIMIT,
      currentPage: undefined,
      searchParams: Object.assign({}, this.$route.query),
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
        { key: 'mapping_year', label: 'Year of mapping' }
      ]
    }
  },
  computed: {
    aquiferList () { return this.response && this.response.results },
    displayPagination () { return this.aquiferList && (this.response.next || this.response.previous) },
    emptyResults () { return this.response && this.response.count === 0 },
    query () { return this.$route.query }
  },
  methods: {
    fetchResults (query) {
      if (isEmpty(query)) {
        return
      }

      ApiService.query('aquifers/', query)
        .then((response) => {
          this.response = response.data
          this.scrollToTableTop()
        })
    },
    reset () {
      this.response = {}
      this.searchParams = {
        search: '',
        aquifer_id: ''
      }

     this.updateQueryParams()
    },
    scrollToTableTop () {
      this.$SmoothScroll(this.$el, 100)
    },
    updateQueryParams () {
      this.$router.replace({
        query: omitBy(this.searchParams, isNil)
      })
    }
  },
  mounted () {
    this.fetchResults(this.query)
  },
  watch: {
    query (query) {
      this.fetchResults(query)
    },
    currentPage (currentPage) {
      const i = (currentPage || 1) - 1

      this.searchParams.limit = LIMIT
      this.searchParams.offset = i * LIMIT

      this.updateQueryParams()
    }
  }
}
</script>
