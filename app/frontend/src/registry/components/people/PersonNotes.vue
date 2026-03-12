<template>
  <div class="card mb-3" ref="noteSection">
    <div class="card-body p-2 p-md-3">
      <h6 class="card-title" id="notesSectionTitle">Notes</h6>
      <div class="mt-3 mb-4" v-if="userRoles.registry.edit">
        <b-form @submit.prevent="noteSubmitHandler" @reset.prevent="noteCancelHandler">
          <Form
              id="noteInputGroup"
              label="Add a note:"
              label-for="noteInput">
            <b-form-textarea id="noteInput" v-model="noteInput" :rows="3" :max-rows="6" :disabled="submitLoading"></b-form-textarea>
          </Form>
          <div class="submit-row">
            <Button type="submit" variant="primary" :disabled="!noteInput || submitLoading" ref="noteInputSaveBtn">Save</Button>
            <Button type="reset" variant="light" :disabled="!noteInput" ref="noteInputCancelBtn">Cancel</Button>
            <p
              class="font-weight-bold text-count"
              :class="[invalidNewNoteLength ? 'error': '']"
            >
              {{ noteInput.length }}/{{ maxNoteLength }}
            </p>
          </div>
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
          <!-- Delete Note Modal  -->
          <b-modal
            v-model="confirmDeleteModal"
            centered
            title="Confirm Deletion"
            @shown="focusDeleteModal"
            :return-focus="$refs.noteInputCancelBtn"
          >
            <p>Are you sure you want to delete this note?</p>
            <div v-if="activeNote" class="">
              <p class="font-weight-bold wb">"{{activeNote.note}}"</p>
            </div>
            <div slot="modal-footer" class="buttons">
              <b-btn
                variant="light"
                @click="confirmDeleteModal=false"
                ref="cancelDeleteBtn"
              >
                Cancel
              </b-btn>
              <b-btn
                variant="danger"
                @click="confirmDeleteModal=false;deleteNote()"
              >
                Delete
              </b-btn>
            </div>
          </b-modal>
          <!-- Edit Modal -->
          <b-modal
              v-model="confirmEditNoteModal"
              centered
              title="Editing Note"
              @shown="focusEditNoteModal"
              :return-focus="$refs.noteInputCancelBtn"
            >
            <div>
              <b-form-textarea
                id="editNoteTextArea"
                v-model="noteContentEdit"
                placeholder="Edit Note..."
                rows="4"
                max-rows="6"
              />
              <p class="font-weight-bold text-count" :class="[invalidEditNoteLength ? 'error': '']">
              {{ noteContentEdit.length }}/{{ maxNoteLength }}
              </p>
            </div>
            <div slot="modal-footer" class="buttons">
              <b-btn variant="light" @click="confirmEditNoteModal=false" ref="cancelEditNoteCancelBtn">
                Cancel
              </b-btn>
              <b-btn variant="primary" :disabled="invalidEditNoteLength || !noteContentEdit" @click="notePatchHandle()">
                Submit
              </b-btn>
            </div>
          </b-modal>
        </b-form>
      </div>
      <div id="notesList" ref="notes">
        <div v-if="!notes || !notes.length">
          <div class="row"><div class="col">No notes for this person.</div></div>
        </div>
        <div class="mt-5 note-container" v-if="notes && notes.length">
          <div class="note wb" v-for="(note, index) in notes" :key="`note ${index}`" :id="`person-note-${index}`">
            <p>
              <span class="font-weight-bold">{{ note.author }}</span> ({{ note.date | moment("MMMM Do YYYY [at] LT") }}):
              {{ note.note }}
            </p>
            <div class="crud-options">
              <b-btn
                :disabled="keycloak.idTokenParsed.display_name !== note.author"
                @click="noteEditHandler(note)"
                size="sm"
                variant="primary"
              >
                <i class="fa fa-edit"></i>
                Edit
              </b-btn>
              <b-btn
                :disabled="!userRoles.registry.admin && keycloak.idTokenParsed.display_name !== note.author"
                @click="noteDeleteHandler(note)"
                size="sm"
                variant="danger"
              >
                &#x2715;
              </b-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import smoothScroll from 'smoothscroll'

