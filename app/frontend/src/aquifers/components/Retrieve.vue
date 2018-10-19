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
    <b-container>
      <b-row>
        <b-col><h5>Aquifer Summary</h5></b-col>
        <b-col cols="auto">
            <b-button variant="secondary" v-on:click.prevent="print()">
              <span title="Print" class="fa-print"/>
            </b-button>
        </b-col>
      </b-row>

      <dl class="row">
        <dt class="col-sm-2">Aquifer number</dt>
        <dd class="col-sm-4">{{record.aquifer_id}}</dd>
        <dt class="col-sm-2">Year of mapping</dt>
        <dd class="col-sm-4">{{record.mapping_year}}</dd>

        <dt class="col-sm-2">Aquifer name</dt>
        <dd class="col-sm-4">{{record.aquifer_name}}</dd>
        <dt class="col-sm-2">Litho stratigraphic unit</dt>
        <dd class="col-sm-4">{{record.litho_stratographic_unit}}</dd>

        <dt class="col-sm-2">Descriptive location</dt>
        <dd class="col-sm-4">{{record.descriptive_location}}</dd>
        <dt class="col-sm-2">Vulnerability</dt>
        <dd class="col-sm-4">{{record.vulnerability_description}}</dd>

        <dt class="col-sm-2">Material type</dt>
        <dd class="col-sm-4">{{record.material_location}}</dd>
        <dt class="col-sm-2">Subtype</dt>
        <dd class="col-sm-4">{{record.subtype_description}}</dd>

        <dt class="col-sm-2">Quality concerns</dt>
        <dd class="col-sm-4">{{record.quality_concern_description}}</dd>
        <dt class="col-sm-2">Productivity</dt>
        <dd class="col-sm-4">{{record.productivity_description}}</dd>

        <dt class="col-sm-2">Size (km²)</dt>
        <dd class="col-sm-4">{{record.area}}</dd>
        <dt class="col-sm-2">Demand</dt>
        <dd class="col-sm-4">{{record.demand_description}}</dd>
      </dl>
    </b-container>
  </b-card>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'

export default {
  props: ['id'],
  created () { this.fetch() },
  data () {
    return {
      record: {}
    }
  },
  watch: {
    id () { this.fetch() }
  },
  methods: {
    print () {
      window.print()
    },
    fetch (id = this.id) {
      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        })
    }
  }
}
</script>
