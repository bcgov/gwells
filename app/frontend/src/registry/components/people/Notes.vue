<template>
  <div class="card" ref="noteSection">
    <div class="card-body">
      <h6 class="text-xl font-bold mb-4" id="notesSectionTitle">Notes</h6>

      <!-- Add Note Form -->
      <div class="mt-3" v-if="commonStore.userRoles.registry.edit">
        <Form @submit.prevent="noteSubmitHandler" @reset.prevent="noteCancelHandler">
          <div class="flex flex-col gap-2 mb-3">
            <label for="noteInput">Add a note:</label>
            <Textarea
              id="noteInput"
              v-model="noteInput"
              :disabled="submitLoading"
              :rows="3"
              :max-rows="6"
              class="w-full"
            />
            <div class="flex justify-between items-center mt-1">
              <div class="flex gap-2">
              <Button
                type="submit"
                label="Save"
                :disabled="!noteInput || submitLoading || invalidNewNoteLength"
                ref="noteInputSaveBtn"
              />
                <Button
                  type="reset"
                  label="Cancel"
                  severity="secondary"
                  size="small"
                  outlined
                  :disabled="!noteInput"
                />
              </div>
              <p class="text-sm font-bold" :class="[invalidNewNoteLength ? 'error': '']">
                {{ noteInput.length }}/{{ maxNoteLength }}
              </p>
            </div>
          </div>

          <Message v-if="submitSuccess" severity="success" class="mt-3" :closable="true" @close="submitSuccess = false">
            {{ alertText }}
          </Message>
          <!-- Submit Modal -->
          <Dialog
            v-model="confirmSubmitModal"
            v-model:visible="visible"
            centered
            modal
            header="Confirm save"
            @shown="focusSubmitModal"
            :return-focus="$refs.noteInputSaveBtn"
          >
            Are you sure you want to save this note?
            <div slot="modal-footer" class="buttons">
              <Button variant="primary" @click="confirmSubmitModal=false;noteSubmit()" ref="confirmSubmitConfirmBtn">
                Save
              </Button>
              <Button variant="light" @click="confirmSubmitModal=false">
                Cancel
              </Button>
            </div>
          </Dialog>
          <!-- Cancellation Modal -->
          <Dialog
              v-model="confirmCancelModal"
              v-model:visible="visible"
              centered
              modal
              header="Confirm cancel"
              @shown="focusCancelModal"
              :return-focus="$refs.noteInputCancelBtn"
            >
            Your note is not saved. Are you sure you want to discard your changes?
            <div slot="modal-footer" class="buttons">
              <Button severity="secondary" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn">
                Cancel
              </Button>
              <Button severity="danger" @click="confirmCancelModal=false;noteReset()">
                Discard
              </Button>
            </div>
          </Dialog>
          <!-- Delete Note Modal  -->
          <Dialog
            v-model="confirmDeleteModal"
            v-model:visible="visible"
            centered
            modal
            header="Confirm Deletion"
            @shown="focusDeleteModal"
            :return-focus="$refs.noteInputCancelBtn"
          >
            <p>Are you sure you want to delete this note?</p>
            <div v-if="activeNote" class="">
              <p class="font-weight-bold wb">"{{activeNote.note}}"</p>
            </div>
            <div slot="modal-footer" class="buttons">
              <Button
                variant="light"
                @click="confirmDeleteModal=false"
                ref="cancelDeleteBtn"
              >
                Cancel
              </Button>
              <Button
                severity="danger"
                @click="confirmDeleteModal=false;deleteNote()"
              >
                Delete
              </Button>
            </div>
          </Dialog>
          <!-- Edit Modal -->
          <Dialog
              v-model="confirmEditNoteModal"
              v-model:visible="visible"
              centered
              modal
              header="Editing Note"
              @shown="focusEditNoteModal"
              :return-focus="$refs.noteInputCancelBtn"
            >
            <div>
              <InputText
                id="editNoteTextArea"
                v-model="noteContentEdit"
                placeholder="Edit Note..."
                rows="4"
                max-rows="6"
              />
              <p
              class="font-weight-bold text-count"
              :class="[invalidEditNoteLength ? 'error': '']"
            >
              {{ noteContentEdit.length }}/{{ maxNoteLength }}
            </p>
            </div>
            <div slot="modal-footer" class="buttons">
              <Button variant="light" @click="confirmEditNoteModal=false" ref="cancelEditNoteCancelBtn">
                Cancel
              </Button>
              <Button variant="primary" :disabled="invalidEditNoteLength || !noteContentEdit" @click="notePatchHandle()">
                Submit
              </Button>
            </div>
          </Dialog>
        </Form>
      </div>

      <!-- Notes List -->
      <div id="notesList" class="mt-6 border-t border-surface-200 pt-4">
        <div v-if="!notes || !notes.length" class="text-surface-500">
          No notes for this record.
        </div>
        <div v-else class="flex flex-col gap-4">
          <div
            v-for="(note, index) in notes"
            :key="index"
            class="p-4 bg-surface-50 rounded-md border border-surface-100 flex flex-col sm:flex-row justify-between gap-4"
          >
            <div class="break-words max-w-full">
              <p class="mb-1">
                <span class="font-bold text-primary">{{ note.author }}</span>
                <span class="text-surface-500 text-sm ml-1">({{ note.date }})</span>:
              </p>
              <p>{{ note.note }}</p>
            </div>

            <div class="flex items-start gap-2 shrink-0">
              <!-- Kept FontAwesome icons inside PrimeVue buttons -->
              <Button
                @click="noteEditHandler(note)"
                size="small"
                outlined
                :disabled="commonStore.keycloak.idTokenParsed.display_name !== note.author"
              >
                <i class="fa fa-edit mr-2"></i> Edit
              </Button>
              <Button
                @click="noteDeleteHandler(note)"
                size="small"
                severity="danger"
                outlined
                :disabled="!commonStore.userRoles.registry.admin && commonStore.keycloak.idTokenParsed.display_name !== note.author"
              >
                <i class="fa fa-times"></i>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import smoothScroll from 'smoothscroll'
