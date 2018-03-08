<template>
  <div @click="clearError" class="alert alert-warning" role="alert" id="errorAlert">
    {{ error.status }} {{ error.statusText }}: {{ error.data.detail }}
  </div>
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
