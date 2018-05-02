<template>
    <b-modal id="qualificationModal" title="Classification and Qualifications">
        <b-card title="Classification and Qualifications">
            <b-form>
                <b-form-group label="Select classification.">
                    <b-form-radio-group :options="classification">
                    </b-form-radio-group>
                </b-form-group>
                <b-form-group label="Certification">
                    <b-form-group label="Issued by">
                        <b-form-select :options="issuer">
                        </b-form-select>
                    </b-form-group>
                    <b-form-group label="Certificate Number">
                        <b-form-input type="text" placeholder="Enter certificate number"></b-form-input>
                    </b-form-group>
                    <b-button>Add additional certification</b-button>
                </b-form-group>
                <b-form-group label="Qualified to drill">
                    <b-form-checkbox-group :options="qualifications">
                    </b-form-checkbox-group>
                </b-form-group>
            </b-form>
        </b-card>
        <b-card title="Adjudication">
            <p class="card-text">
            </p>
        </b-card>
    </b-modal>
</template>

<script>
export default {
  data () {
    return {
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
      classification: [
        {text: 'Classification 1', value: 'Classification 1'},
        {text: 'Classification 2', value: 'Classification 2'}
      ]
    }
  }
}
</script>
