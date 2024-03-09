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
  <b-form-row class="search-result-filter" :class="`search-result-filter-${type}`">
    <b-col v-if="type === 'text' || type === 'number' || type === 'select' || type === 'radio' || type === 'nullcheck'">
      <b-form-input
        v-if="type === 'text'"
        type="text"
        :id="`${id}Input`"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder || 'Filter...'"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter.native="applyFilter()" />
      <b-form-input
        v-else-if="type === 'number'"
        type="text"
        :id="`${id}Input`"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder || 'Filter...'"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter.native="applyFilter()" />
      <b-form-select
        v-else-if="type === 'select' || type === 'radio'"
        :id="`${id}Input`"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :disabled="isActive"
        :options="selectOptions"
        :value-field="valueField"
        :text-field="textField"
        v-model="localValue[paramNames[0]]"
        @keyup.enter.native="applyFilter()" />
      <b-col v-else-if="type === 'nullcheck'">
        <b-button
          variant="button"
          class="py-2 px-3"
          :class="{'active-filter-border': isActive, 'active-filter': isActive}"
          @click.prevent="toggleNullFilter">
          Null Fields
          <span class="fa fa-sm mb-1 pl-1" :class="{'fa-check': !isActive, 'fa-times': isActive}" :aria-label="isActive ? 'Clear' : 'Apply'" />
        </b-button>
      </b-col>
      <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </b-form-invalid-feedback>
    </b-col>
    <b-col sm="5" v-if="type === 'range' || type === 'dateRange'">
      <b-form-input
        :type="`${ type === 'range' ? 'number' : 'date'}`"
        :id="`${id}StartInput`"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="`${ type === 'range' ? 'From' : 'YYYY/MM/DD'}`"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter.native="applyFilter()" />
    </b-col>
    <b-col sm="5" v-if="type === 'range' || type === 'dateRange'">
      <b-form-input
        :type="`${ type === 'range' ? 'number' : 'date'}`"
        :id="`${id}EndInput`"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="`${ type === 'range' ? 'To' : 'YYYY/MM/DD'}`"
        :disabled="isActive"
        v-model="localValue[paramNames[1]]"
        @keyup.enter.native="applyFilter()" />
    </b-col>
    <b-col v-if="type !== 'nullcheck'" :sm="(type === 'text') ? 3 : 2">
      <b-button
        variant="link"
        class="py-2 px-0"
        :class="{'apply-filter': !isActive, 'clear-filter': isActive}"
        :disabled="!hasLocalValue"
        @click.prevent="isActive ? clearFilter() : applyFilter()">
          <span class="fa fa-lg" :class="{'fa-check': !isActive, 'fa-times': isActive}" :aria-label="isActive ? 'Clear' : 'Apply'" />
      </b-button>
    </b-col>
  </b-form-row>
</template>

<script>
export default {
  props: {
    id: { // an ID for the form group that will be used to generate IDs for the related components
      required: true,
      type: String
    },
    errors: null, // pass any "field errors" returned by the API into the "errors" prop
    value: Object, // internal (holds the values for the field)
    type: { // the type of filter (e.g. text, range, dateRange)
      type: String,
      default: 'text'
    },
    paramNames: {
      required: true,
      type: Array
    },
    options: Array,
    textField: {
      type: String,
      default: 'text'
    },
    valueField: {
      type: String,
      default: 'value'
    },
    placeholder: String
  },
  data () {
    return {
      localValue: this.getLocalValue()
    }
  },
  computed: {
    hasLocalValue () {
      return this.paramNames.some(param => this.localValue[param])
    },
    isActive () {
      return (this.value !== undefined && this.paramNames.some(param => this.value[param]))
    },
    selectOptions () {
      if (this.options === undefined) {
        return []
      }

      // Filter out options where the textField equals "Staff edit"
      let filteredOptions = this.options.filter(option => option[this.textField] !== 'Staff edit')

      // Determine the null value to use based on paramNames
      const nullValue = (this.paramNames[0] === 'well_subclass')
        ? '00000000-0000-0000-0000-000000000000'
        : 'null'

      return [
        { [this.textField]: 'Filter...', [this.valueField]: null },
        { [this.textField]: 'Null', [this.valueField]: nullValue },
        ...filteredOptions]
    },
    validation () {
      return (Object.entries(this.value).length > 0 && this.errors && this.errors.length) ? false : null
    }
  },
  methods: {
    getLocalValue () {
      const localValue = {}
      this.paramNames.forEach(paramName => {
        if (this.value && this.value[paramName]) {
          localValue[paramName] = this.value[paramName]
        } else {
          localValue[paramName] = null
        }
      })

      return localValue
    },
    toggleNullFilter () {
      // Check if the null filter is already applied
      if (this.localValue[this.paramNames[0]] === 'null') {
        // If yes, clear the filter
        this.clearFilter()
      } else {
        // If no, set the null filter
        this.applyNullFilter()
      }
    },
    applyNullFilter () {
      // Set the field to a special value that represents 'null'
      this.$set(this.localValue, this.paramNames[0], 'null')
      // Emit an update event (or directly apply the filter if handled within the component)
      this.applyFilter()
    },
    applyFilter () {
      if (this.hasLocalValue) {
        this.$emit('input', this.localValue)
      }
    },
    clearFilter () {
      const localValue = {}
      this.paramNames.forEach(paramName => {
        localValue[paramName] = null
      })
      this.localValue = localValue

      this.$emit('input', {})
    }
  },
  watch: {
    value (newValue, oldValue) {
      this.localValue = this.getLocalValue()
    }
  }
}
</script>

<style lang="scss">

.active-filter-border {
  border: 5px solid #007bff;
}

.active-filter {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.search-result-filter {
  min-width: 8rem;

  .btn-link:focus,
  .btn-link:active:focus
  {
    .fa {
      text-decoration: underline;
    }
  }
}

.search-result-filter.search-result-filter-select {
  min-width: 12rem;
}

.search-result-filter.search-result-filter-range {
  min-width: 14rem;
}

.search-result-filter.search-result-filter-dateRange {
  min-width: 20rem;
}
</style>
