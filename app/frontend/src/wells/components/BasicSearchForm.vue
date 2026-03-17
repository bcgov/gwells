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
  <b-form @submit.prevent="handleSubmit()" @reset.prevent="handleReset()">
    <b-row>
      <b-col>
        <b-form-group>
          <form-input id="id_search" group-class="font-weight-bold" v-model="searchString">
            <label>
              Search by well tag or ID plate number, street address, city or owner name
              <b-badge pill variant="primary" id="basicSearchInfo" tabindex="0"><i class="fa fa-question fa-lg"></i></b-badge>
              <b-popover target="basicSearchInfo" triggers="hover focus" content="Enter the well electronic filing number or physical identification plate number, or the street address, city or well owner name."></b-popover>
            </label>
          </form-input>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row class="my-3">
      <b-col>
        <b-btn variant="primary" type="submit" :disabled="searchInProgress">Search</b-btn>
        <b-btn variant="dark" type="reset" :disabled="searchInProgress" class="mx-2">Reset</b-btn>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <well-exports/>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <p>For additional search options, try:</p>
        <ul>
          <li><a href="http://maps.gov.bc.ca/ess/hm/wrbc/" id="BCWRAtlas" target="_blank">B.C. Water Resource Atlas</a></li>
          <li><a href="http://maps.gov.bc.ca/ess/hm/imap4m/" id="iMapBC" target="_blank">iMapBC</a></li>
        </ul>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
import { mapGetters } from 'vuex'
import { SEARCH_WELLS } from '@/wells/store/actions.types.js'
import { SET_SEARCH_PARAMS } from '@/wells/store/mutations.types.js'
import { SEARCH_TRIGGER } from '@/wells/store/triggers.types.js'
import Exports from '@/wells/components/Exports.vue'

export default {
  components: {
    'well-exports': Exports
  },
  data () {
    return {
      searchString: null
    }
  },
  computed: {
    ...mapGetters(['searchParams', 'searchInProgress'])
  },
  methods: {
    handleSubmit () {
      const params = { search: this.searchString }
      this.$store.commit(SET_SEARCH_PARAMS, params)

      this.$store.dispatch(SEARCH_WELLS, { trigger: SEARCH_TRIGGER, constrain: true })

      this.$emit('search', params)
    },
    handleReset () {
      this.$emit('reset')
    },
    updateSearchString () {
      const searchString = this.searchParams.search
      this.searchString = searchString || null
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
