<template>
  <div>
    <template v-for="(reg, regIndex) in driller.registrations">
      <div v-if="reg.activity === activity && reg.applications && reg.applications.length" :key="`reg cert ${driller.person_guid} ${regIndex}`">
        <div v-for="(app, appIndex) in reg.applications" :key="`app cert ${driller.person_guid} ${app.application_guid} ${appIndex}`">
          <div v-if="app.subactivity">
            <span v-if="app.certificate">{{ app.certificate }} - </span>{{ app.cert_authority }}
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  props: ['driller', 'activity']
}
</script>

<style>

</style>
