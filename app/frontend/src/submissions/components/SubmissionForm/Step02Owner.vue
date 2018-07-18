<template>
  <fieldset>
    <legend>Well Owner</legend>
    <b-row>
      <b-col cols="12" md="6">
        <form-input id="ownerFullName" label="Well owner name:" v-model="ownerFullNameInput" :errors="errors['owner_full_name']"></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import inputBindingsMixin from './inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    ownerFullName: String,
    errors: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    ownerFullNameInput: 'ownerFullName'
  }
}
</script>

<style>

</style>
