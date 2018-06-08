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
    <div class="card w-100">
      <div class="card-body">
        <h5 class="card-title">Classification &amp; Qualifications
          <button type="button" class="close pull-right" aria-label="Close" v-on:click="$emit('close')">
            <span aria-hidden="true">&times;</span>
          </button>
        </h5>
        <p v-if="loading" class="card-text">
          <b-row>
            <b-col md="12">
              <div class="fa-2x text-center">
                <i class="fa fa-circle-o-notch fa-spin"></i>
              </div>
            </b-col>
          </b-row>
        </p>
        <p v-else class="card-text">
          <b-row>
            <b-col class="font-weight-bold">Certification</b-col>
          </b-row>
          <b-row>
            <b-col md="6">
              <b-form-group label="Issued by" horizontal :label-cols="3">
                <b-form-select :options="formOptions.issuer" v-model="qualificationForm.primary_certificate.acc_cert_guid" required></b-form-select>
              </b-form-group>
            </b-col>
            <b-col md="6">
              <b-form-group label="Certificate number" horizontal :label-cols="3">
                <b-form-input type="text" placeholder="Enter certificate number" v-model="qualificationForm.primary_certificate_no" required></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="12">
              <b-form-group label="Select classification" horizontal :label-cols="2" class="font-weight-bold">
                <b-form-radio-group class="fixed-width font-weight-normal pt-2" :options="formOptions.classifications" @change="changedClassification" v-model="qualificationForm.subactivity.registries_subactivity_code" required></b-form-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="8">
              <b-form-group label="Qualified to drill" class="font-weight-bold">
                <b-form-checkbox-group class="fixed-width font-weight-normal" :options="formOptions.qualifications" v-model="qualificationForm.qualifications" disabled>
                </b-form-checkbox-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="8">
              <h5>Adjudication</h5>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group horizontal :label-cols="5" label="Confirmed applicant is 19 years of age or older by reviewing" class="font-weight-bold">
                <b-form-select :options="formOptions.proofOfAge" v-model="qualificationForm.proof_of_age.code" required></b-form-select>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="4">
              <b-form-group horizontal :label-cols="4" label="Date application received (yyyy-mm-dd)" class="font-weight-bold" invalid-feedback="Invalid date format">
                <b-form-input type="date" v-model="qualificationForm.application_recieved_date" :state="pendingDateState"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="4" v-if="qualificationForm.application_recieved_date">
              <b-form-group horizontal :label-cols="4" label="Approval date outcome (yyyy-mm-dd)" class="font-weight-bold" invalid-feedback="Invalid date format">
                <b-form-input type="date" v-model="qualificationForm.application_outcome_date" :state="approvalDateState"/>
              </b-form-group>
            </b-col>
            <b-col md="4" v-if="qualificationForm.application_outcome_date">
              <b-form-group horizontal :label-cols="4" label="Approval outcome" class="font-weight-bold">
                <b-form-select :options="formOptions.approvalOutcome" v-model="currentStatusCode"/>
              </b-form-group>
            </b-col>
            <b-col md="4" v-if="qualificationForm.reason_denied || (qualificationForm.application_outcome_date && qualificationForm.current_status.code ==='NA')">
              <b-form-group horizontal :label-cols="4" label="Reason denied" class="font-weight-bold">
                <b-form-input type="text" v-model="qualificationForm.reason_denied"/>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="4" v-if="qualificationForm.application_outcome_notification_date || (qualificationForm.application_outcome_date && qualificationForm.current_status.code !== 'P')">
              <b-form-group horizontal :label-cols="4" label="Notification date" class="font-weight-bold">
                <b-form-input type="date" v-model="qualificationForm.application_outcome_notification_date" :state="notificationDateState"/>
              </b-form-group>
            </b-col>
          </b-row>
          <!-- slot for child elements to be added by parent component -->
          <slot></slot>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import moment from 'moment'
