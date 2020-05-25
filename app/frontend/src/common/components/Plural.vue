<template>
  <span :data-count="count">
    <slot name="zero" v-if="count === 0 && hasZeroSlot">
      {{zero}}
    </slot>
    <slot name="singular" :count="count" v-else-if="count === 1">
      {{singular}}
    </slot>
    <slot name="plural" :count="count" v-else>
      {{plural}}
    </slot>
  </span>
</template>

<script>
export default {
  props: [
    'count',
    'zero',
    'singular',
    'plural'
  ],
  computed: {
    hasZeroSlot () {
      return !!this.$slots.zero
    }
  }
}
</script>

<style>
</style>
