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
        <b-col xs="12">
          <legend :id="id">
            Person Responsible for Work
          </legend>
        </b-col>
        <b-col xs="12">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <b-form-checkbox id="checkbox1"
        v-model="drillerSameAsPersonResponsibleInput"
        :value="true"
        :unchecked-value="false"
      >
      <p>Person Responsible is the same as the Person Who Completed the Work</p>
      </b-form-checkbox>
      <b-row>
        <b-col cols="12" md="12" lg="6">
          <b-form-group
              label="Person Responsible for Work *"
              aria-describedby="personResponsibleInvalidFeedback"
              :state="false"
          >
            <v-select
                :class="errors.person_responsible?'border border-danger dropdown-error-border':''"
                :disabled="persons === null"
                id="personResponsibleSelect"
                :filterable="false"
                :options="personOptions"
                label="name"
                v-model="personResponsibleInput"
                @search="onPersonSearch"
                ref="personResponsible"
                @search:blur="handleSearchBlur(personOptions, $refs.personResponsible, 'personResponsibleInput')">
              <template slot="no-options">
                  Type to search registry...
              </template>
              <template slot="selected-option" slot-scope="option">
                <div>
                  {{ personNameReg (option) }}
                </div>
              </template>
              <template slot="option" slot-scope="option">
                <div>
                  {{ personNameReg (option) }}
                </div>
              </template>
            </v-select>
            <small id="personResponsibleSelectHint" class="form-text text-muted">
              *displays a maximum of {{MAX_RESULTS}} results
            </small>
            <b-form-text id="personResponsibleInvalidFeedback" v-if="errors.person_responsible">
              <div v-for="(error, index) in errors.person_responsible" :key="`personResponsible error ${index}`" class="text-danger">
                {{ error }}
              </div>
            </b-form-text>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="12" lg="6">
          <form-input
              id="drillerName"
              label="Person Who Completed the Work"
              type="text"
              :disabled="drillerSameAsPersonResponsible"
              v-model="drillerNameInput"
              :errors="errors['driller_name']"
              :loaded="fieldsLoaded['driller_name']"
          ></form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="12" lg="4">
          <b-form-group
              aria-describedby="companyOfPersonResponsibleInvalidFeedback"
              :state="false">
            <label>Company of person Responsible for Drilling</label>
            <v-select
              :disabled="companies === null"
              id="companyOfPersonResponsibleSelect"
              :filterable="false"
              :options="companyOfPersonResponsibleOptions"
              label="org_verbose_name"
              v-model="companyOfPersonResponsibleInput"
              @search="onCompanyOfPersonResponsibleSearch"
              ref="companyOfPersonResponsible"
              @search:blur="handleSearchBlur(companyOfPersonResponsibleOptions, $refs.companyOfPersonResponsible, 'companyOfPersonResponsibleInput')">
              <template slot="no-options">
                  Search by company name
              </template>
            </v-select>
            <small id="companyOfPersonResponsibleSelectHint" class="form-text text-muted">
              *displays a maximum of {{MAX_RESULTS}} results
            </small>
            <b-form-text id="companyOfPersonResponsibleInvalidFeedback" v-if="errors.person_responsible">
              <div v-for="(error, index) in errors.driller_company_responsible" :key="`companyOfPersonResponsible error ${index}`" class="text-danger">
                {{ error }}
              </div>
            </b-form-text>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input
              id="consultantName"
              label="Consultant Name"
              type="text"
              v-model="consultantNameInput"
              :errors="errors['consultant_name']"
              :loaded="fieldsLoaded['consultant_name']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="consultantCompany"
              label="Consultant Company"
              type="text"
              v-model="consultantCompanyInput"
              :errors="errors['consultant_company']"
              :loaded="fieldsLoaded['consultant_company']"
          ></form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'PersonResponsible',
  mixins: [inputBindingsMixin],
  props: {
    personResponsible: Object,
    companyOfPersonResponsible: Object,
    drillerName: String,
    consultantName: String,
    consultantCompany: String,
    drillerSameAsPersonResponsible: Boolean,
    id: {
      type: String,
      isInput: false
    },
    errors: {
      type: Object,
      default: () => ({}),
      inInput: true
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({}),
      inInput: true
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
  data () {
    return {
      personOptions: [],
      persons: null,
      companyOfPersonResponsibleOptions: [],
      companies: null,
      MAX_RESULTS: 50
    }
  },
  computed: {
    ...mapGetters(['userRoles'])
  },
  methods: {
    onPersonSearch (search, loading) {
      this.personOptions = this.genericSearch(search, this.persons, (item, search) => {
        const name = item.name
        // On some browsers indexOf is faster than contains and vice versa. The trends seems to be that indexOf is faster
        return name != null && name.toUpperCase().indexOf(search) !== -1
      })
    },
    onCompanyOfPersonResponsibleSearch (search, loading) {
      this.companyOfPersonResponsibleOptions = this.genericSearch(search, this.companies, (item, search) => {
        // On some browsers indexOf is faster than contains and vice versa. The trends seems to be that indexOf is faster
        return (item.name != null && item.name.toUpperCase().indexOf(search) !== -1) || (item.org_verbose_name != null && item.org_verbose_name.toUpperCase().indexOf(search) !== -1)
      })
    },
    /**
     * Get a list of matches.
     * @param {string} needle - The string being searched for.
     * @param {array} haystack - A list of objects to search.
     * @param {function} match - The function to evaluate if a needle matches an item in the list.
     * @return {array} Up to MAX_RESULT matching objects.
     */
    genericSearch (needle, haystack, match) {
      const result = []
      if (needle && needle.length >= 1 && haystack) {
        needle = needle.toUpperCase()
        for (let i = 0; i < haystack.length && result.length < this.MAX_RESULTS; ++i) {
          if (match(haystack[i], needle)) {
            result.push(haystack[i])
          }
        }
      }
      return result
    },
    /**
     * Select the highlighted option in the dropdown as the input field.
     * @param {array} options - List of objects.
     * @param {object} ref - Reference to v-select component.
     * @param {string} inputName - Name of property on this component to set with the highlighted item.
     */
    handleSearchBlur (options, ref, inputName) {
      if (options && ref.typeAheadPointer < options.length) {
        this[inputName] = options[ref.typeAheadPointer]
      }
    },
    personNameReg (option) {
      const drillReg = option.registrations.find((item) => {
        return item.registries_activity === 'DRILL'
      })
      const drillNo = (drillReg && drillReg.registration_no) ? drillReg.registration_no : 'Registration Number Unavailable'
      return option.name + ' (' + drillNo + ')'
    }
  },
  watch: {
    personResponsible (val, prev) {
      // reset list of people when user finished selecting a person
      this.personOptions = []
      if (prev) {
        this.drillerSameAsPersonResponsibleInput = false
      }
      this.drillerNameInput = (this.personResponsible && this.drillerSameAsPersonResponsible) ? this.personResponsible.name : ''
    },
    drillerSameAsPersonResponsible (val) {
      // keep driller name disabled & set to "person responsible", or leave it enabled and blank
      this.drillerNameInput = (this.personResponsible && this.drillerSameAsPersonResponsible) ? this.personResponsible.name : ''
    }
  },
  created () {
    ApiService.query(`drillers/names/`).then((response) => {
      this.persons = response.data
    })
    ApiService.query('organizations/names/').then((response) => {
      this.companies = response.data
    })
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
.v-select i.open-indicator {
  width: 0px;
  visibility: hidden;
}
</style>
