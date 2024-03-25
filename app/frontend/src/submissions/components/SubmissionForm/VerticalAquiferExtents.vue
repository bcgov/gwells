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
  <fieldset class="vertical-aquifer-extents">
    <legend :id="id">Well {{wellTagNumber}}'s Vertical Aquifer Extents</legend>

    <div v-if="loading">
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"/>
      </div>
    </div>
    <div v-else>
      <api-error v-if="error" :error="error"/>

      <b-table
        :fields="tableFields"
        :items="tableData"
        show-empty
        empty-text="There are currently no vertical aquifer extents for this well.">
        <template v-slot:cell(start)="data">{{parseFloat(data.item.start).toFixed(2)}} m</template>
        <template v-slot:cell(end)="data">{{parseFloat(data.item.end).toFixed(2)}} m</template>
        <template v-slot:cell(height)="data">{{data.item.height.toFixed(2)}} m</template>
      </b-table>

      <div>
        <router-link :to="{ name: 'well-aquifers', params: {wellTagNumber} }" class="btn btn-primary" role="button">
          <i class="fa fa-edit"/>
          {{this.aquifers.length > 0 ? 'Edit' : 'Add'}}
        </router-link>
      </div>
    </div>
  </fieldset>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'

export default {
  props: {
    id: {
      type: String
    },
    wellTagNumber: {
      type: Number
    }
  },
  components: {
    'api-error': APIErrorMessage
  },
  data () {
    return {
      error: null,
      loading: false,
      aquifers: [],
      tableFields: [
        {
          key: 'aquifer_id',
          label: 'Aquifer Id'
        },
        {
          key: 'aquifer_name',
          label: 'Aquifer Name'
        },
        {
          key: 'start',
          label: 'Start'
        },
        {
          key: 'end',
          label: 'End'
        },
        {
          key: 'height',
          label: 'Height'
        }
      ]
    }
  },
  computed: {
    tableData () {
      return this.aquifers.map((aquifer) => {
        return {
          ...aquifer,
          height: parseFloat(aquifer.end) - parseFloat(aquifer.start)
        }
      })
    }
  },
  methods: {
    fetchAquifersForWell () {
      this.loading = true
      return ApiService.query(`wells/${this.wellTagNumber}/vertical-aquifer-extents`)
        .then((response) => {
          this.loading = false
          this.aquifers = response.data
        }).catch((e) => {
          this.loading = false
          this.error = e.response
          if (this.error && this.error.status === 404) {
            this.errorNotFound = true
          }
        })
    }
  },
  created () {
    if (this.wellTagNumber === null) {
      this.error = `Unable to load well '${this.wellTagNumber}'`
      return
    }

    this.fetchAquifersForWell()
  }
}
</script>

<style lang="scss">
</style>
