<template>
  <div class="card" ref="noteSection">
    <div class="card-body p-2 p-md-3">
      <h6 class="card-title" id="notesSectionTitle">Notes</h6>
      <div class="mt-3">
        <b-form @submit.prevent="noteSubmitHandler" @reset.prevent="noteCancelHandler">
          <b-form-group
              id="noteInputGroup"
              label="Add a note:"
              label-for="noteInput">
            <b-form-textarea id="noteInput" v-model="noteInput" :rows="3" :max-rows="6" :disabled="submitLoading"></b-form-textarea>
          </b-form-group>
          <b-button type="submit" variant="primary" :disabled="!noteInput || submitLoading" ref="noteInputSaveBtn">Save</b-button>
          <b-button type="reset" variant="light" :disabled="!noteInput" ref="noteInputCancelBtn">Cancel</b-button>
          <b-alert
              class="mt-3"
              variant="success"
              dismissible
              :show="submitSuccess"
              @dismissed="submitSuccess=false">Note added.</b-alert>
          <b-modal
              v-model="confirmSubmitModal"
              centered
              title="Confirm save"
              @shown="focusSubmitModal"
              :return-focus="$refs.noteInputSaveBtn">
            Are you sure you want to save this note?
            <div slot="modal-footer">
              <b-btn variant="primary" @click="confirmSubmitModal=false;noteSubmit()" ref="confirmSubmitConfirmBtn">
                Save
              </b-btn>
              <b-btn variant="light" @click="confirmSubmitModal=false">
                Cancel
              </b-btn>
            </div>
          </b-modal>
          <b-modal
              v-model="confirmCancelModal"
              centered
              title="Confirm cancel"
              @shown="focusCancelModal"
              :return-focus="$refs.noteInputCancelBtn">
            Your note is not saved. Are you sure you want to discard your changes?
            <div slot="modal-footer">
              <b-btn variant="secondary" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn">
                Cancel
              </b-btn>
              <b-btn variant="danger" @click="confirmCancelModal=false;noteReset()">
                Discard
              </b-btn>
            </div>
          </b-modal>
        </b-form>
      </div>
      <div id="notesList" ref="notes">
        <div class="mt-5" v-if="!sortedNotes || !sortedNotes.length">
          <b-row><b-col>No notes for this person.</b-col></b-row>
        </div>
        <div class="mt-5" v-if="sortedNotes && sortedNotes.length">
          <div class="mt-3" v-for="(note, index) in sortedNotes" :key="`note ${index}`" :id="`person-note-${index}`">
              <span class="font-weight-bold">{{ note.author }}</span> ({{ note.date | moment("MMMM Do YYYY [at] LT") }}):
              {{ note.note }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'PersonNotes',
  data () {
    return {
      noteInput: '',
      submitLoading: false,
      submitSuccess: false,
      submitError: false,
      confirmSubmitModal: false,
      confirmCancelModal: false
    }
  },
  computed: {
    sortedNotes () {
      if (this.currentDriller && this.currentDriller.notes && this.currentDriller.notes.length) {
        let notes = JSON.parse(JSON.stringify(this.currentDriller.notes)).sort((a, b) => {
          return (Date(a.date) < Date(b.date)) ? -1 : 1
        })
        return notes
      }
      return []
    },
    ...mapGetters(['currentDriller'])
  },
  methods: {
    noteSubmit () {
      // submit the note as a post request, triggered after confirming via popup
      this.submitSuccess = false
      this.submitError = false
      this.submitLoading = true
      ApiService.post(`drillers/${this.currentDriller.person_guid}/notes`, { note: this.noteInput })
        .then((response) => {
          const notes = this.$refs.noteSection
          this.noteReset()
          this.submitLoading = false
          this.submitSuccess = true
          this.$SmoothScroll(notes, 1000)
          this.$emit('updated')
        }).catch((e) => {
          this.submitLoading = false
          this.submitError = e.response.data
        })
    },
    noteReset () {
      this.submitSuccess = false
      this.submitError = false
      this.submitLoading = false
      this.noteInput = ''
    },
    noteSubmitHandler () {
      // trigger popup to confirm submit
      this.confirmSubmitModal = true
    },
    noteCancelHandler () {
      // trigger popup to confirm discard note
      this.confirmCancelModal = true
    },
    focusCancelModal () {
      // focus the "cancel" button in the confirm discard popup
      this.$refs.cancelSubmitCancelBtn.focus()
    },
    focusSubmitModal () {
      // focus the "submit" button in the confirm save note popup
      this.$refs.confirmSubmitConfirmBtn.focus()
    }
  }
}
</script>

<style>

</style>