import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'PersonNotes',
  data () {
    return {
      noteInput: '',
      submitLoading: false,
      submitSuccess: false,
      submitError: false,
      confirmEditNoteModal: false,
      confirmSubmitModal: false,
      confirmCancelModal: false,
      confirmDeleteModal: false,
      noteContentEdit: '',
      activeNote: null,
      maxNoteLength: 900
    }
  },
  computed: {
    notes () {
      if (this.currentDriller && this.currentDriller.notes) {
        return this.currentDriller.notes
      }
      return []
    },
    invalidNewNoteLength () { return this.noteInput.length > this.maxNoteLength },
    invalidEditNoteLength () { return this.noteContentEdit.length > this.maxNoteLength },
    ...mapGetters([
      'userRoles',
      'keycloak'
    ]),
    ...mapGetters('registriesStore', [
      'currentDriller'
    ])

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
          smoothScroll(notes, 1000)
          this.$emit('updated')
        }).catch((e) => {
          this.submitLoading = false
          this.submitError = e.response.data
        })
    },
    noteEditHandler (note) {
      const editRegexChromium = /^\(Edited \d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2}:\d{2} (AM|PM)\)\s/
      const editRegexFirefox = /^\(Edited \d{4}-\d{1,2}-\d{1,2}, \d{1,2}:\d{2}:\d{2} (a.m.|p.m.)\)\s/
      this.noteContentEdit = note.note.replace(editRegexChromium, '')
      this.noteContentEdit = this.noteContentEdit.replace(editRegexFirefox, '')
      this.activeNote = note
      this.confirmEditNoteModal = true
    },
    noteDeleteHandler (note) {
      this.activeNote = note
      this.confirmDeleteModal = true
    },
    noteCancelDeleteHandler () {
      this.activeNote = null
    },
    focusEditNoteModal () {
      this.$refs.cancelEditNoteCancelBtn.focus()
    },
    focusDeleteModal () {
      this.$refs.cancelDeleteBtn.focus()
    },
    deleteNote () {
      ApiService.delete(`drillers/${this.currentDriller.person_guid}/notes`, this.activeNote.person_note_guid)
        .then(() => {
          this.activeNote = null
          this.alertText = 'Note deleted.'
          this.submitSuccess = true
          this.$emit('updated')
        })
        .catch((e) => {
          this.errorHandler(e)
        })
    },
    notePatchHandle () {
      const updatedNote = `(Edited ${new Date().toLocaleString()}) ` + this.noteContentEdit
      ApiService.patch(`drillers/${this.currentDriller.person_guid}/notes`, this.activeNote.person_note_guid, { note: updatedNote })
        .then(() => {
          this.noteReset()
          this.activeNote = null
          this.noteContentEdit = ''
          this.confirmEditNoteModal = false
          this.alertText = 'Note updated.'
          this.submitSuccess = true
          this.$emit('updated')
        })
        .catch((e) => {
          this.errorHandler(e)
        })
    },
    errorHandler (e) {
      this.submitLoading = false
      if (e.response.status === 500) { this.submitError = 'Service unavailable - try again later' } else { this.submitError = e.response.data }
      alert(`An error has occured:\n\n${this.submitError}`)
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

<style lang="scss">
  .crud-options {
    display: flex;
    margin-left: 0.5em;
    width: auto;
  }
  .crud-options button:last-child {
    margin-left: 0.5em;
  }
  .note {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 0.5em;
    border-radius: 4pt;
  }
  .note:hover {
    transition: 0.2s;
    background-color: #F8F8F8;
  }
  .note p {
    padding: 0;
    margin: 0;
  }
  .buttons button:last-child {
    margin-left: 0.5em;
  }
  .wb {
    word-break: break-all;
  }
  .error {
    color: red;
  }
  .text-count {
    width: 100%;
    text-align: right;
    padding: 0.5em 1em 0 0;
  }
  .submit-row {
    display: flex;
    flex-direction: row;
  }
  .row {
    display: flex;
    flex-wrap: wrap;
    margin-left: -15px;
    margin-right: -15px;
  }
  .col {
    flex: 1 1 0%;
    padding-left: 15px;
    padding-right: 15px;
  }
</style>
