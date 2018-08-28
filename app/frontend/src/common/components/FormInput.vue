<template>
  <b-form-group
    :id="id"
    :label="label"
    :label-for="`${id}Input`">
    <b-form-select v-if="select"
        :id="`${id}Input`"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
        :value="value"
        :options="options"
        :value-field="valueField"
        :text-field="textField"
        @focus.native="$emit('focus', true)"
        @blur.native="$emit('blur', true)"
        :disabled="disabled"
        :required="required"
        @input="updateValue($event)"
    >
      <template slot="first" v-if="placeholder">
        <option value="">{{ placeholder }}</option>
      </template>
    </b-form-select>
    <b-form-input
        v-else
        :id="`${id}Input`"
        :type="type"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
        :value="value"
        :disabled="disabled"
        :required="required"
        @input="updateValue($event)"
        @focus.native="$emit('focus', true)"
        @blur.native="$emit('blur', true)"
        :placeholder="placeholder"/>
    <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
      <div v-for="(error, index) in errors" :key="`${id}Input error ${index}`">
        {{ error }}
      </div>
    </b-form-invalid-feedback>
    <b-form-text :id="`${id}Hint`">
      {{ hint }}
    </b-form-text>
  </b-form-group>
</template>

<script>
/**
 * example usage in another component:
 *
 * <form-input
 *    id="ownerName"
 *    label="Well owner name:"
 *    v-model="ownerNameInput"
 *    hint="Type a name!"
 *    :errors="errors['ownerName']">   // errors for individual fields must be an array e.g. ['Name already taken']
 * </form-input>
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
    value: null, // internal (holds the value for the field)
    required: String,
    disabled: Boolean,
    type: { // the type of input (e.g. text, number, email)
      type: String,
      default: 'text'
    },
    select: Boolean,
    options: Array,
    valueField: String,
    textField: String,
    placeholder: String,
    loaded: String // if changed to true, change contextual state temporarily (e.g. flash green on valid input)
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
    updateValue: function (value) {
      this.$emit('input', value)
    }
  },
  watch: {
    loaded () {
      if (this.loaded && this.loaded.length) {
        this.updated = true
        setTimeout(() => { this.updated = false }, 500)
      }
    }
  }
}
</script>

<style>

</style>
