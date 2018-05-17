<template>
  <div>
    {{ company.name }}
  </div>
</template>

<script>
export default {
  props: ['driller', 'activity'],
  data () {
    return {
    }
  },
  computed: {
    company () {
      const company = {}
      if (this.driller && this.driller.registrations && this.driller.registrations.length && this.activity) {
        const registration = this.driller.registrations.find((reg) => {
          return reg.activity === this.activity
        })
        if (registration && registration.organization) {
          company['name'] = registration.organization.name
        }
      }
      return company
    }
  }
}
</script>

<style>

</style>
