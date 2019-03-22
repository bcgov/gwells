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
        <b-btn variant="primary" type="submit">Search</b-btn>
        <b-btn variant="dark" type="reset" class="mx-2">Reset</b-btn>
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
            <li><a href="http://maps.gov.bc.ca/ess/hm/wrbc/" id="BCWRAtlas">B.C. Water Resource Atlas</a></li>
            <li><a href="http://maps.gov.bc.ca/ess/hm/imap4m/" id="iMapBC">iMapBC</a></li>
        </ul>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
import { mapGetters } from 'vuex'
import { RESET_WELLS_SEARCH, SEARCH_WELLS, SEARCH_WELL_LOCATIONS } from '@/wells/store/actions.types.js'
import { SET_SEARCH_PARAMS } from '@/wells/store/mutations.types.js'
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
    ...mapGetters(['searchParams'])
  },
  methods: {
    handleSubmit () {
      if (this.searchString === null || this.searchString === '') {
        return
      }
      const params = { search: this.searchString }
      this.$store.commit(SET_SEARCH_PARAMS, params)
      this.$store.dispatch(SEARCH_WELLS, {})
      this.$store.dispatch(SEARCH_WELL_LOCATIONS, {})

      this.$emit('search', params)
    },
    handleReset () {
      this.searchString = null
      this.$store.dispatch(RESET_WELLS_SEARCH)

      this.$emit('reset')
    },
    initSearchString () {
      const searchString = this.searchParams.search
      if (searchString !== undefined && searchString !== '' && searchString !== null) {
        this.searchString = searchString
      }
    }
  },
  created () {
    this.initSearchString()
  }
}
</script>

<style>
</style>
