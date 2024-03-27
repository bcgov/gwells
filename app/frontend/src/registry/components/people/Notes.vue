<template>
  <div class="card" ref="noteSection">
    <div class="card-body p-2 p-md-3">
      <h6 class="card-title" id="notesSectionTitle">Notes</h6>
      <div class="mt-3" v-if="userRoles.registry.edit">
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
            @dismissed="submitSuccess=false"
          >
            {{ alertText }}
          </b-alert>
          <b-modal
              v-model="confirmSubmitModal"
              centered
              title="Confirm save"
              @shown="focusSubmitModal"
              :return-focus="$refs.noteInputSaveBtn"
            >
              Are you sure you want to save this note?
            <div slot="modal-footer" class="buttons">
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
              :return-focus="$refs.noteInputCancelBtn"
            >
            Your note is not saved. Are you sure you want to discard your changes?
            <div slot="modal-footer" class="buttons">
              <b-btn variant="secondary" @click="confirmCancelModal=false" ref="cancelSubmitCancelBtn">
                Cancel
              </b-btn>
              <b-btn variant="danger" @click="confirmCancelModal=false;noteReset()">
                Discard
              </b-btn>
            </div>
          </b-modal>
          <b-modal
              v-model="confirmDeleteModal"
              centered
              title="Confirm Deletion"
              @shown="focusDeleteModal"
              :return-focus="$refs.noteInputCancelBtn">
              <p>Are you sure you want to delete this note?</p>
              <div v-if="activeNote" >
                <p class="font-weight-bold">"{{activeNote.note}}"</p>
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
            </div>
            <div slot="modal-footer" class="buttons">
              <b-btn variant="light" @click="confirmEditNoteModal=false" ref="cancelEditNoteCancelBtn">
                Cancel
              </b-btn>
              <b-btn variant="primary" @click="notePatchHandle()">
                Submit
              </b-btn>
            </div>
          </b-modal>
        </b-form>
      </div>
      <div id="notesList" ref="notes">
        <div class="mt-5" v-if="!notes || !notes.length">
          <b-row><b-col>No notes for this record.</b-col></b-row>
        </div>
        <div class="mt-5 note-container" v-if="notes && notes.length">
          <div class="note" v-for="(note, index) in notes" :key="`note ${index}`" :id="`note-${index}`">
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
      noteContentEdit: "",
      activeNote: null
    }
  },
  computed: {
    notes () {
      if (this.record && this.record.notes) {
        return this.record.notes
      }
      return []
    },
    resourceType () {
      // map 'resource' names (e.g. organization, person) to API friendly plural versions
      // - this is also the list of resources that currently accept notes
      const typeMap = {
        organization: 'organizations',
        person: 'people'
      }
      return typeMap[this.type]
    },
    ...mapGetters(['userRoles', 'keycloak'])
  },
  methods: {
    deleteNote() {
      ApiService.delete(`${this.resourceType}/${this.guid}/notes`, this.activeNote.org_note_guid)
      .then(() => {
        this.activeNote = null;
        this.alertText = "Note deleted.";
        this.submitSuccess = true;
        this.$emit('updated');
      })
    },
    noteSubmit () {
      // submit the note as a post request, triggered after confirming via popup
      this.submitSuccess = false;
      this.submitError = false;
      this.submitLoading = true;
      ApiService.post(`${this.resourceType}/${this.guid}/notes`, { note: this.noteInput })
        .then(() => {
          const notes = this.$refs.noteSection;
          // Note submitted, set loading/success indicators and scroll down to the new note
          this.noteReset()
          this.alertText = "Note added.";
          this.submitLoading = false;
          this.submitSuccess = true;
          smoothScroll(notes, 1000);
          this.$emit('updated');;
        }).catch((e) => {
          this.submitLoading = false;
          this.submitError = e.response.data;
        })
    },
    notePatchHandle() {
      const updatedNote = `(Edited ${new Date().toLocaleString()}) ` + this.noteContentEdit;
      ApiService.patch(`${this.resourceType}/${this.guid}/notes`, this.activeNote.org_note_guid, {note: updatedNote})
        .then(() => {
          this.activeNote = null;
          this.noteContentEdit = null;
          this.confirmEditNoteModal = false;
          this.alertText = "Note updated."
          this.submitSuccess = true;
          this.$emit('updated');
        })

    },
    noteReset () {
      this.submitSuccess = false;
      this.submitError = false;
      this.submitLoading = false;
      this.noteInput = '';
    },
    noteSubmitHandler () {
      // trigger popup to confirm submit
      this.confirmSubmitModal = true
    },
    noteDeleteHandler (note) {
      this.activeNote = note;
      this.confirmDeleteModal = true;
    },
    noteCancelDeleteHandler () {
      this.activeNote = null;
    },
    /**
     * @desc Handler for note editing, prepends an Edited field to mark the content as changed
     * @param {Object} note Note currently being edited
     */
    noteEditHandler (note) {
      const editRegex = /^\(Edited \d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2}:\d{2} (AM|PM)\)\s/;
      this.noteContentEdit = note.note.replace(editRegex, "");
      this.activeNote = note;
      this.confirmEditNoteModal = true;
    },
    noteCancelHandler () {
      // trigger popup to confirm discard note
      this.confirmCancelModal = true;
    },
    focusCancelModal () {
      // focus the "cancel" button in the confirm discard popup
      this.$refs.cancelSubmitCancelBtn.focus();
    },
    focusDeleteModal () {
      this.$refs.cancelDeleteBtn.focus();
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
</style>
