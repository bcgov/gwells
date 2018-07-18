<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">Well Activity Submission</h4>
      <p>Submit activity on a well that does not exist in the system. Try a search to see if the well exists in the system before submitting a report.</p>
      <b-form>
        <step01-type class="my-3"
          :typeOfWork.sync="form.type_of_work"
          :units.sync="units"
          :personResponsible.sync="form.person_responsible"
          :workStartDate.sync="form.work_start_date"
          :workEndDate.sync="form.work_end_date"
          :errors="errors"
        ></step01-type>
        <step02-owner class="my-3"
          :ownerFullName.sync="form.owner_full_name"
          :errors="errors"
        ></step02-owner>
      </b-form>
    </div>
  </div>
</template>

<script>
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
      units: '',
      errors: {},
      form: {
        // forms are grouped into 'steps' to facilitate completing submissions
        // one step at a time.

        type_of_work: '',
        person_responsible: {},
        work_start_date: '',
        work_end_date: '',
        owner_full_name: ''

      }
    }
  }
}
</script>

<style>

</style>
