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
  <div class="grid grid-cols-12 gap-2 search-result-filter" :class="`search-result-filter-${type}`">
    <div :class="`col-span-${type === 'text' ? 9 : 10}`" v-if="type === 'text' || type === 'number' || type === 'select' || type === 'radio' || type === 'nullcheck'">
      <InputText
        v-if="type === 'text'"
        type="text"
        :id="`${id}Input`"
        :invalid="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder || 'Filter...'"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter" />
      <InputText
        v-else-if="type === 'number'"
        type="text"
        :id="`${id}Input`"
        :invalid="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder || 'Filter...'"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter" />
      <Select
        v-else-if="type === 'select' || type === 'radio'"
        :id="`${id}Input`"
        :invalid="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :disabled="isActive"
        :options="selectOptions"
        :value-field="valueField"
        :text-field="textField"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter" />
      <!-- There isn't a replacement. Will need to redo error logic later.
      <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </b-form-invalid-feedback>
      -->
    </div>
    <div class="col-span-12" v-if="type === 'nullcheck'">
      <div>
        <Button
          class="py-2 px-4"
          :class="{'active-filter-border': isActive, 'active-filter': isActive}"
          @click="toggleNullFilter">
          Null Fields
          <span class="fa fa-sm mb-1 pl-1" :class="{'fa-check': !isActive, 'fa-times': isActive}" :aria-label="isActive ? 'Clear' : 'Apply'" />
        </Button>
      </div>
      <!-- There isn't a replacement. Will need to redo error logic later.
      <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </b-form-invalid-feedback>
      -->
    </div>
    <div class="col-span-5" v-if="type === 'range' || type === 'dateRange'">
      <InputText
        :type="`${ type === 'range' ? 'number' : 'date'}`"
        :id="`${id}StartInput`"
        :invalid="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="`${ type === 'range' ? 'From' : 'YYYY/MM/DD'}`"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter()" />
    </div>
    <div class="col-span-5" v-if="type === 'range' || type === 'dateRange'">
      <InputText
        :type="`${ type === 'range' ? 'number' : 'date'}`"
        :id="`${id}EndInput`"
        :invalid="validation"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="`${ type === 'range' ? 'To' : 'YYYY/MM/DD'}`"
        :disabled="isActive"
        v-model="localValue[paramNames[1]]"
        @keyup.enter="applyFilter" />
    </div>
    <div :class="`col-span-${type === 'text' ? 3 : 2}`" v-if="type !== 'nullcheck'">
      <Button
        variant="text"
        class="py-2 px-0"
        :class="{'apply-filter': !isActive, 'clear-filter': isActive}"
        :disabled="!hasLocalValue"
        @click="isActive ? clearFilter() : applyFilter()">
          <span class="fa fa-lg" :class="{'fa-check': !isActive, 'fa-times': isActive}" :aria-label="isActive ? 'Clear' : 'Apply'" />
      </Button>
    </div>
  </div>
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
  emits: ['input'],
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
      this.localValue[this.paramNames[0]] = 'null'
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

.p-inputtext {
  display: block;
  width: 100%;
  padding: .375rem .75rem;
  line-height: 1.5;
  background-clip: padding-box;
}
</style>