import { useCommonStore } from '@/stores/common.js'
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'Notes',

  /**
   * This component accepts props:
   * type (string): the type of resource (person or organization)
   * guid (uuid string): the individual person or company record guid to attach notes to
   * record (object): the person or company's object (with a 'notes' property as an array of notes)
   */
  props: ['type', 'guid', 'record'],

  data () {
    return {
      noteInput: '',
      alertText: '',
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
      if (this.record && this.record.notes) {
        return this.record.notes
      }
      return []
    },
    invalidNewNoteLength () { return this.noteInput.length > this.maxNoteLength },
    invalidEditNoteLength () { return this.noteContentEdit.length > this.maxNoteLength },
    resourceType () {
      // map 'resource' names (e.g. organization, person) to API friendly plural versions
      // - this is also the list of resources that currently accept notes
      const typeMap = {
        organization: 'organizations',
        person: 'people'
      }
      return typeMap[this.type]
    },
    commonStore () { return useCommonStore() },
  },
  methods: {
    deleteNote () {
      ApiService.delete(`${this.resourceType}/${this.guid}/notes`, this.activeNote.org_note_guid)
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
    noteSubmit () {
      // submit the note as a post request, triggered after confirming via popup
      this.submitSuccess = false
      this.submitError = false
      this.submitLoading = true
      ApiService.post(`${this.resourceType}/${this.guid}/notes`, { note: this.noteInput })
        .then(() => {
          const notes = this.$refs.noteSection
          // Note submitted, set loading/success indicators and scroll down to the new note
          this.noteReset()
          this.alertText = 'Note added.'
          this.submitLoading = false
          this.submitSuccess = true
          smoothScroll(notes, 1000)
          this.$emit('updated')
        }).catch((e) => {
          this.errorHandler(e)
        })
    },
    notePatchHandle () {
      const updatedNote = `(Edited ${new Date().toLocaleString()}) ` + this.noteContentEdit

      ApiService.patch(`${this.resourceType}/${this.guid}/notes`, this.activeNote.org_note_guid, { note: updatedNote })
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
    noteDeleteHandler (note) {
      this.activeNote = note
      this.confirmDeleteModal = true
    },
    noteCancelDeleteHandler () {
      this.activeNote = null
    },
    /**
     * @desc Handler for note editing, prepends an Edited field to mark the content as changed
     * @param {Object} note Note currently being edited
     */
    noteEditHandler (note) {
      const editRegexChromium = /^\(Edited \d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2}:\d{2} (AM|PM)\)\s/
      const editRegexFirefox = /^\(Edited \d{4}-\d{1,2}-\d{1,2}, \d{1,2}:\d{2}:\d{2} (a.m.|p.m.)\)\s/
      this.noteContentEdit = note.note.replace(editRegexChromium, '')
      this.noteContentEdit = this.noteContentEdit.replace(editRegexFirefox, '')
      this.activeNote = note
      this.confirmEditNoteModal = true
    },
    noteCancelHandler () {
      // trigger popup to confirm discard note
      this.confirmCancelModal = true
    },
    focusCancelModal () {
      // focus the "cancel" button in the confirm discard popup
      this.$refs.cancelSubmitCancelBtn.focus()
    },
    focusDeleteModal () {
      this.$refs.cancelDeleteBtn.focus()
    },
    focusSubmitModal () {
      // focus the "submit" button in the confirm save note popup
      this.$refs.confirmSubmitConfirmBtn.focus()
    },
    focusEditNoteModal () {
      this.$refs.cancelEditNoteCancelBtn.focus()
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
</style>
