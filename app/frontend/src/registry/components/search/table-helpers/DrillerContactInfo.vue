<template>
  <div>
    <div v-if="driller.contact_tel">{{driller.contact_tel}}</div>
    <div v-if="driller.contact_cell">{{driller.contact_cell}}</div>

    <!-- contact_info dataset: exists in database but new applicants use driller.contact_tel  -->
    <div v-for="(contact, contactIndex) in contactSort(driller)" :key="`contact ${driller.person_guid} ${contactIndex}`">
      <span v-if="contact.type === 'tel'">{{ contact.value }}</span>
      <span v-if="contact.type === 'email'"><a :href="`mailto:${contact.value}`">{{contact.value}}</a></span>
    </div>

    <div v-if="driller.contact_email"><a :href="`mailto:${driller.contact_email}`">{{driller.contact_email}}</a></div>
  </div>
</template>

<script>
export default {
  props: ['driller'],
  methods: {
    contactSort (driller) {
      // sort a person's contact info into groups (tel numbers followed by emails)
      const tel = []
      const email = []
      driller.contact_info.forEach((item) => {
        if (item.contact_tel) {
          tel.push({
            type: 'tel',
            value: item.contact_tel
          })
        }
        if (item.contact_email) {
          email.push({
            type: 'email',
            value: item.contact_email
          })
        }
      })
      return tel.concat(email)
    }
  }
}
</script>

<style>

</style>
