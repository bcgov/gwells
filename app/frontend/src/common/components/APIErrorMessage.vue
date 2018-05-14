<template>
  <b-alert :show="error !== null" dismissible @dismissed="clearError()" variant="warning" role="alert" id="errorAlert">
    <div v-if="error && error.data && error.data.non_field_errors && error.data.non_field_errors.length">
      {{ error.data.non_field_errors[0] }}
    </div>
    <div v-else>
      {{ error.status }} {{ error.statusText }}<span v-if="error.data && error.data.detail">: {{ error.data.detail }}</span>
    </div>
  </b-alert>
</template>

<script>

export default {
  props: ['error', 'resetter'],
  methods: {
    clearError () {
      this.$store.commit(this.resetter, null)
    }
  }
}
</script>

<style>

</style>
