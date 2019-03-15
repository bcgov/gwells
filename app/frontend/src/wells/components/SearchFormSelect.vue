<template>
  <b-form-row class="mb-1">
    <b-col sm="6">
      <label :id="`${id}Label`" :label-for="`${id}Input`">{{ label }}</label>
    </b-col>
    <b-col>
      <b-form-select
          :id="`${id}Input`"
          :state="validation"
          :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
          :value="value"
          :options="options"
          :value-field="valueField"
          :text-field="textField"
          :class="inputClass"
          @focus.native="$emit('focus', true)"
          @blur.native="$emit('blur', true)"
          :disabled="disabled"
          :required="required"
          :multiple="multiple"
          @input="updateValue($event)"
      >
        <template slot="first" v-if="placeholder">
          <option value="">{{ placeholder }}</option>
        </template>
      </b-form-select>
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
 * <search-form-select
 *    id="wellClass"
 *    label="Well class:"
 *    v-model="wellClass"
 *    hint="A type of well"
 *    :errors="errors['wellClass']"/>   // errors for individual fields must be an array e.g. ['Name already taken']
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
    labelCols: [Number, String],
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
