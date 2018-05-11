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
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Classification, Qualifications &amp; Adjudication
        <button type="button" class="close pull-right" aria-label="Close" v-on:click="$emit('close')">
          <span aria-hidden="true">&times;</span>
        </button>
      </h5>
      <p class="card-text">
        <b-row>
          <div class="col-md-2">Select classification:</div>
          <div class="col-md-8">
            <b-form-radio-group class="fixed-width" :options="formOptions.classification" @change="changedClassification" v-model="qualificationForm.subactivity"></b-form-radio-group>
          </div>
        </b-row>
        <b-form-group label="Certification">
          <b-row v-for="item in qualificationForm.certifications" :key="item.id">
            <div class="col-md-1">Issued by</div>
            <div class="col-md-3">
                  <b-form-select :options="formOptions.issuer" v-model="item.issuer"></b-form-select>
            </div>
            <div class="col-md-2">Certificate number</div>
            <div class="col-md-3">
              <b-form-input type="text" placeholder="Enter certificate number" v-model="item.number"></b-form-input>
            </div>
          </b-row>
          <b-row class="mt-2">
            <b-col>
              <b-button variant="primary" v-on:click="addCertification()">Add additional certification</b-button>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group label="Qualified to drill">
            <b-row>
              <div class="col-md-8">
                <b-form-checkbox-group class="fixed-width" :options="formOptions.qualifications" v-model="qualificationForm.qualifications">
                </b-form-checkbox-group>
              </div>
            </b-row>
        </b-form-group>
        <b-row>
          <div class="col-md-4 pr-0">
            <span class="pr-1">Step 1</span> Date application received
            <datepicker :format="formOptions.format" v-model="qualificationForm.applicationReceivedDate" class="pull-right"></datepicker>
          </div>
        </b-row>
        <b-row class="mt-2">
          <div class="col-md-4 pr-0">
            <span class="pr-1">Step 2</span> Approval outcome date
            <datepicker :format="formOptions.format" v-model="qualificationForm.approvalOutcomeDate" class="pull-right"></datepicker>
          </div>
          <div class="col-md-2">Approval outcome</div>
          <div class="col-md-2"><b-form-select :options="formOptions.approval_outcome" v-model="qualificationForm.approvalOutcome"></b-form-select></div>
          <div class="col-md-2">Reason denied</div>
          <div class="col-md-2"><b-form-input type="text" v-model="qualificationForm.reasonDenied" placeholder="Enter reason denied"/></div>
        </b-row>
        <b-row class="mt-2">
          <div class="col-md-4 pr-0">
            <span class="pr-1">Step 3</span> Notification date
            <datepicker :format="formOptions.format" v-model="qualificationForm.notificationDate" class="pull-right"></datepicker>
          </div>
        </b-row>
        <b-row class="mt-2">
          <div class="col-md-2 pr-0"><span class="pr-1">Step 4 </span>Register status</div>
          <div class="col-md-2 p-0"><b-form-select :options="formOptions.register_status" v-model="qualificationForm.registerStatus"></b-form-select></div>
          <div class="col-md-2">Registration date</div>
          <div class="col-md-2"><datepicker :format="formOptions.format" class="pull-right" v-model="qualificationForm.registrationDate"></datepicker></div>
        </b-row>
        <b-row class="mt-2">
          <div class="col-md-4 pr-0"><span class="pr-1">Step 5 </span>Register removal date
              <datepicker :format="formOptions.format" class="pull-right" v-model="qualificationForm.registerRemovalDate"></datepicker>
          </div>
          <div class="col-md-2">Removal reason</div>
          <div class="col-md-6">
              <b-form-select :options="formOptions.removal_reason" v-model="qualificationForm.removalReason"></b-form-select>
          </div>
        </b-row>
        <b-row>
          <div class="col-md-12">
            <b-form-checkbox value="accepted" unchecked-value="not_accepted" v-model="qualificationForm.approved">
              As Deputy Comptoller, I confirm I have reviewed the application or action and approved this registry update
            </b-form-checkbox>
          </div>
        </b-row>
        <!-- TODO: <b-row>
          <b-col>Date/Time and IDIR Stamp</b-col>
        </b-row> -->
      </p>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
export default {
  components: {
    Datepicker
  },
  props: ['value'],
  data () {
    return {
      qualificationForm: {
        subactivity: null,
        certifications: [
          {id: 0, issuer: null, number: null}
        ],
        qualifications: [],
        applicationReceivedDate: null,
        approvalOutcomeDate: null,
        approvalOutcome: null,
        reasonDenied: null,
        notificationDate: null,
        registerStatus: null,
        registrationDate: null,
        registerRemovalDate: null,
        removalReason: null,
        approved: null
      },
      formOptions: {
        format: 'yyyy-MM-dd',
        // TODO: Load issuer from DB ?
        issuer: [
          {value: null, text: 'Please select an option'},
          {value: 'CGWA', text: 'CGWA'},
          {value: 'Province of B.C.', text: 'Province of B.C.'}],
        // TODO: Load qualifications from DB ?
        qualifications: [
          {text: 'Water supply wells', value: 'Water supply wells'},
          {text: 'Monitoring wells', value: 'Monitoring wells'},
          {text: 'Recharge wells', value: 'Recharge wells'},
          {text: 'Injection wells', value: 'Injection wells'},
          {text: 'Dewatering wells', value: 'Dewatering wells'},
          {text: 'Remediation wells', value: 'Remediation wells'},
          {text: 'Geotechnical wells', value: 'Geotechnical wells'},
          {text: 'Closed-loop geoexchange wells', value: 'Closed-loop geoexchange wells'}],
        // TODO: Load qualifications from DB ?
        classification: [
          {text: 'Water Well Driller', value: 'WATER'},
          {text: 'Geotechnical/EnvironmentalDriller', value: 'GEOTECH'},
          {text: 'Geoexchange Driller', value: 'GEOXCHG'},
          {text: 'Grandparented up to Nov 2006', value: 'PHASE1'},
          {text: 'Grandparented up to Feb 29, 2016', value: 'PHASE2'},
          {text: 'Pump Installer', value: 'PUMPINST'}
        ],
        approval_outcome: ['Approved', 'Not approved'],
        register_status: ['Pending'],
        removal_reason: ['No longer active',
          'Failed to maintain requirement of registration',
          'Did not meet the requirement of registration']
      },
      certificationCount: 1
    }
  },
  watch: {
    qualificationForm: {
      handler: function (val, oldVal) {
        this.$emit('input', val)
      },
      deep: true
    }
  },
  methods: {
    addCertification () {
      this.qualificationForm.certifications.push({id: ++this.certificationCount, issuer: null, number: null})
    },
    changedClassification (value) {
      const map = {
        'DRILL': ['Water supply wells', 'Monitoring wells', 'Recharge wells', 'Injection wells', 'Dewatering wells', 'Remediation wells', 'Geotechnical wells'],
        'GEOTECH': ['Monitoring wells', 'Remediation wells', 'Geotechnical wells'],
        'GEOXCHG': ['Closed-loop geoexchange wells']
      }
      if (value in map) {
        this.qualificationForm.qualifications = map[value]
      } else {
        this.qualificationForm.qualifications = []
      }
    }
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
