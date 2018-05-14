<template>
  <div>
    <div v-for="(reg, regIndex) in driller.registrations"
        v-if="reg.activity === 'DRILL'"
        :key="`reg quals ${driller.person_guid} ${regIndex}`">
      <div v-if="reg.applications && reg.applications.length"
          v-for="(app, appIndex) in reg.applications"
          :key="`app quals ${driller.person_guid} ${app.application_guid} ${appIndex}`">
        <div v-if="app.subactivity">
          {{ app.subactivity.description }}
        </div>
        <!-- <div v-if="app.subactivity &&
                    app.subactivity.qualification_set &&
                    app.subactivity.qualification_set.length"
            v-for="(qual, qualIndex) in app.subactivity.qualification_set"
            :key="`qual set ${driller.person_guid} ${app.application_guid} ${qualIndex}`">
            {{ qual.description }}
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['driller']
}
</script>

<style>

</style>
