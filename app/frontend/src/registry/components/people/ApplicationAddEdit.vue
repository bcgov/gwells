/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
  <div>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Classification &amp; Qualifications
          <Button class="close pull-right" aria-label="Close" @click="$emit('close')" severity="secondary">
            <span aria-hidden="true">&times;</span>
          </Button>
        </h5>
        <div v-if="loading">
          <div class="grid">
            <div class="row-span-full">
              <div class="fa-2x text-center">
                <i class="fa fa-circle-o-notch fa-spin"></i>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <div class="grid">
            <div class="row-span-full">
              <div style="font-weight: bold;">Certification</div>
            </div>
          </div>
          <responsive-grid :cols="[2, 4, 2, 4]" gap="6" class="form-group">
            <label for="issued-by">Issued by</label>
            <Select
            inputId="issued-by"
            :options="formOptions.issuer"
            optionLabel="text"
            optionValue="value"
            v-model="qualificationForm.primary_certificate.acc_cert_guid"
            required
            placeholder="Please select an option"/>
            <label for="cert-num">Certificate number</label>
            <InputText
            inputId="cert-num"
            type="text"
            placeholder="Enter certificate number"
            v-model="qualificationForm.primary_certificate_no"
            required/>
          </responsive-grid>
          <responsive-grid :cols="[2, 10]" gap="2" class="form-group font-bold mb-2">
            <div>Select classification</div>
            <div class="flex flex-wrap lg:gap-4 gap-2 sm:flex-row">
              <div v-for="option in formOptions.classifications" :key="option.value" class="flex items-center gap-2">
                <RadioButton
                  v-model="qualificationForm.subactivity.registries_subactivity_code"
                  :value="option.value"
                  :inputId="option.value"
                  @change="changedClassification"
                  required/>
                <label :for="option.value" class="font-normal">{{ option.text }}</label>
              </div>
            </div>
          </responsive-grid>
          <responsive-grid :cols="[12, 8]" :sm="12" gap="2" class="form-group mb-2">
            <label class="font-bold">Qualified{{activity === 'DRILL' ? ' to drill' : '' }}</label>
            <div class=" grid lg:grid-cols-3">
              <div v-for="opt of formOptions.qualifications" :key="opt.value" class="flex items-center gap-2">
                <Checkbox
                  v-model="qualificationForm.qualifications"
                  :value="opt.value"
                  :inputId="opt.value"
                  :disabled="true"
                />
                <label :for="opt.value">{{ opt.text }}</label>
              </div>
            </div>
          </responsive-grid>
          <responsive-grid :cols="[12, 4, 4]" gap="2" class="form-group block mb-2">
            <h5>Adjudication</h5>
            <label class="col-span-1">Confirmed applicant is 19 years of age or older by reviewing</label>
            <Select
              v-model="qualificationForm.proof_of_age.code"
              :options="formOptions.proofOfAge"
              optionValue="value"
              optionLabel="text"
              class="col-span-2"
              placeholder="Please select an option"
              required/>
          </responsive-grid>
          <responsive-grid :cols="2" gap="2" class="form-group mb-2">
            <label description="format: yyy-mm-dd" label="" invalid-feedback="Invalid date format">Date application received</label>
            <InputText type="date" v-model="qualificationForm.application_recieved_date" :state="pendingDateState"/>
          </responsive-grid>
          <div class="grid" v-if="isEditMode">
            <div class="grid grid-cols-2 gap-6" v-if="qualificationForm.application_recieved_date">
              <label class="col-span-1" description="format: yyyy-mm-dd" invalid-feedback="Invalid date format">Approval date outcome</label>
                <InputText class="col-span-1" type="date" v-model="qualificationForm.application_outcome_date" :state="approvalDateState"/>
            </div>
            <div class="grid grid-cols-2 gap-6" v-if="showApprovalOutcome">
              <label class="col-span-1">Approval outcome</label>
                <Select :options="formOptions.approvalOutcome" optionValue="value" optionLabel="text" v-model="qualificationForm.current_status.code"/>
            </div>
            <div class="grid grid-cols-2 gap-6" v-if="showReasonDenied">
              <label class="col-span-1">Reason denied</label>
                <InputText class="col-span-1" type="text" v-model="qualificationForm.reason_denied"/>
            </div>
          </div>
          <div class="grid" v-if="isEditMode">
            <div class="grid grid-cols-2 gap-6" v-if="showNotificationDate">
              <label class="col-span-1" description="format: yyyy-mm-dd">Notification date</label>
                <InputText type="date" class="col-span-1" v-model="qualificationForm.application_outcome_notification_date" :state="notificationDateState"/>
            </div>
          </div>
          <div class="grid" v-if="showRemoval && isEditMode">
            <div class="grid grid-cols-2 gap-6">
              <h5>Removal of classification from Register</h5>
            </div>
          </div>
          <div class="grid" v-if="showRemoval && isEditMode">
            <div class="grid grid-cols-2 gap-6">
              <label class="col-span-1">Removal date</label>
                <InputText type="date" class="col-span-1" v-model="qualificationForm.removal_date" :state="removalDateState"/>
            </div>
            <div class="grid grid-cols-2 gap-6" v-if="showRemovalReason">
              <label class="col-span-1">Removal reason</label>
                <Select :options="formOptions.removalReasons" optionValue="value" optionLabel="text" v-model="qualificationForm.removal_reason.code" placeholder="Please select an option"/>
            </div>
          </div>
          <!-- slot for child elements to be added by parent component -->
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { useRegistryStore } from '@/stores/registry.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

