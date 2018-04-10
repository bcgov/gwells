<template>
  <div>
    <div v-for="(reg, regIndex) in driller.registrations"
        v-if="reg.activity === activity"
        :key="`reg cert ${driller.person_guid} ${regIndex}`">
      <div v-if="reg.applications && reg.applications.length"
          v-for="(app, appIndex) in reg.applications"
          :key="`app cert ${driller.person_guid} ${app.application_guid} ${appIndex}`">
        <div v-if="applicationApproved(app) && app.subactivity">
          {{ app.cert_authority }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['driller', 'activity'],
  methods: {
    applicationApproved (app) {
      return app.status_set && app.status_set.length && !!~app.status_set.findIndex((item) => {
        return item.status === 'A'
      })
    }
  }
}
</script>

<style>

</style>
