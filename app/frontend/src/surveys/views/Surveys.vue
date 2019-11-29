<template>
  <div>
    <b-card v-if="userRoles && userRoles.surveys.edit" class="container">
      <fieldset>
        <legend id="surveyList">Current Surveys</legend>
        <b-table
          id="survey-table"
          responsive
          :fields="fields"
          show-empty
          empty-text="There are no surveys available."
          :items="currentSurveys"
          :per-page="perPage"
          :current-page="currentPage"
        >
          <template slot="survey_page" slot-scope="row">
            {{formatPageName(row.item.survey_page)}}
          </template>
          <template slot="survey_link" slot-scope="row">
            <a :href="row.item.survey_link" target="_blank">{{row.item.survey_link}}</a>
          </template>
          <template slot="survey_enabled" slot-scope="row">
            <b-form-checkbox v-model="row.item.survey_enabled" name="check-button" @input="toggleSurveyEnabled(row.item.survey_guid, row.item.survey_enabled)"/>
          </template>
          <template slot="remove" slot-scope="row">
            <b-btn type="button" variant="outline-danger" size="sm" @click="handleRemoveSurvey(row.item.survey_guid)"><i class="fa fa-trash"></i></b-btn>
          </template>
        </b-table>
        <b-pagination v-if="totalSurveys > perPage"
          v-model="currentPage"
          :total-rows="totalSurveys"
          :per-page="perPage"
          aria-controls="survey-table"
        ></b-pagination>
      </fieldset>
      <fieldset>
        <legend>Add a Survey</legend>
        <b-form @submit.prevent="submitForm" @reset.prevent="resetForm">
          <form-input
            id="surveyTextInput"
            label="Survey text"
            :errors="errors['survey_introduction_text']"
            v-model="form.survey_introduction_text"
          ></form-input>
          <form-input
            id="surveyLinkInput"
            label="Survey link"
            v-model="form.survey_link"
            :errors="errors['survey_link']"
          ></form-input>

          <b-row>
            <b-col cols="12" sm="6">
              <form-input
                id="surveyPageSelect"
                label="Survey page"
                select
                :options="pageOptions"
                placeholder="Select page"
                :errors="errors['survey_page']"
                v-model="form.survey_page"
              ></form-input>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col cols="12" sm="6">
              <b-form-checkbox v-model="form.survey_enabled" name="check-button">
                Enable survey immediately
              </b-form-checkbox>
            </b-col>
          </b-row>
          <b-row class="mt-4">
            <b-col>
              <b-btn type="submit" variant="primary">Save</b-btn>
            </b-col>
          </b-row>
        </b-form>
      </fieldset>
      <b-modal
          v-model="removeSurveyModal"
          centered
          title="Confirm remove"
          @shown="focusRemoveModal">
        Are you sure you want to remove this survey?
        <div slot="modal-footer">
          <b-btn variant="secondary" @click="removeSurveyModal=false;surveyToRemove=null" ref="cancelRemoveBtn">
            Cancel
          </b-btn>
          <b-btn variant="danger" @click="removeSurveyModal=false;removeSurvey(surveyToRemove)">
            Remove
          </b-btn>
        </div>
      </b-modal>
    </b-card>
    <b-card v-else class="container">
      <b-card-body>
        <div id="loginMsg">Please log in to continue.</div>
      </b-card-body>
    </b-card>
  </div>

</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'

export default {
  name: 'Surveys',
  data () {
    return {
      currentSurveys: [],
      removeSurveyModal: false,
      surveyToRemove: null,
      form: {},
      errors: {},
      fields: [
        {
          key: 'survey_page',
          label: 'Page',
          sortable: true
        },
        {
          key: 'survey_introduction_text',
          label: 'Survey text',
          sortable: false
        },
        {
          key: 'survey_link',
          label: 'Link',
          sortable: false
        },
        {
          key: 'survey_enabled',
          label: 'Enabled',
          sortable: true
        },
        { key: 'remove', label: 'Remove' }
      ],
      // this is a list of survey pages that an admin user can create surveys for.
      // Individual pages currently look for a survey with the corresponding letter (not great design).
      // TODO: if adding more survey choices, refactor to use a code table on backend and
      // populate frontend using an options endpoint.
      pageMapping: {
        r: 'Registry',
        a: 'Aquifers',
        s: 'Well Search',
        w: 'Well Summary',
        u: 'Activity Submissions',
        e: 'Staff Edit'
      },
      perPage: 5,
      currentPage: 1
    }
  },
  computed: {
    // transform the pageMapping object into an array of objects of the format { value: x, text: y },
    // where x is a key of pageMapping.
    pageOptions () {
      const opts = []
      for (let [k, v] of Object.entries(this.pageMapping)) {
        opts.push({
          value: k,
          text: v
        })
      }
      return opts
    },
    totalSurveys () {
      return this.currentSurveys.length
    },
    ...mapGetters(['userRoles'])
  },
  methods: {
    submitForm () {
      ApiService.post('surveys', this.form).then(() => {
        this.getSurveys()
        this.resetForm()
        this.$noty.success('Survey created.')
      }).catch((e) => {
        this.errors = e.response.data
      })
    },
    resetForm () {
      this.form = {
        survey_introduction_text: '',
        survey_link: '',
        survey_page: '',
        survey_enabled: false
      }
      this.errors = {}
    },
    getSurveys () {
      ApiService.query('surveys').then((response) => {
        if (response.data) {
          this.currentSurveys = response.data
        }
      }).catch((e) => {
        console.error(e)
      })
    },
    formatPageName (code) {
      return this.pageMapping[code] || code
    },
    handleRemoveSurvey (id) {
      this.removeSurveyModal = true
      this.surveyToRemove = id
    },
    removeSurvey (id) {
      ApiService.delete('surveys', id).then(() => {
        this.getSurveys()
        this.$noty.success('Survey removed.')
      }).catch((e) => {
        this.$noty.error('Error deleting survey. Please try again later.')
      })
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    toggleSurveyEnabled (id, currentVal) {
      ApiService.patch('surveys', id, {
        survey_enabled: currentVal
      }).then((r) => {
        this.getSurveys()
        this.$noty.success(`Survey ${r.data.survey_enabled ? 'enabled' : 'disabled'}.`)
      })
    }
  },
  created () {
    this.getSurveys()
    this.resetForm()
  }
}
</script>

<style>
</style>
