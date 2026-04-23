<template>
  <div class="card mb-3" ref="noteSection">
    <div class="card-body p-2 p-md-3">
      <h6 class="card-title" id="notesSectionTitle">Notes</h6>
      <div class="mt-3 mb-4" v-if="commonStore.userRoles.registry.edit">
        <Form @submit.prevent="noteSubmitHandler" @reset.prevent="noteCancelHandler">
          <div
            class="flex flex-col gap-2"
            id="noteInputGroup"
            label="Add a note:"
            label-for="noteInput">
            <Textarea id="noteInput" v-model="noteInput" :rows="3" :max-rows="6" :disabled="submitLoading"></Textarea>
          </div>
          <div class="flex-row">
            <Button type="submit" variant="primary" :disabled="!noteInput || submitLoading" ref="noteInputSaveBtn">Save</Button>
            <Button type="reset" variant="light" :disabled="!noteInput" ref="noteInputCancelBtn">Cancel</Button>
            <p
              class="font-weight-bold text-count"
              :class="[invalidNewNoteLength ? 'error': '']"
            >
              {{ noteInput.length }}/{{ maxNoteLength }}
            </p>
          </div>
          <Message
              class="mt-3"
              severity="success"
              dismissible
              :show="submitSuccess"
              @dismissed="submitSuccess=false">Note added.</Message>
          <Dialog
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
          </Dialog>
          <Dialog
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
          </Dialog>
          <!-- Delete Note Modal  -->
          <Dialog
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
          </Dialog>
          <!-- Edit Modal -->
          <Dialog
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
          </Dialog>
        </Form>
      </div>
      <div id="notesList" ref="notes">
        <div v-if="!notes || !notes.length">
          <b-row><b-col>No notes for this person.</b-col></b-row>
        </div>
        <div class="mt-5 p-4 border border-gray-200 rounded-lg" v-if="notes && notes.length">
          <div class="flex flex-row items-center justify-between w-full p-[0.5em] rounded-[4pt] transition-colors duration-200 hover:bg-[#F8F8F8]" v-for="(note, index) in notes" :key="`note ${index}`" :id="`person-note-${index}`">
            <p>
              <span class="font-weight-bold">{{ note.author }}</span> ({{ moment(note.date, "MMMM Do YYYY [at] LT") }}):
              {{ note.note }}
            </p>
            <div class="flex ml-[0.5em] w-auto">
              <b-btn
                :disabled="commonStore.keycloak.idTokenParsed.display_name !== note.author"
                @click="noteEditHandler(note)"
                size="sm"
                variant="primary"
              >
                <i class="fa fa-edit"></i>
                Edit
              </b-btn>
              <b-btn
                :disabled="!commonStore.userRoles.registry.admin && commonStore.keycloak.idTokenParsed.display_name !== note.author"
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
import { useCommonStore } from '@/stores/common'
import smoothScroll from 'smoothscroll'

import ApiService from '@/common/services/ApiService.js'
import { useRegistryStore } from '@/stores/registry.js'

export default {
  name: 'PersonNotes',
  data () {
    return {
      registryStore: useRegistryStore(),
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
    currentDriller () { return this.registryStore.currentDriller },
    notes () {
      if (this.currentDriller && this.currentDriller.notes) {
        return this.currentDriller.notes
      }
      return []
    },
    invalidNewNoteLength () { return this.noteInput.length > this.maxNoteLength },
    invalidEditNoteLength () { return this.noteContentEdit.length > this.maxNoteLength },
    commonStore () { return useCommonStore() }
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
.buttons button:last-child {
  margin-left: 0.5em;
}
.error {
  color: red;
}
.text-count {
  width: 100%;
  text-align: right;
  padding: 0.5em 1em 0 0;
}
</style>
