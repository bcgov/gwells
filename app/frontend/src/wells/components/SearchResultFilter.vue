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
  <div class="search-result-filter" :class="`search-result-filter-${type}`">
    <div v-if="type === 'text' || type === 'number' || type === 'select' || type === 'radio'">
      <InputText
        v-if="type === 'text'"
        type="text"
        :id="`${id}Input`"
        :invalid="isInvalid"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder || 'Filter...'"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter()" />
      <InputText
        v-else-if="type === 'number'"
        type="text"
        :id="`${id}Input`"
        :invalid="isInvalid"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder || 'Filter...'"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter()" />
      <Select
        v-else-if="type === 'select' || type === 'radio'"
        :id="`${id}Input`"
        :invalid="isInvalid"
        :aria-describedby="`${id}InvalidFeedback`"
        :disabled="isActive"
        :options="selectOptions"
        :optionValue="valueField"
        :optionLabel="textField"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter()" />
      <div :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" class="mt-1 text-sm text-red-600" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </div>
    </div>
    <div class="sm:col-span-5" v-if="type === 'range' || type === 'dateRange'">
      <InputText
        :type="`${ type === 'range' ? 'number' : 'date'}`"
        :id="`${id}StartInput`"
        :invalid="isInvalid"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="`${ type === 'range' ? 'From' : 'YYYY/MM/DD'}`"
        :disabled="isActive"
        v-model="localValue[paramNames[0]]"
        @keyup.enter="applyFilter()" />
    </div>
    <div class="sm:col-span-5" v-if="type === 'range' || type === 'dateRange'">
      <InputText
        :type="`${ type === 'range' ? 'number' : 'date'}`"
        :id="`${id}EndInput`"
        :invalid="isInvalid"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="`${ type === 'range' ? 'To' : 'YYYY/MM/DD'}`"
        :disabled="isActive"
        v-model="localValue[paramNames[1]]"
        @keyup.enter="applyFilter()" />
    </div>
    <div :class="`sm:col-span-${(type === 'text') ? 3 : 2}`">
      <Button
        variant="link"
        class="py-2 px-0"
        :class="{'apply-filter': !isActive, 'clear-filter': isActive}"
        :disabled="!hasLocalValue"
        @click="isActive ? clearFilter() : applyFilter()"
        :icon="`fa fa-lg ${isActive ? 'fa-times' : 'fa-check'}`"
        :aria-label="isActive ? 'Clear' : 'Apply'"/>
    </div>
  </div>
</template>

<script>
/**
 * example usage in another component:
 *
 * <search-result-filter
 *    id="ownerNameFilter"
 *    v-model="ownerNameInput"
 *    placeholder="Type a name!"
 *    :errors="errors['ownerName']"/>   // errors for individual fields must be an array e.g. ['Name already taken']
 *
 */
export default {
  props: {
    id: { // an ID for the form group that will be used to generate IDs for the related components
      required: true,
      type: String
    },
    paramNames: {
      required: true,
      type: Array
    },
    errors: null, // pass any "field errors" returned by the API into the "errors" prop
    value: Object, // internal (holds the values for the field)
    type: { // the type of filter (e.g. text, range, dateRange)
      type: String,
      default: 'text'
    },
    options: Array,
    valueField: {
      type: String,
      default: 'value'
    },
    textField: {
      type: String,
      default: 'text'
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
    isActive () {
      return (this.value !== undefined && this.paramNames.some(param => this.value[param]))
    },
    hasLocalValue () {
      return this.paramNames.some(param => this.localValue[param])
    },
    isInvalid () {
      return (Object.entries(this.value).length > 0 && this.errors && this.errors.length) ? true : false
    },
    selectOptions () {
      if (this.options === undefined) {
        return []
      }
      return [{ [this.textField]: 'Filter...', [this.valueField]: null }, ...this.options]
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
