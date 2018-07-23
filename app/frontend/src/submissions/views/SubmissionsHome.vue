<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">Well Activity Submission</h4>
      <p>Submit activity on a well that does not exist in the system. Try a search to see if the well exists in the system before submitting a report.</p>

      <!-- Activity submission form -->
      <b-form @submit.prevent="confirmSubmit">

        <!-- Form load/save -->
        <b-row>
          <b-col sm="6" md="7" lg="9"></b-col>
          <b-col sm="6" md="5" lg="3">
            <b-row>
              <b-col class="text-right no-gutters">
                <b-btn block variant="outline-primary" @click="saveForm">
                  Save
                  <transition name="bounce">
                    <i v-show="saveFormSuccess" class="fa fa-check fa-fw text-success"></i>
                  </transition>
                </b-btn>
              </b-col>
              <b-col>
                <b-btn block variant="outline-primary" @click="loadConfirmation" ref="confirmLoadBtn">
                  Load
                  <transition name="bounce">
                    <i v-show="loadFormSuccess" class="fa fa-check fa-fw text-success"></i>
                  </transition>
                </b-btn>
              </b-col>
            </b-row>
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
          :fieldsLoaded="fieldsLoaded"
        ></step01-type>

        <!-- Step 2: Owner information -->
        <step02-owner class="my-3"
          :ownerFullName.sync="form.owner_full_name"
          :ownerMailingAddress.sync="form.owner_mailing_address"
          :ownerProvinceState.sync="form.owner_province_state"
          :ownerCity.sync="form.owner_city"
          :ownerPostalCode.sync="form.owner_postal_code"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
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

      <!-- Form reload (load from save) confirmation -->
      <b-modal
          v-model="confirmLoadModal"
          centered
          title="Confirm load submission data"
          @shown="$refs.confirmLoadConfirmBtn.focus()"
          :return-focus="$refs.loadFormBtn">
        Are you sure you want to load the previously saved activity report? Your current report will be overwritten.
        <div slot="modal-footer">
          <b-btn variant="primary" @click="confirmLoadModal=false;loadForm()" ref="confirmLoadConfirmBtn">
            Save
          </b-btn>
          <b-btn variant="light" @click="confirmLoadModal=false">
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
      saveFormSuccess: false,
      loadFormSuccess: false,
      confirmLoadModal: false,
      errors: {},
      fieldsLoaded: {},
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
    },
    saveForm () {
      // saves a copy of form data locally
      this.saveFormReset()
      const data = JSON.stringify(this.form)
      localStorage.setItem('savedFormData', data)
      setTimeout(() => { this.saveFormSuccess = true }, 0)
    },
    loadForm () {
      this.saveFormReset()
      const storedData = localStorage.getItem('savedFormData')
      if (storedData) {
        const parsedData = JSON.parse(storedData)
        this.form = Object.assign(this.form, parsedData)
        this.fieldsLoaded = Object.assign(this.fieldsLoaded, parsedData)
        setTimeout(() => { this.loadFormSuccess = true }, 0)
        setTimeout(() => { this.fieldsLoaded = {} }, 0)
      } else {
        console.log('no data stored')
      }
    },
    loadConfirmation () {
      this.confirmLoadModal = true
    },
    saveFormReset () {
      this.saveFormSuccess = false
      this.loadFormSuccess = false
    }
  },
  watch: {
    form: {
      handler () {
        this.saveFormReset()
      },
      deep: true
    }
  },
  created () {
    this.resetForm()
  }
}
</script>

<style lang="scss">
.bounce-enter-active {
  animation: bounce-in .5s;
}
.bounce-leave-active {
  animation: bounce-out .2s;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes bounce-out {
  100% {
    transform: scale(0)
  }
}
</style>
