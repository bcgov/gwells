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
  <div class="card w-100">
    <div class="card-body">
      <h5 class="card-title">Classification, Qualifications &amp; Adjudication
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
          <b-col>Certification</b-col>
        </b-row>
        <b-row>
          <b-col md="6">
            <b-form-group label="Issued by" horizontal :label-cols="3" label-for="issuer">
              <b-form-select id="issuer" :options="formOptions.issuer" v-model="qualificationForm.primary_certificate" required></b-form-select>
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Certificate number" label-for="primary_certificate_no" horizontal :label-cols="3">
              <b-form-input id="primary_certificate_no" type="text" placeholder="Enter certificate number" v-model="qualificationForm.primary_certificate_no" required></b-form-input>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row class="mt-3">
          <b-col md="12">
            <b-form-group label="Select classification" label-for="classifications" horizontal :label-cols="2">
              <b-form-radio-group id="classifications" class="fixed-width" :options="formOptions.classifications" @change="changedClassification" v-model="qualificationForm.subactivity" required></b-form-radio-group>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="8">
            <b-form-group label="Qualified to drill" label-for="qualifications">
              <b-form-checkbox-group id="qualifications" class="fixed-width" :options="formOptions.qualifications" v-model="qualificationForm.qualifications" disabled>
              </b-form-checkbox-group>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group label="Date application received" label-for="effective_date">
              <datepicker id="effective_date" format="yyyy-MM-dd" v-model="qualificationForm.status_set[0].effective_date" required></datepicker>
            </b-form-group>
          </b-col>
        </b-row>
      </p>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import { mapGetters, mapActions } from 'vuex'
export default {
  components: {
    Datepicker
  },
  props: ['value', 'activity'],
  data () {
    return {
      qualificationForm: {
        subactivity: null,
        primary_certificate_no: null,
        primary_certificate: null,
        status_set: [
          {
            effective_date: null,
            status: 'P'
          }
        ],
        qualifications: []
      }
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
    ...mapActions([
      'fetchDrillerOptions'
    ])
  },
  computed: {
    computedQualificationForm: function () {
      // We need to transform the bound dates to something that is acceptable to the API without affecting
      // the values to which the form are bound.
      // Make a deep copy, and transform the date fields.
      const transformed = JSON.parse(JSON.stringify(this.qualificationForm))
      transformed.status_set.forEach((status) => { status.effective_date = status.effective_date && status.effective_date.length >= 10 ? status.effective_date.substring(0, 10) : status.effective_date })
      return transformed
    },
    ...mapGetters([
      'loading',
      'drillerOptions'
    ]),
    formOptions () {
      let result = {
        issuer: [{value: null, text: 'Please select an option'}],
        classifications: [],
        qualifications: []
      }
      if (this.activity in this.drillerOptions) {
        const options = this.drillerOptions[this.activity]
        result.issuer = result.issuer.concat(options.AccreditedCertificateCode.map((item) => { return {'text': item.name + ' (' + item.cert_auth + ')', 'value': item.acc_cert_guid} }))
        result.classifications = options.SubactivityCode.map((item) => { return {'text': item.description, 'value': item.registries_subactivity_code} })
        result.qualifications = options.WellClassCode.map((item) => { return {'text': item.description, 'value': item.registries_well_class_code} })
      }
      return result
    },
    subactivityMap () {
      return this.activity in this.drillerOptions ? this.drillerOptions[this.activity].SubactivityCode : []
    }
  },
  created () {
    this.fetchDrillerOptions({activity: this.activity})
  }
}
</script>

<style>
.vdp-datepicker input {
  width: 80px;
}
.fixed-width .custom-control-label {
  width: 220px;
}
</style>
