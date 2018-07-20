<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">Well Activity Submission</h4>
      <p>Submit activity on a well that does not exist in the system. Try a search to see if the well exists in the system before submitting a report.</p>

      <!-- Activity submission form -->
      <b-form @submit.prevent="confirmSubmit">

        <!-- Form load/save -->
        <b-row>
          <b-col class="text-right">
            <b-btn variant="outline-primary">Save</b-btn>
            <b-btn variant="outline-primary">Load last saved</b-btn>
          </b-col>
        </b-row>

        <!-- Form step 1: Type of well -->
        <step01-type class="my-3"
          :wellActivityType.sync="form.well_activity_type"
          :units.sync="units"
          :personResponsible.sync="form.driller_responsible"
          :workStartDate.sync="form.work_start_date"
          :workEndDate.sync="form.work_end_date"
          :errors="errors"
        ></step01-type>

        <!-- Step 2: Owner information -->
        <step02-owner class="my-3"
          :ownerFullName.sync="form.owner_full_name"
          :ownerMailingAddress.sync="form.owner_mailing_address"
          :ownerProvinceState.sync="form.owner_province_state"
          :ownerCity.sync="form.owner_city"
          :ownerPostalCode.sync="form.owner_postal_code"
          :errors="errors"
        ></step02-owner>

        <b-btn type="submit" variant="primary" ref="activitySubmitBtn">Submit</b-btn>
      </b-form>

      <!-- Form submission success message -->
      <b-alert
          :show="formSubmitSuccess"
          dismissible
          @dismissed="formSubmitSuccess=false"
          variant="success"
          class="mt-3">Report submitted!</b-alert>

      <!-- Form submission confirmation -->
      <b-modal
          v-model="confirmSubmitModal"
          centered
          title="Confirm submission"
          @shown="$refs.confirmSubmitConfirmBtn.focus()"
          :return-focus="$refs.activitySubmitBtn">
        Are you sure you want to submit this activity report?
        <div slot="modal-footer">
          <b-btn variant="primary" @click="confirmSubmitModal=false;formSubmit()" ref="confirmSubmitConfirmBtn">
            Save
          </b-btn>
          <b-btn variant="light" @click="confirmSubmitModal=false">
            Cancel
          </b-btn>
        </div>
      </b-modal>
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
      confirmSubmitModal: false,
      formSubmitLoading: false,
      formSubmitSuccess: false,
      errors: {},
      form: {}
    }
  },
  methods: {
    formSubmit () {
      const data = Object.assign({}, this.form)

      // replace the "person responsible" object with the person's guid
      if (data.driller_responsible && data.driller_responsible.person_guid) {
        data.driller_responsible = data.driller_responsible.person_guid
      }
      this.formSubmitLoading = true
      this.errors = {}
      ApiService.post('submissions', data).then(() => {
        this.formSubmitSuccess = true
        this.resetForm()
      }).catch((error) => {
        this.errors = error.response.data
      }).finally(() => {
        this.formSubmitLoading = false
      })
    },
    confirmSubmit () {
      this.confirmSubmitModal = true
    },
    resetForm () {
      this.form = {
        // forms are grouped into 'steps' to facilitate completing submissions
        // one step at a time.

        well_activity_type: 'CON',
        driller_responsible: null,
        work_start_date: '',
        work_end_date: '',
        owner_full_name: '',
        owner_mailing_address: '',
        owner_city: '',
        owner_province_state: '',
        owner_postal_code: ''
      }
    }
  },
  created () {
    this.resetForm()
  }
}
</script>

<style>

</style>
