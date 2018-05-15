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

    TODO: Add a note re. popup for warning when classification and qualifications is removed.
*/
<template>
  <div class="card w-100">
    <div class="card-body">
      <h5 class="card-title">Classification, Qualifications &amp; Adjudication
        <button type="button" class="close pull-right" aria-label="Close" v-on:click="$emit('close')">
          <span aria-hidden="true">&times;</span>
        </button>
      </h5>
      <p v-if="loaded" class="card-text">
        <b-form-group label="Certification">
          <b-row>
            <b-col md="2">Issued by</b-col>
            <b-col md="3">
                  <b-form-select :options="formOptions.issuer" v-model="qualificationForm.primary_certificate" required></b-form-select>
            </b-col>
            <b-col md="2">Certificate number</b-col>
            <b-col md="3">
              <b-form-input type="text" placeholder="Enter certificate number" v-model="qualificationForm.primary_certificate_no" required></b-form-input>
            </b-col>
          </b-row>
        </b-form-group>
        <b-row>
          <b-col md="2">Select classification</b-col>
          <b-col md="8">
            <b-form-radio-group class="fixed-width" :options="formOptions.classification" @change="changedClassification" v-model="qualificationForm.subactivity" required></b-form-radio-group>
          </b-col>
        </b-row>
        <b-form-group label="Qualified to drill">
          <b-row>
            <b-col md="8">
              <b-form-checkbox-group class="fixed-width" :options="formOptions.qualifications" v-model="qualificationForm.qualifications" disabled>
              </b-form-checkbox-group>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group label="Date application received">
          <b-row>
            <b-col>
              <datepicker :format="formOptions.format" v-model="qualificationForm.status_set[0].effective_date" required></datepicker>
            </b-col>
          </b-row>
        </b-form-group>
      </p>
      <p v-else class="card-text">
        <b-row>
          <b-col md="12">
            <div class="fa-2x text-center">
              <i class="fa fa-circle-o-notch fa-spin"></i>
            </div>
          </b-col>
        </b-row>
      </p>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import ApiService from '@/common/services/ApiService.js'
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
      },
      formOptions: {
        format: 'yyyy-MM-dd',
        // The issuer, qualifications and classifications options are all loaded from the API.
        issuer: [
          {value: null, text: 'Please select an option'}],
        qualifications: [],
        classification: []
      },
      loaded: false
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
    }
  },
  computed: {
    computedQualificationForm: function () {
      // We need to transform the bound dates to something that is acceptable to the API without affecting
      // the values to which the form are bound.
      // Make a deep copy, and transform the date fields.
      const transformed = JSON.parse(JSON.stringify(this.qualificationForm))
      transformed.status_set.forEach((status) => { status.effective_date = status.effective_date && status.effective_date.length >= 10 ? status.effective_date.substring(0, 10) : status.effective_date })
      return transformed
    }
  },
  beforeCreate () {
    // This could also be placed on PersonAdd, but it's nice having this component exists on it's own and bootstrap itself.
    ApiService.query('drillers/options/', {'activity': this.$options.propsData.activity}).then((response) => {
      this.subactivityMap = response.data.SubactivityCode
      this.formOptions.issuer = this.formOptions.issuer.concat(response.data.AccreditedCertificateCode.map((item) => { return {'text': item.name + ' (' + item.cert_auth + ')', 'value': item.acc_cert_guid} }))
      this.formOptions.classification = this.subactivityMap.map((item) => { return {'text': item.description, 'value': item.registries_subactivity_code} })
      this.formOptions.qualifications = response.data.WellClassCode.map((item) => { return {'text': item.description, 'value': item.registries_well_class_code} })
      // Set loaded flag to true, indicating that the view is now ready to show.
      this.loaded = true
    })
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
