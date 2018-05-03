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
    <b-modal id="qualificationModal" size="lg" title="Classification and Qualifications">
        <b-card title="Classification and Qualifications">
            <b-form>
                <div class="row">
                  <div class="col-md-3">Select classification:</div>
                  <div class="col-md-9">
                    <b-form-radio-group :options="classification">
                    </b-form-radio-group>
                  </div>
                </div>
                <b-form-group label="Certification">
                  <div class="row">
                    <div class="col-md-3">Issued by</div>
                    <div class="col-md-3">
                          <b-form-select :options="issuer"></b-form-select>
                    </div>
                    <div class="col-md-3">Certificate number</div>
                    <div class="col-md-3">
                      <b-form-input type="text" placeholder="Enter certificate number"></b-form-input>
                    </div>
                  </div>
                  <div class="row">
                    <b-button>Add additional certification</b-button>
                  </div>
                </b-form-group>
                <b-form-group label="Qualified to drill">
                    <b-form-checkbox-group :options="qualifications">
                    </b-form-checkbox-group>
                </b-form-group>
            </b-form>
        </b-card>
        <b-card title="Adjudication">
            <p class="card-text">
                <b-form>
                    <b-form-group label="Step 1 Date application received">
                        <datepicker :format="format"></datepicker>
                    </b-form-group>
                    <b-form-group label="Step 2">
                      <b-form-group label="Approval outcome date">
                        <datepicker :format="format"></datepicker>
                      </b-form-group>
                      <b-form-group label="Approval outcome">
                        <b-form-select :options="approval_outcome">
                        </b-form-select>
                      </b-form-group>
                      <b-form-group label="Reason denied">
                        <b-form-input type="text" placeholder="Enter reason denied"/>
                      </b-form-group>
                    </b-form-group>
                    <b-form-group label="Step 3 Notification date">
                      <datepicker :format="format"></datepicker>
                    </b-form-group>
                    <b-form-group label="Step 4">
                    <b-form-group label="Register status">
                      <b-form-select :options="register_status">
                      </b-form-select>
                    </b-form-group>
                    <b-form-group label="Registration date">
                      <datepicker :format="format"></datepicker>
                    </b-form-group>
                    </b-form-group>
                    <b-form-group label="Step 5">
                      <b-form-group label="Register removal date">
                        <datepicker :format="format"></datepicker>
                      </b-form-group>
                      <b-form-group label="Removal reason">
                        <b-form-select :options="removal_reason"></b-form-select>
                      </b-form-group>
                    </b-form-group>
                    <b-form-checkbox value="accepted" unchecked-value="not_accepted">
                      As Deputy Comptoller, I confirm I have reviewed the application or action and approved this registry update
                    </b-form-checkbox>
                    Date/Time and IDIR Stamp
                    <b-form-group>
                      <b-button>Add additional certification</b-button>
                    </b-form-group>
                </b-form>
            </p>
        </b-card>
    </b-modal>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
export default {
  components: {
    Datepicker
  },
  data () {
    return {
      format: 'yyyy-MM-dd',
      // TODO: Load issuer from DB ?
      issuer: [
        {value: null, text: 'Please select an option'},
        {value: 'Issuer 1', text: 'Issuer 1'},
        {value: 'Issuer 2', text: 'Issuer 2'}],
      // TODO: Load qualifications from DB ?
      qualifications: [
        {text: 'Qualification 1', value: 'Qualification 1'},
        {text: 'Qualification 2', value: 'Qualification 2'},
        {text: 'Qualification 3', value: 'Qualification 3'},
        {text: 'Qualification 4', value: 'Qualification 4'},
        {text: 'Qualification 5', value: 'Qualification 5'},
        {text: 'Qualification 6', value: 'Qualification 6'},
        {text: 'Qualification 7', value: 'Qualification 7'},
        {text: 'Qualification 8', value: 'Qualification 8'}],
      // TODO: Load qualifications from DB ?
      classification: [
        {text: 'Water Well Driller', value: 'Classification 1'},
        {text: 'Geotechnical/EnvironmentalDriller', value: 'Classification 2'},
        {text: 'Geotechnical/EnvironmentalDriller', value: 'Classification 3'},
        {text: 'Pump Installer', value: 'Classification 4'}
      ],
      approval_outcome: ['Approved', 'Not approved'],
      register_status: ['Pending'],
      removal_reason: ['No longer active',
        'Failed to maintain requirement of registration',
        'Did not meet the requirement of registration']
    }
  }
}
</script>
