<template>
  <div>
    <div v-if="driller.contact_tel">{{driller.contact_tel}}</div>
    <div v-if="driller.contact_cell">{{driller.contact_cell}}</div>
    <div v-if="driller.contact_email"><a :href="`mailto:${driller.contact_email}`">{{driller.contact_email}}</a></div>
  </div>
</template>

<script>
export default {
  props: ['driller']
}
</script>

<style>

</style>
