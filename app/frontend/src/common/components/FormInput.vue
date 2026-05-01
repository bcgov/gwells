<template>
  <div :class="groupClass" :id="id">
    <label v-if="label" :for="`${id}Input`" class="block mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    <slot />
    <MultiSelect
      v-if="select"
      :id="`${id}Input`"
      :model-value="modelValue"
      :invalid="validation"
      :options="options"
      :optionLabel="textField"
      :optionValue="valueField"
      :placeholder="placeholder"
      :class="inputClass"
      :disabled="disabled"
      @update:modelValue="updateValue"
      @focus="$emit('focus', true)"
      @blur="$emit('blur', true)"
    />
    <InputText
      v-else
      :id="`${id}Input`"
      :type="type"
      :invalid="validation"
      :model-value="modelValue"
      :disabled="disabled"
      :placeholder="placeholder"
      :maxlength="maxlength"
      :class="inputClass"
      @update:modelValue="updateValue"
      @focus="$emit('focus', true)"
      @blur="$emit('blur', true)"
    />
    <Message
      v-for="(error, index) in errors"
      :key="`${id}-error-${index}`"
      severity="error"
      class="mt-1"
      >
      {{ error }}
    </Message>
    <small v-if="hint" class="text-muted block mt-1" :id="`${id}Hint`">
      {{ hint }}
    </small>
  </div>
</template>


<script>
  // Example
  //  <FormInput
  //   id="ownerName"
  //   label="Well owner name:"
  //   v-model="ownerNameInput"
  //   hint="Type a name!"
  //   :errors="errors.ownerName"
  //  />

export default {
  props: {
    id: { // an ID for the form group that will be used to generate IDs for the related components
      required: true,
      type: String
    },
    label: String, // a label for the form input e.g.: "First name:"
    hint: String, // a hint for the user on how to enter text e.g. "Please use YYYY/MM/DD format"
    errors: null, // pass any "field errors" returned by the API into the "errors" prop
    modelValue: null,
    required: String,
    disabled: Boolean,
    groupClass: String, // optional pass-through class (use for formatting the form-group)
    inputClass: String, // optional pass-through input class (use for formatting the input field)
    type: { // the type of input (e.g. text, number, email)
      type: String,
      default: 'text'
    },
    select: Boolean,
    options: Array,
    valueField: String,
    textField: String,
    placeholder: String,
    maxlength: Number,
    loaded: {
      required: false
    } // if changed to true, change contextual state temporarily (e.g. flash green on valid input)
  },

  emits: ['update:modelValue', 'focus', 'blur'],

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
      if (this.type.toLowerCase() === 'number' && value === '') {
        this.$emit('update:modelValue', null)
        return
      } else {
        this.$emit('update:modelValue', value)
      }
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
