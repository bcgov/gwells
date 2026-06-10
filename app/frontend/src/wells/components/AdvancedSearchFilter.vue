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
  <div class="grid grid-cols-12 advanced-search-filter mb-2" :class="`advanced-search-filter-${type}`">
    <div v-if="label" :class="`col-span-12 sm:col-span-${labelColWidth}`">
      <label v-if="(type === 'text' || type === 'number' || type === 'select') && !anyValueCheckbox" :id="`${id}Label`" :label-for="`${id}Input`" class="col-form-label">{{ label }}</label>
      <legend v-else tabindex="-1" :id="`${id}Label`" class="col-form-label">{{ label }}</legend>
    </div>
    <div v-if="anyValueCheckbox" class="col-span-12 sm:col-span-3">
      <div class="pt-2 flex sm:justify-end">
        <div class="flex items-center gap-2">
          <Checkbox :inputId="`${id}AnyValue`" v-model="modelValue[anyValueParam]" @input="updateAnyValueCheckbox($event)" binary/>
          <label :for="`${id}AnyValue`">Any value</label>
        </div>
      </div>
    </div>
    <div :class="`col-span-12 sm:col-span-${inputColWidth}`">
      <InputText
        v-if="type === 'text' || type === 'number'"
        :type="type"
        :id="`${id}Input`"
        :modelValue="modelValue[paramNames[0]]"
        :invalid="isInvalid"
        :disabled="inputDisabled"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder"
        @input="updateParamValue(paramNames[0], $event)"
        @focus="$emit('focus', true)"
        @blur="$emit('blur', true)" />
      <Select 
        v-else-if="type === 'select'"
        :id="`${id}Input`"
        :modelValue="modelValue[paramNames[0]] ? modelValue[paramNames[0]] : null"
        :invalid="isInvalid"
        :disabled="inputDisabled"
        :aria-describedby="`${id}InvalidFeedback`"
        :options="selectOptions"
        :optionValue="valueField"
        :optionLabel="textField"
        @input="updateParamValue(paramNames[0], $event)"
        @focus="$emit('focus', true)"
        @blur="$emit('blur', true)"
        :placeholder="placeholder || '----------'"/>
      <!--
      <RadioButtonGroup v-else-if="type === 'radio'" :id="`${id}Input`">
        <div v-for="option in options" class="flex align-items-center">

        </div>
      </RadioButtonGroup>
      <b-form-radio-group
        v-else-if="type === 'radio'"
        :id="`${id}Input`"
        :checked="modelValue[paramNames[0]]"
        :state="validation"
        :disabled="inputDisabled"
        :aria-describedby="`${id}InvalidFeedback`"
        :options="options"
        @input="updateParamValue(paramNames[0], $event)"
        @focus="$emit('focus', true)"
        @blur="$emit('blur', true)" />
      -->
      <div v-else-if="type === 'range' || type === 'dateRange'">
        <div class="mb-1">
          <div class="grid grid-cols-12">
            <label :id="`${id}StartLabel`" :label-for="`${id}StartInput`" class="sm:col-span-4 col-form-label sm:text-right">From</label>
            <div class="sm:col-span-8">
              <InputText
                v-if="type === 'range'"
                type="number"
                step="any"
                :id="`${id}StartInput`"
                :modelValue="modelValue[paramNames[0]]"
                :invalid="isInvalid"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                :placeholder="placeholder"
                @input="updateParamValue(paramNames[0], $event)"
                @focus="$emit('focus', true)"
                @blur="$emit('blur', true)" />
              <InputText
                v-else-if="type === 'dateRange'"
                type="date"
                :id="`${id}StartInput`"
                :modelValue="modelValue[paramNames[0]]"
                :invalid="isInvalid"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                placeholder="YYYY/MM/DD"
                @input="updateParamValue(paramNames[0], $event)"
                @focus="$emit('focus', true)"
                @blur="$emit('blur', true)" />
            </div>
          </div>
        </div>
        <div class="mb-1">
          <div class="grid grid-cols-12">
            <label :id="`${id}EndLabel`" :for="`${id}EndInput`" class="sm:col-span-4 col-form-label sm:text-right">To</label>
            <div class="col-span-8">
              <InputText
                v-if="type === 'range'"
                type="number"
                step="any"
                :id="`${id}EndInput`"
                :modelValue="modelValue[paramNames[1]]"
                :invalid="isInvalid"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                :placeholder="placeholder"
                @input="updateParamValue(paramNames[1], $event)"
                @focus="$emit('focus', true)"
                @blur="$emit('blur', true)" />
              <InputText
                v-else-if="type === 'dateRange'"
                type="date"
                :id="`${id}EndInput`"
                :modelValue="modelValue[paramNames[1]]"
                :invalid="isInvalid"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                placeholder="YYYY/MM/DD"
                @input="updateParamValue(paramNames[1], $event)"
                @focus="$emit('focus', true)"
                @blur="$emit('blur', true)" />
            </div>
          </div>
        </div>
      </div>
      <div :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" class="mt-1 text-sm text-red-600" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </div>
    </div>
    <div class="col-span-1" v-if="removable">
      <Button icon="fa fa-times" severity="secondary" variant="text" rounded aria-label="Remove" @click="$emit('remove')" class="pt-1"/>
    </div>
  </div>
</template>

<script>
/**
 * example usage in another component:
 *
 * <advanced-search-filter
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
    label: String,
    errors: null, // pass any "field errors" returned by the API into the "errors" prop
    modelValue: Object, // internal (holds the values for the field)
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
    placeholder: String,
    removable: {
      type: Boolean,
      default: false
    },
    anyValueCheckbox: {
      type: Boolean,
      default: false
    }
  },
  emits: ['focus', 'blur', 'update:modelValue'],
  data () {
    return {}
  },
  computed: {
    isInvalid () {
      return (this.errors && this.errors.length)
    },
    labelColWidth () {
      if (!this.anyValueCheckbox && (this.type === 'text' || this.type === 'select' || this.type === 'radio')) {
        return 6
      }
      return false
    },
    inputColWidth () {
      if (this.anyValueCheckbox) {
        return 6
      } else if (this.type === 'range' || this.type === 'dateRange') {
        return 8
      }
      return false
    },
    selectOptions () {
      if (this.options === undefined) {
        return []
      }
      return [...this.options]
    },
    anyValueParam () {
      return this.paramNames.slice(-1)[0]
    },
    inputDisabled () {
      return this.anyValueCheckbox && this.modelValue[this.anyValueParam] === true
    }
  },
  methods: {
    updateParamValue (param, value) {
      this.$emit('update:modelValue', { ...this.modelValue, [param]: value })
    },
    updateAnyValueCheckbox (value) {
      if (!this.anyValueCheckbox) {
        return
      }

      if (value === true) {
        this.$emit('update:modelValue', { [this.anyValueParam]: true })
      } else {
        this.$emit('update:modelValue', {})
      }
    }
  }
}
</script>

<style lang="scss">
</style>
