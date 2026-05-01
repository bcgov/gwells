<template>
  <Message v-if="error !== null" closable @close="clearError()" severity="warn" id="errorAlert">
    <div v-if="error && error.data && error.data.non_field_errors && error.data.non_field_errors.length">
      {{ error.data.non_field_errors[0] }}
    </div>
    <div v-else>
      {{ error.status }} {{ error.statusText }}<span v-if="error.data && error.data.detail">: {{ error.data.detail }}</span>
    </div>
  </Message>
</template>

<script>

export default {
  props: ['error', 'resetter', 'onClear'],
  methods: {
    clearError () {
      if (this.onClear) {
        this.onClear()
      } else if (this.resetter) {
        this.$store.commit(this.resetter, null)
      }
    }
  }
}
</script>

<style>

</style>
