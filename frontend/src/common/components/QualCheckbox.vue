<template>
  <span>
    <i class="fa fa-check-square registry-checkbox" v-if="checked"></i>
    <i class="fa fa-square-o registry-checkbox" v-else></i>
  </span>
</template>

<script>
export default {
  props: ['checked']
}
</script>

<style>
.registry-checkbox {
  font-size: 1.5rem;
}
</style>
