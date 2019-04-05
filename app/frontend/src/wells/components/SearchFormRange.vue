<template>
  <b-form-row>
    <b-col class="mb-1">
      <legend tabindex="-1" :id="`${id}Label`" class="col-form-label">{{ label }}</legend>
    </b-col>
    <b-col sm="8">
      <b-form-row>
        <b-col class="mb-1">
          <b-form-row>
            <label :id="`${id}StartLabel`" :label-for="`${id}StartInput`" class="col-sm-4 col-form-label text-sm-right">From</label>
            <b-col sm="8">
              <b-form-input
                :id="`${id}StartInput`"
                :type="type"
                :state="validation"
                :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
                :value="minValue"
                :disabled="disabled"
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
        <b-col class="mb-1">
          <b-form-row>
            <label :id="`${id}EndLabel`" :label-for="`${id}EndInput`" class="col-sm-4 col-form-label text-sm-right">To</label>
            <b-col sm="8">
              <b-form-input
                :id="`${id}EndInput`"
                :type="type"
                :state="validation"
                :aria-describedby="`${id}InvalidFeedback ${id}Hint`"
                :value="maxValue"
                :disabled="disabled"
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
 * <search-form-range
 *    id="dateOfWork"
 *    label="Date of work"
 *    v-model="ownerNameInput"
 *    hint="A date range"
 *    type="date"
 *    :errors="errors['dateOfWork']"/>   // errors for individual fields must be an array e.g. ['Name already taken']
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
    updateStartValue (value) {
      this.$emit('start-input', value)
    },
    updateEndValue (value) {
      this.$emit('end-input', value)
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
