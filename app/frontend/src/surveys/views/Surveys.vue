<template>
  <div>
    <Card v-if="commonStore.userRoles && commonStore.userRoles.surveys.edit" class="container">
      <fieldset>
        <legend id="surveyList">Current Surveys</legend>
        <DataTable
          id="survey-table"
          :value="currentSurveys"
          paginator
          :totalRecords="totalSurveys"
          :rows="perPage"
        >
          <template #empty>There are no surveys available.</template>
          <template v-slot:cell(survey_page)="row">
            {{formatPageName(row.item.survey_page)}}
          </template>
          <template v-slot:cell(survey_link)="row">
            <a :href="row.item.survey_link" target="_blank">{{row.item.survey_link}}</a>
          </template>
          <template v-slot:cell(survey_enabled)="data">
            <Checkbox v-model="row.item.survey_enabled" name="check-button" @input="toggleSurveyEnabled(row.item.survey_guid, row.item.survey_enabled)"/>
          </template>
          <template v-slot:cell(remove)="data">
            <Button type="button" severity="danger" outlined size="small" @click="handleRemoveSurvey(row.item.survey_guid)"><i class="fa fa-trash"></i></Button>
          </template>
        </DataTable>
      </fieldset>
      <fieldset>
        <legend>Add a Survey</legend>
        <Form @submit="submitForm" @reset="resetForm">
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

          <tr>
            <td cols="12" sm="6">
              <form-input
                id="surveyPageSelect"
                label="Survey page"
                select
                :options="pageOptions"
                placeholder="Select page"
                :errors="errors['survey_page']"
                v-model="form.survey_page"
              ></form-input>
            </td>
          </tr>
          <tr class="mt-3">
            <td cols="12" sm="6">
              <Checkbox v-model="form.survey_enabled" name="check-button">
                Enable survey immediately
              </Checkbox>
            </td>
          </tr>
          <tr class="mt-4">
            <td>
              <Button type="submit">Save</Button>
            </td>
          </tr>
        </Form>
      </fieldset>
      <Dialog
          v-model="removeSurveyModal"
          centered
          title="Confirm remove"
          @shown="focusRemoveModal">
        Are you sure you want to remove this survey?
        <div slot="modal-footer">
          <Button severity="secondary" @click="removeSurveyModal=false;surveyToRemove=null" ref="cancelRemoveBtn">
            Cancel
          </Button>
          <Button severity="danger" @click="removeSurveyModal=false;removeSurvey(surveyToRemove)">
            Remove
          </Button>
        </div>
      </Dialog>
    </Card>
    <Card v-else class="container">
      <b-card-body>
        <div id="loginMsg">Please log in to continue.</div>
      </b-card-body>
    </Card>
  </div>

</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { useCommonStore } from '@/stores/common.js'

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
    commonStore () { return useCommonStore() },
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
    }
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
