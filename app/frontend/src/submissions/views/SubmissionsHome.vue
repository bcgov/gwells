<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">Well Activity Submission</h4>
      <p>Submit activity on a well that does not exist in the system. Try a search to see if the well exists in the system before submitting a report.</p>
      <b-form @submit.prevent="handleFormSubmit">
        <step01-type class="my-3"
          :wellActivityType.sync="form.well_activity_type"
          :units.sync="units"
          :personResponsible.sync="form.driller_responsible"
          :workStartDate.sync="form.work_start_date"
          :workEndDate.sync="form.work_end_date"
          :errors="errors"
        ></step01-type>
        <step02-owner class="my-3"
          :ownerFullName.sync="form.owner_full_name"
          :errors="errors"
        ></step02-owner>
        <b-btn type="submit" variant="primary">Submit</b-btn>
      </b-form>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import Step01Type from '@/submissions/components/SubmissionForm/Step01Type.vue'
import Step02Owner from '@/submissions/components/SubmissionForm/Step02Owner.vue'
export default {
  name: 'SubmissionsHome',
  components: {
    Step01Type,
    Step02Owner
  },
  data () {
    return {
      units: 'imperial',
      errors: {},
      form: {
        // forms are grouped into 'steps' to facilitate completing submissions
        // one step at a time.

        well_activity_type: 'CON',
        driller_responsible: null,
        work_start_date: '',
        work_end_date: '',
        owner_full_name: ''

      }
    }
  },
  methods: {
    handleFormSubmit () {
      const data = Object.assign({}, this.form)

      // replace the "person responsible" object with the person's guid
      if (data.driller_responsible && data.driller_responsible.person_guid) {
        data.driller_responsible = data.driller_responsible.person_guid
      }
      ApiService.post('submissions', data).then(() => {
        console.log('success')
      }).catch((error) => {
        this.errors = error.response.data
      })
    }
  }
}
</script>

<style>

</style>
