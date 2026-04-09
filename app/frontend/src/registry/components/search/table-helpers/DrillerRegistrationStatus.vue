<template>
  <div>
    <template v-for="(reg, regIndex) in driller.registrations" :key="`reg status ${driller.person_guid} ${regIndex}`">
      <div v-if="reg.activity === activity">
        <div v-for="(app, appIndex) in reg.applications" :key="`app ${driller.person_guid} ${regIndex} ${appIndex}`">
          {{app.display_status}}
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  props: ['driller', 'activity'],
}
</script>

<style>

</style>
