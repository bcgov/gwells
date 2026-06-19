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
  <Form @submit="handleSubmit()" @reset="handleReset()">
    <div>
      <div>
        <form-input id="id_search" group-class="font-weight-bold" v-model="searchString">
          <label>
            Search by well tag or ID plate number, street address, city or owner name
            <Badge
              id="basicSearchInfo"
              tabindex="0"
              class="fa fa-question fa-lg"
              v-tooltip.top="'Enter the well electronic filing number or physical identification plate number, or the street address, city or well owner name.'"
              @focus="show"
              @blur="hide"/>
          </label>
        </form-input>
      </div>
    </div>
    <div class="my-4">
      <div>
        <Button label="Search" type="submit" :disabled="searchInProgress"/>
        <Button label="Reset" severity="contrast" type="reset" :disabled="searchInProgress" class="mx-2"/>
      </div>
    </div>
    <div class="flex flex-col">
      <well-exports/>
    </div>
    <div class="flex flex-col">
      <p>For additional search options, try:</p>
      <ul>
        <li><a href="http://maps.gov.bc.ca/ess/hm/wrbc/" id="BCWRAtlas" target="_blank">B.C. Water Resource Atlas</a></li>
        <li><a href="http://maps.gov.bc.ca/ess/hm/imap4m/" id="iMapBC" target="_blank">iMapBC</a></li>
      </ul>
    </div>
  </Form>
</template>

<script>
import { mapStores } from 'pinia'
import { Badge, Popover } from 'primevue'
import { useWellsStore } from '@/stores/wells.js'
import { SEARCH_TRIGGER } from '@/wells/triggers.types.js'
import Exports from '@/wells/components/Exports.vue'

export default {
  components: {
    'well-exports': Exports,
    Badge,
    Popover
  },
  data () {
    return {
      searchString: null,
      wells: null
    }
  },
  computed: {
    ...mapStores(useWellsStore),
    searchParams () {
      return this.wellsStore ? this.wellsStore.searchParams : {}
    },
    searchInProgress () {
      return this.wellsStore ? this.wellsStore.searchInProgress : false
    }
  },
  methods: {
    handleSubmit () {
      const params = { search: this.searchString }
      this.wellsStore.setSearchParams(params)

      this.wellsStore.searchWells({ trigger: SEARCH_TRIGGER, constrain: true })

      this.$emit('search', params)
    },
    handleReset () {
      this.$emit('reset')
    },
    updateSearchString () {
      const searchString = this.searchParams?.search
      this.searchString = searchString || null
    },
    show () {
      this.$refs.basicSearchInfo.show()
    },
    hide () {
      this.$refs.basicSearchInfo.hide()
    }
  },
  watch: {
    searchParams (params = {}) {
      this.updateSearchString()
    }
  },
  created () {
    this.updateSearchString()
  }
}
</script>

<style>
</style>
