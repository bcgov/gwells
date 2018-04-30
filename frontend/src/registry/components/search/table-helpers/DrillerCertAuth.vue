<template>
  <div>
    <div v-for="(reg, regIndex) in driller.registrations"
        v-if="reg.activity === activity"
        :key="`reg cert ${driller.person_guid} ${regIndex}`">
      <div v-if="reg.applications && reg.applications.length"
          v-for="(app, appIndex) in reg.applications"
          :key="`app cert ${driller.person_guid} ${app.application_guid} ${appIndex}`">
        <div v-if="app.subactivity">
          {{ app.cert_authority }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['driller', 'activity']
}
</script>

<style>

</style>
