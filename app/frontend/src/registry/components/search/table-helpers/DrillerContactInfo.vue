<template>
  <div class="text-nowrap">
    <div v-if="company.tel">Phone: {{company.tel}}</div>
    <div v-if="company.fax">Fax: {{company.fax}}</div>
    <div v-if="company.email">Email: <a :href="`mailto:${company.email}`">{{company.email}}</a></div>
    <div v-if="company.website">Web: <a :href="company.website">{{company.website}}</a></div>
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
          company['tel'] = registration.organization.main_tel
          company['fax'] = registration.organization.fax_tel
          company['email'] = registration.organization.email
          company['website'] = registration.organization.website_url
        }
      }
      return company
    }
  }
}
</script>

<style>

</style>
