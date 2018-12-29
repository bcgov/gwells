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
  <fieldset>
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Well Testing and Aquifer Details</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" md="6" xl="3">
        <b-form-group label="Associated aquifer">
          <v-select
            v-model="aquiferInput"
            id="aquiferSelect"
            :filterable="false"
            :options="aquiferList"
            label="description"
            index="aquifer_id"
            @search="onAquiferSearch">
            <template slot="no-options">
                Search for an aquifer by name or id number
            </template>
            <template slot="option" slot-scope="option">
              <div>
                {{ option.description }}
              </div>
            </template>
            <template slot="selected-option" slot-scope="option">
              <div>
                {{ option.description }}
              </div>
            </template>
          </v-select>
        </b-form-group>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import debounce from 'lodash.debounce'
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'

export default {
  mixins: [inputBindingsMixin, inputFormatMixin],
  props: {
    aquifer: null,
    id: {
      type: String,
      isInput: false
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  fields: {
    aquiferInput: 'aquifer'
  },
  data () {
    return {
      aquiferList: []
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    aquiferSearch: debounce((loading, search, vm) => {
      ApiService.query(`aquifers/names/?search=${escape(search)}`).then((response) => {
        vm.aquiferList = response.data
        loading(false)
      })
    }, 500),
    onAquiferSearch (search, loading) {
      loading(true)
      this.aquiferSearch(loading, search, this)
    }
  }
}
</script>

<style>

</style>
