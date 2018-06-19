<template>
  <div>
    <div v-for="(reg, regIndex) in driller.registrations"
        v-if="reg.activity === activity"
        :key="`reg status ${driller.person_guid} ${regIndex}`">
      <div v-for="(app, appIndex) in reg.applications" :key="`app ${driller.person_guid} ${regIndex} ${appIndex}`">
        <div v-if="!!app.removal_date">Removed</div>
        <div v-else-if="!!app.current_status">{{app.current_status.description}}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: ['driller', 'activity'],
  computed: {
    ...mapGetters(['user'])
  }
}
</script>

<style>

</style>
