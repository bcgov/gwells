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
  <b-form-row class="advanced-search-filter mb-2" :class="`advanced-search-filter-${type}`">
    <b-col v-if="label" :sm="labelColWidth">
      <label v-if="(type === 'text' || type === 'number' || type === 'select') && !anyValueCheckbox" :id="`${id}Label`" :label-for="`${id}Input`" class="col-form-label">{{ label }}</label>
      <legend v-else tabindex="-1" :id="`${id}Label`" class="col-form-label">{{ label }}</legend>
    </b-col>
    <b-col v-if="anyValueCheckbox" sm="3">
      <div class="pt-2 d-flex justify-content-sm-end">
        <b-form-checkbox
          :id="`${id}AnyValue`"
          :checked="value[anyValueParam]"
          @input="updateAnyValueCheckbox($event)">
          Any value
        </b-form-checkbox>
      </div>
    </b-col>
    <b-col :sm="inputColWidth">
      <b-form-input
        v-if="type === 'text' || type === 'number'"
        :type="type"
        :id="`${id}Input`"
        :value="value[paramNames[0]]"
        :state="validation"
        :disabled="inputDisabled"
        :aria-describedby="`${id}InvalidFeedback`"
        :placeholder="placeholder"
        @input="updateParamValue(paramNames[0], $event)"
        @focus.native="$emit('focus', true)"
        @blur.native="$emit('blur', true)" />
      <b-form-select
        v-else-if="type === 'select'"
        :id="`${id}Input`"
        :value="value[paramNames[0]] ? value[paramNames[0]] : null"
        :state="validation"
        :disabled="inputDisabled"
        :aria-describedby="`${id}InvalidFeedback`"
        :options="selectOptions"
        :value-field="valueField"
        :text-field="textField"
        @input="updateParamValue(paramNames[0], $event)"
        @focus.native="$emit('focus', true)"
        @blur.native="$emit('blur', true)">
        <template slot="first">
          <option :value="null">{{ placeholder || '----------' }}</option>
        </template>
      </b-form-select>
      <b-form-radio-group
        v-else-if="type === 'radio'"
        :id="`${id}Input`"
        :checked="value[paramNames[0]]"
        :state="validation"
        :disabled="inputDisabled"
        :aria-describedby="`${id}InvalidFeedback`"
        :options="options"
        @input="updateParamValue(paramNames[0], $event)"
        @focus.native="$emit('focus', true)"
        @blur.native="$emit('blur', true)" />
      <b-form-row v-else-if="type === 'range' || type === 'dateRange'">
        <b-col class="mb-1">
          <b-form-row>
            <label :id="`${id}StartLabel`" :label-for="`${id}StartInput`" class="col-sm-4 col-form-label text-sm-right">From</label>
            <b-col sm="8">
              <b-form-input
                v-if="type === 'range'"
                type="number"
                step="any"
                :id="`${id}StartInput`"
                :value="value[paramNames[0]]"
                :state="validation"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                :placeholder="placeholder"
                @input="updateParamValue(paramNames[0], $event)"
                @focus.native="$emit('focus', true)"
                @blur.native="$emit('blur', true)" />
              <b-form-input
                v-else-if="type === 'dateRange'"
                type="date"
                :id="`${id}StartInput`"
                :value="value[paramNames[0]]"
                :state="validation"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                placeholder="YYYY/MM/DD"
                @input="updateParamValue(paramNames[0], $event)"
                @focus.native="$emit('focus', true)"
                @blur.native="$emit('blur', true)" />
            </b-col>
          </b-form-row>
        </b-col>
        <b-col class="mb-1">
          <b-form-row>
            <label :id="`${id}EndLabel`" :label-for="`${id}EndInput`" class="col-sm-4 col-form-label text-sm-right">To</label>
            <b-col sm="8">
              <b-form-input
                v-if="type === 'range'"
                type="number"
                step="any"
                :id="`${id}EndInput`"
                :value="value[paramNames[1]]"
                :state="validation"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                :placeholder="placeholder"
                @input="updateParamValue(paramNames[1], $event)"
                @focus.native="$emit('focus', true)"
                @blur.native="$emit('blur', true)" />
              <b-form-input
                v-else-if="type === 'dateRange'"
                type="date"
                :id="`${id}EndInput`"
                :value="value[paramNames[1]]"
                :state="validation"
                :disabled="inputDisabled"
                :aria-describedby="`${id}InvalidFeedback`"
                placeholder="YYYY/MM/DD"
                @input="updateParamValue(paramNames[1], $event)"
                @focus.native="$emit('focus', true)"
                @blur.native="$emit('blur', true)" />
            </b-col>
          </b-form-row>
        </b-col>
      </b-form-row>
      <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </b-form-invalid-feedback>
    </b-col>
    <b-col cols="1" v-if="removable">
      <b-button-close @click="$emit('remove')" class="pt-1">&times;</b-button-close>
    </b-col>
  </b-form-row>
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
  model: {
    prop: 'value',
    event: 'input'
  },
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
  data () {
    return {}
  },
  computed: {
    validation () {
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
      return this.anyValueCheckbox && this.value[this.anyValueParam] === true
    }
  },
  methods: {
    updateParamValue (param, value) {
      this.$emit('input', {...this.value, [param]: value})
    },
    updateAnyValueCheckbox (value) {
      if (!this.anyValueCheckbox) {
        return
      }

      if (value === true) {
        this.$emit('input', {[this.anyValueParam]: true})
      } else {
        this.$emit('input', {})
      }
    }
  }
}
</script>

<style lang="scss">
</style>
