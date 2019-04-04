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
  <b-form-row class="mb-1">
    <b-col>
      <legend tabindex="-1" :id="`${id}Label`" class="col-form-label">{{ label }}</legend>
    </b-col>
    <b-col sm="3">
      <b-form-row class="pt-2 d-flex justify-content-end">
        <b-form-checkbox
          :id="`${id}AnyValue`"
          :checked="booleanChecked"
          v-on:input="updateBooleanValue($event)">
          {{ booleanLabel }}
        </b-form-checkbox>
      </b-form-row>
      <b-form-invalid-feedback :id="`${id}AnyValueInvalidFeedback`">
        <div v-for="(error, index) in booleanErrors" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </b-form-invalid-feedback>
    </b-col>
    <b-col sm="7">
      <b-form-row>
        <b-col>
          <b-form-row>
            <label :id="`${id}StartLabel`" :label-for="`${id}StartInput`" class="col-sm-4 col-form-label text-right">From</label>
            <b-col sm="8">
              <b-form-input
                :id="`${id}StartInput`"
                :type="type"
                :state="validation"
                :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
                :value="minValue"
                :disabled="rangeDisabled"
                :required="required"
                :class="inputClass"
                :step="step"
                :min="min"
                :maxlength="maxlength"
                :formatter="formatter"
                :lazy-formatter="lazyFormatter"
                @input="updateStartValue($event)"
                @focus.native="$emit('focus', true)"
                @blur.native="$emit('blur', true)"
                :placeholder="placeholder"/>
            </b-col>
          </b-form-row>
        </b-col>
        <b-col>
          <b-form-row>
            <label :id="`${id}EndLabel`" :label-for="`${id}EndInput`" class="col-sm-4 col-form-label text-right">To</label>
            <b-col sm="8">
              <b-form-input
                :id="`${id}EndInput`"
                :type="type"
                :state="validation"
                :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
                :value="maxValue"
                :disabled="rangeDisabled"
                :required="required"
                :class="inputClass"
                :step="step"
                :min="min"
                :maxlength="maxlength"
                :formatter="formatter"
                :lazy-formatter="lazyFormatter"
                @input="updateEndValue($event)"
                @focus.native="$emit('focus', true)"
                @blur.native="$emit('blur', true)"
                :placeholder="placeholder"/>
            </b-col>
          </b-form-row>
        </b-col>
      </b-form-row>
      <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
        <div v-for="(error, index) in errors" :key="`${id}Input error ${index}`">
          {{ error }}
        </div>
      </b-form-invalid-feedback>
      <b-form-text :id="`${id}Hint`">
        {{ hint }}
      </b-form-text>
    </b-col>
  </b-form-row>
</template>

<script>
/**
 * example usage in another component:
 *
 * <search-form-boolean-or-range
 *    id="artesianFlow"
 *    label="Artesian Flow"
 *    v-model="artesianFlow"
 *    hint="A flow value"
 *    type="number"
 *    :errors="errors['artesianFlow']"/>   // errors for individual fields must be an array e.g. ['Name already taken']
 *
 */
export default {
  props: {
    id: { // an ID for the form group that will be used to generate IDs for the related components
      required: true,
      type: String
    },
    label: String, // a label for the form input e.g.: "First name:"
    hint: String, // a hint for the user on how to enter text e.g. "Please use YYYY/MM/DD format"
    errors: null, // pass any "field errors" returned by the API into the "errors" prop
    booleanLabel: String,
    booleanErrors: null,
    booleanValue: {
      type: [Boolean, String],
      default: false
    },
    minValue: null, // internal (holds the value for the field)
    maxValue: null, // internal (holds the value for the field)
    required: String,
    disabled: Boolean,
    groupClass: String, // optional pass-through class (use for formatting the form-group)
    inputClass: String, // optional pass-through input class (use for formatting the input field)
    step: [String, Number],
    max: Number,
    min: Number,
    maxlength: Number,
    type: { // the type of input (e.g. number, date)
      type: String,
      default: 'number'
    },
    placeholder: String,
    formatter: Function,
    lazyFormatter: Boolean,
    loaded: {
      required: false
    } // if changed to true, change contextual state temporarily (e.g. flash green on valid input)
  },
  data () {
    return {
      localBooleanValue: null,
      updated: false
    }
  },
  computed: {
    booleanChecked () {
      if (this.localBooleanValue === null) {
        return (this.booleanValue === true) || (this.booleanValue === 'true')
      } else {
        return this.localBooleanValue
      }
    },
    rangeDisabled () {
      return this.disabled || this.booleanChecked === 'true' || this.booleanChecked === true
    },
    validation () {
      return (this.errors && this.errors.length) ? false
        : (this.updated) ? true : null
    }
  },
  methods: {
    updateStartValue (value) {
      this.$emit('start-input', value)
    },
    updateEndValue (value) {
      this.$emit('end-input', value)
    },
    updateBooleanValue (value) {
      this.localBooleanValue = value
      // Clear other values if checked.
      if (this.localBooleanValue) {
        this.updateStartValue('')
        this.updateEndValue('')
      }
    }
  },
  watch: {
    loaded () {
      if (this.loaded && String(this.loaded).length) {
        this.updated = true
        setTimeout(() => { this.updated = false }, 500)
      }
    },
    localBooleanValue (value) {
      this.$emit('boolean-input', value)
    }
  }
}
</script>

<style>

</style>