export default {
  components: {
    ResponsiveGrid
  },
  props: {
    value: Object,
    activity: {
      required: true,
      type: String,
      validator: (val) => {
        return ['DRILL', 'PUMP'].includes(val)
      }
    },
    mode: {
      required: true,
      type: String,
      validator: (val) => {
        return ['edit', 'add'].includes(val)
      }
    }
  },
  data () {
    return {
      registryStore: useRegistryStore(),
      qualificationForm: this.copyFormData(this.value)
    }
  },
  watch: {
    // Watching the entire object is expensive, but we need some way of notifying the parent.
    qualificationForm: {
      handler: function (val, oldVal) {
        this.$emit('input', val)
      },
      deep: true
    }
  },
  methods: {
    copyFormData (input) {
      // We need a default data structure when we're creating an application. If we're editing an
      // application, we can piggy back off the value being passed in.
      const defaultData = {
        subactivity: {
          registries_subactivity_code: null
        },
        primary_certificate_no: '',
        primary_certificate: {
          acc_cert_guid: null
        },
        proof_of_age: {
          code: null
        },
        qualifications: [],
        reason_denied: '',
        current_status: {
          code: 'P' // We default to Pending approval
        },
        removal_reason: {
          code: null
        }
      }
      // It is important that we preserve the reference to the input variable, as the parent
      // component may be bound to it.
      const defaultCopy = JSON.parse(JSON.stringify(defaultData))
      // Object.assign doesn't work correctly with the vue Observer object correctly.
      let result = null
      if (input) {
        Object.keys(defaultCopy).forEach((key) => {
          if (!(key in input)) {
            input[key] = defaultCopy[key]
          }
        })
        result = input
      } else {
        result = defaultCopy
      }
      if (result.current_status == null) {
        // In very exceptional cases, a current status can be null - this is problematic in terms of
        // data binding, so we attach a default value here.
        result.current_status = defaultCopy.current_status
      }
      if (result.removal_reason == null) {
        result.removal_reason = defaultCopy.removal_reason
      }
      return result
    },
    isDateValid (input) {
      // We accept null, undefined, '' as valid dates, in addition to correctly formatted dates
      return input ? moment(input, 'YYYY-MM-DD', true).isValid() : true
    },
    isAllDatesValid () {
      return (!this.approvalStatus || this.isDateValid(this.qualificationForm.application_outcome_date)) &&
        (!this.pendingStatus || this.isDateValid(this.qualificationForm.application_outcome_notification_date)) &&
        (!this.approvalStatus || this.isDateValid(this.qualificationForm.application_recieved_date)) &&
        this.isDateValid(this.qualificationForm.removal_date)
    },
  },
  computed: {
    loading () { return this.registryStore.loading },
    drillerOptions () { return this.registryStore.drillerOptions },
    formOptions () {
      let result = {
        issuer: [],
        classifications: [],
        qualifications: [],
        proofOfAge: [],
        approvalOutcome: [],
        removalReasons: []
      }
      if (this.drillerOptions) {
        // If driller options have loaded, prepare the form options.
        result.proofOfAge = result.proofOfAge.concat(this.drillerOptions.proof_of_age_codes.map((item) => { return { 'text': item.description, 'value': item.code } }))
        if (this.activity in this.drillerOptions) {
          // Different activities have different options.
          result.classifications = this.drillerOptions[this.activity].subactivity_codes.map((item) => { return { 'text': item.description, 'value': item.registries_subactivity_code } })
          result.qualifications = this.drillerOptions[this.activity].well_class_codes.map((item) => { return { 'text': item.description, 'value': item.registries_well_class_code } })
          result.issuer = result.issuer.concat(this.drillerOptions[this.activity].accredited_certificate_codes.map((item) => { return { 'text': item.name + ' (' + item.cert_auth + ')', 'value': item.acc_cert_guid } }))
          result.approvalOutcome = result.approvalOutcome.concat(this.drillerOptions.approval_outcome_codes.map((item) => { return { 'text': item.code === 'P' ? 'Please select an option' : item.description, 'value': item.code } }))
          result.removalReasons = result.removalReasons.concat(this.drillerOptions.reason_removed_codes.map((item) => { return { 'text': item.description, 'value': item.code } }))
        }
      }
      return result
    },
    subactivityMap () {
      return this.activity in this.drillerOptions ? this.drillerOptions[this.activity].subactivity_codes : []
    },
    approvalDateState () {
      this.$emit('isValid', this.isAllDatesValid())
      return this.isDateValid(this.qualificationForm.application_outcome_date)
    },
    pendingDateState () {
      this.$emit('isValid', this.isAllDatesValid())
      return this.isDateValid(this.qualificationForm.application_recieved_date)
    },
    notificationDateState () {
      this.$emit('isValid', this.isAllDatesValid())
      return this.isDateValid(this.qualificationForm.application_outcome_notification_date)
    },
    removalDateState () {
      this.$emit('isValid', this.isAllDatesValid())
      return this.isDateValid(this.qualificationForm.removal_date)
    },
    showApprovalOutcome () {
      return ((!!this.qualificationForm.application_outcome_date && !!this.qualificationForm.application_recieved_date) ||
        (this.qualificationForm.qualificationForm && this.qualificationForm.qualificationForm.current_status && this.qualificationForm.qualificationForm.current_status.code))
    },
    showReasonDenied () {
      return !!this.qualificationForm.reason_denied ||
        (!!this.qualificationForm.application_outcome_date && this.qualificationForm.current_status.code === 'NA')
    },
    showNotificationDate () {
      return !!this.qualificationForm.application_outcome_notification_date || (!!this.qualificationForm.application_outcome_date && this.qualificationForm.current_status.code !== 'P')
    },
    showRemoval () {
      return !!this.qualificationForm.application_outcome_notification_date || !!this.qualificationForm.removal_date || (this.qualificationForm.removal_reason && this.qualificationForm.removal_reason.code)
    },
    showRemovalReason () {
      return !!this.qualificationForm.removal_date || !!this.qualificationForm.removal_reason.code
    },
    isEditMode () {
      return this.mode === 'edit'
    }
  }
}
</script>

<style>
.fixed-width-date-input {
  width: 150px;
  padding-right: 0px;
  margin-right: 0px;
}
.fixed-width .custom-control-label {
  width: 220px;
}
</style>
