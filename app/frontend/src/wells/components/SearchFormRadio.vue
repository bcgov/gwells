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
  <b-form-row class="pt-1 mb-1">
    <b-col sm="6" v-if="label">
      <legend :id="`${id}Label`" class="col-form-label pt-0">{{ label }}</legend>
    </b-col>
    <b-col>
      <b-form-radio-group
        :id="`${id}Input`"
        :checked="value"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
        :required="required"
        :class="inputClass"
        :options="options"
        @input="updateValue($event)"
        @focus.native="$emit('focus', true)"
        @blur.native="$emit('blur', true)"/>
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
 * <search-form-radio
 *    id="matchAny"
 *    label="Match any or all filters"
 *    v-model="matchAny"
 *    :errors="errors['matchAny']"/>   // errors for individual fields must be an array e.g. ['Name already taken']
 *
 */
export default {
  props: {
    id: { // an ID for the form group that will be used to generate IDs for the related components
      required: true,
      type: String
    },
    options: Array,
    label: String, // a label for the form input e.g.: "First name:"
    hint: String, // a hint for the user on how to enter text e.g. "Please use YYYY/MM/DD format"
    errors: null, // pass any "field errors" returned by the API into the "errors" prop
    value: null, // internal (holds the value for the field)
    required: String,
    disabled: Boolean,
    groupClass: String, // optional pass-through class (use for formatting the form-group)
    inputClass: String, // optional pass-through input class (use for formatting the input field)
    valueField: String,
    textField: String,
    placeholder: String,
    formatter: Function,
    lazyFormatter: Boolean,
    multiple: {
      type: Boolean,
      default: false
    },
    loaded: {
      required: false
    } // if changed to true, change contextual state temporarily (e.g. flash green on valid input)
  },
  data () {
    return {
      updated: false
    }
  },
  computed: {
    validation () {
      return (this.errors && this.errors.length) ? false
        : (this.updated) ? true : null
    }
  },
  methods: {
    updateValue (value) {
      this.$emit('input', value)
    }
  },
  watch: {
    loaded () {
      if (this.loaded && String(this.loaded).length) {
        this.updated = true
        setTimeout(() => { this.updated = false }, 500)
      }
    }
  }
}
</script>

<style>

</style>