import { FETCH_DRILLER_OPTIONS } from '@/registry/store/actions.types'
export default {
  props: ['value', 'activity'],
  data () {
    return {
      qualificationForm: this.copyFormData(this.value)
    }
  },
  watch: {
    // Watching the entire object is expensive, but we need some way of notifying the parent.
    computedQualificationForm: {
      handler: function (val, oldVal) {
        this.$emit('input', val)
      },
      deep: true
    }
  },
  methods: {
    changedClassification (value) {
      const match = this.subactivityMap.filter(item => item.registries_subactivity_code === value)[0]
      this.qualificationForm.qualifications = match.qualification_set.map(item => item.well_class)
    },
    copyFormData (input) {
      // We need a default data structure when we're creating an application. If we're editing an
      // application, we can piggy back off the value being passed in.
      const defaultData = {
        subactivity: {
          registries_subactivity_code: null
        },
        primary_certificate_no: null,
        primary_certificate: {
          acc_cert_guid: null
        },
        proof_of_age: {
          code: null
        },
        qualifications: [],
        reason_denied: null
      }
      // It is important that we preserve the reference to the input variable, as the parent
      // component may be bound to it.
      const defaultCopy = JSON.parse(JSON.stringify(defaultData))
      return input ? Object.assign(input, ...defaultCopy) : defaultCopy
    },
    isDateValid (input) {
      // We accept null, undefined, '' as valid dates, in addition to correctly formatted dates
      return input ? moment(input, 'YYYY-MM-DD', true).isValid() : true
    },
    isAllDatesValid () {
      return (!this.approvalStatus || this.isDateValid(this.qualificationForm.application_outcome_date)) &&
        (!this.pendingStatus || this.isDateValid(this.qualificationForm.application_outcome_notification_date)) &&
        (!this.approvalStatus || this.isDateValid(this.qualificationForm.application_recieved_date))
    },
    ...mapActions([
      FETCH_DRILLER_OPTIONS
    ])
  },
  computed: {
    computedQualificationForm: function () {
      // We need to transform the bound dates to something that is acceptable to the API without affecting
      // the values to which the form are bound.
      // Make a deep copy, and transform the date fields.
      // TODO: do I have to transform the date fields?
      return JSON.parse(JSON.stringify(this.qualificationForm))
      // transformed.status_set.forEach((status) => { status.effective_date = status.effective_date && status.effective_date.length >= 10 ? status.effective_date.substring(0, 10) : status.effective_date })
    },
    ...mapGetters([
      'loading',
      'drillerOptions'
    ]),
    formOptions () {
      let result = {
        issuer: [{value: null, text: 'Please select an option'}],
        classifications: [],
        qualifications: [],
        proofOfAge: [{value: null, text: 'Please select an option'}],
        approvalOutcome: [{value: null, text: 'Please select an option'}]
      }
      if (this.drillerOptions) {
        // If driller options have loaded, prepare the form options.
        result.proofOfAge = result.proofOfAge.concat(this.drillerOptions.ProofOfAgeCode.map((item) => { return {'text': item.description, 'value': item.code} }))
        if (this.activity in this.drillerOptions) {
          // Different activities have different options.
          result.classifications = this.drillerOptions[this.activity].SubactivityCode.map((item) => { return {'text': item.description, 'value': item.registries_subactivity_code} })
          result.qualifications = this.drillerOptions[this.activity].WellClassCode.map((item) => { return {'text': item.description, 'value': item.registries_well_class_code} })
          result.issuer = result.issuer.concat(this.drillerOptions[this.activity].AccreditedCertificateCode.map((item) => { return {'text': item.name + ' (' + item.cert_auth + ')', 'value': item.acc_cert_guid} }))
          result.approvalOutcome = result.approvalOutcome.concat(this.drillerOptions.ApprovalOutcome.map((item) => { return {'text': item.description, 'value': item.code} }))
        }
      }
      return result
    },
    subactivityMap () {
      return this.activity in this.drillerOptions ? this.drillerOptions[this.activity].SubactivityCode : []
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
    currentStatusCode: {
      get () {
        return this.qualificationForm.current_status ? this.qualificationForm.current_status.code : null
      },
      set (newValue) {
        this.qualificationForm.current_status = {code: newValue}
      }
    }
  },
  created () {
    this.FETCH_DRILLER_OPTIONS()
  }
}
</script>

<style>
input[type='date'] {
  width: 150px;
  padding-right: 0px;
  margin-right: 0px;
}
.vdp-datepicker input {
  width: 80px;
}
.fixed-width .custom-control-label {
  width: 220px;
}
</style>
