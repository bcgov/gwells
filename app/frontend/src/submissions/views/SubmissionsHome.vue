<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">
        <b-row>
          <b-col lg="8">Well Activity Submission</b-col>
          <b-col lg="4" class="text-right">
            <b-btn size="sm" :variant="`${formIsFlat ? 'primary':'outline-primary'}`" @click="formIsFlat=true">Flat form</b-btn>
            <b-btn size="sm" :variant="`${formIsFlat ? 'outline-primary':'primary'}`" @click="formIsFlat=false">Wizard</b-btn>
          </b-col>
        </b-row>
      </h4>
      <p>Submit activity on a well that does not exist in the system. Try a search to see if the well exists in the system before submitting a report.</p>

      <!-- Activity submission form -->
      <b-form @submit.prevent="confirmSubmit">

        <!-- Form load/save -->
        <b-row>
          <b-col class="text-right">
            <b-btn size="sm" variant="outline-primary" @click="saveForm">
              Save
              <transition name="bounce" mode="out-in">
                  <i v-show="saveFormSuccess" class="fa fa-check text-success"></i>
              </transition>
            </b-btn>
            <b-btn size="sm" variant="outline-primary" @click="loadConfirmation" ref="confirmLoadBtn">
              Load
              <transition name="bounce">
                  <i v-show="loadFormSuccess" class="fa fa-check text-success"></i>
              </transition>
            </b-btn>
          </b-col>
        </b-row>

        <!-- Form step 1: Type of well -->
        <step01-type class="my-3"
          v-if="formStep === 1 || formIsFlat"
          :wellTagNumber.sync="form.well"
          :wellActivityType.sync="form.well_activity_type"
          :wellClass.sync="form.well_class"
          :wellSubclass.sync="form.well_subclass"
          :intendedWaterUse.sync="form.intended_water_use"
          :units.sync="units"
          :personResponsible.sync="form.driller_responsible"
          :idPlateNumber.sync="form.identification_plate_number"
          :wellPlateAttached.sync="form.well_plate_attached"
          :drillerName.sync="form.driller_name"
          :consultantName.sync="form.consultant_name"
          :consultantCompany.sync="form.consultant_company"
          :workStartDate.sync="form.work_start_date"
          :workEndDate.sync="form.work_end_date"
          :drillerSameAsPersonResponsible.sync="form.nonForm.drillerSameAsPersonResponsible"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        ></step01-type>

        <!-- Step 2: Owner information -->
        <step02-owner class="my-3"
          v-if="formStep === 2 || formIsFlat"
          :ownerFullName.sync="form.owner_full_name"
          :ownerMailingAddress.sync="form.owner_mailing_address"
          :ownerProvinceState.sync="form.owner_province_state"
          :ownerCity.sync="form.owner_city"
          :ownerPostalCode.sync="form.owner_postal_code"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        ></step02-owner>
        <b-row>
          <b-col v-if="!formIsFlat">
            <b-btn v-if="step > 1" @click="step > 1 ? step-- : null">Back</b-btn>
          </b-col>
          <b-col :class="`pr-4 ${formIsFlat ? '':'text-right'}`">
            <b-btn v-if="step < maxSteps && !formIsFlat" @click="step++">Next</b-btn>
            <b-btn v-else id="formSubmitButton" type="submit" variant="primary" ref="activitySubmitBtn">Submit</b-btn>
          </b-col>
        </b-row>
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
          id="confirmSubmitModal"
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
            Load
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
import { FETCH_CODES } from '../store/actions.types.js'
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
      formIsFlat: true,
      units: 'imperial',
      confirmSubmitModal: false,
      formSubmitLoading: false,
      formSubmitSuccess: false,
      saveFormSuccess: false,
      loadFormSuccess: false,
      confirmLoadModal: false,
      step: 1,
      maxSteps: 2,
      sliding: null,
      errors: {},
      fieldsLoaded: {},
      form: {},
      formOptions: {}
    }
  },
  computed: {
    formStep () {
      return (this.step % (this.maxSteps + 1))
    }
  },
  methods: {
    formSubmit () {
      const data = Object.assign({}, this.form)

      // delete nonForm data stored within form object
      delete data.nonForm

      // replace the "person responsible" object with the person's guid
      if (data.driller_responsible && data.driller_responsible.person_guid) {
        data.driller_responsible = data.driller_responsible.person_guid
      }

      if (data.well && data.well.well_tag_number) {
        data.well = data.well.well_tag_number
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
        well_activity_type: 'CON',
        well: null,
        well_class: '',
        well_subclass: '',
        intended_water_use: '',
        identification_plate_number: null,
        well_plate_attached: '',
        driller_responsible: null,
        driller_name: '',
        consultant_name: '',
        consultant_company: '',
        work_start_date: '',
        work_end_date: '',
        owner_full_name: '',
        owner_mailing_address: '',
        owner_city: '',
        owner_province_state: '',
        owner_postal_code: '',

        // non-form fields that should be saved with form
        nonForm: {
          drillerSameAsPersonResponsible: false
        }
      }
    },
    saveForm () {
      // saves a copy of form data locally
      this.saveStatusReset()
      const data = JSON.stringify(this.form)
      localStorage.setItem('savedFormData', data)
      setTimeout(() => { this.saveFormSuccess = true }, 10)
      setTimeout(() => { this.saveFormSuccess = false }, 1000)
    },
    loadForm () {
      this.saveStatusReset()
      const storedData = localStorage.getItem('savedFormData')
      if (storedData) {
        this.resetForm()

        // some form features depend on watching form field values.
        // setTimeout pushes rendering new data down execution queue
        // to give watchers a chance to act on each set of changes
        // (e.g. form reset, form population)
        setTimeout(() => {
          const parsedData = JSON.parse(storedData)
          this.form = Object.assign(this.form, parsedData)
          this.fieldsLoaded = Object.assign(this.fieldsLoaded, parsedData)
          setTimeout(() => { this.loadFormSuccess = true }, 0)
          setTimeout(() => { this.fieldsLoaded = {} }, 0)
          setTimeout(() => { this.loadFormSuccess = false }, 1000)
        }, 0)
      }
    },
    loadConfirmation () {
      this.confirmLoadModal = true
    },
    saveStatusReset () {
      this.saveFormSuccess = false
      this.loadFormSuccess = false
    }
  },
  watch: {
    form: {
      handler () {
        this.saveStatusReset()
      },
      deep: true
    }
  },
  created () {
    this.resetForm()
    this.$store.dispatch(FETCH_CODES)
  }
}
</script>

<style lang="scss">
.slide-leave-active,
.slide-enter-active {
  transition: 1s;
}
.slide-enter {
  transform: translate(100%, 0);
}
.slide-leave-to {
  transform: translate(-100%, 0);
}
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
