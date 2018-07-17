<template>
  <b-form-group
    :id="id"
    :label="label"
    :label-for="`${id}Input`">
    <b-form-input
        :id="`${id}Input`"
        :type="type"
        :state="validation"
        :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
        :value="value"
        @input="updateValue($event.target.value)"
        placeholder="e.g.: http://www.example.com"/>
    <b-form-invalid-feedback :id="`${id}InvalidFeedback`">
      <div v-for="(error, index) in errors" :key="`urlInput error ${index}`">
        {{ error }}
      </div>
    </b-form-invalid-feedback>
    <b-form-text :id="`${id}Hint`">
      {{ hint }}
    </b-form-text>
  </b-form-group>
</template>

<script>
export default {
  props: {
    id: { // an ID for the form group that will be used to generate IDs for the related components
      required: true,
      type: String
    },
    label: String, // a label for the form input e.g.: "First name:"
    hint: String, // a hint for the user on how to enter text e.g. "Please use YYYY/MM/DD format"
    errors: Array, // pass any "field errors" returned by the API into the "errors" prop
    value: String, // internal (holds the value for the field)
    type: { // the type of input (e.g. text, number, email)
      type: String,
      default: 'text'
    }
  },
  computed: {
    validation () {
      return (this.errors && this.errors.length) ? false : null
    }
  },
  methods: {
    updateValue: function (value) {
      this.$emit('input', value)
    }
  }

}
</script>

<style>

</style>
