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
import { defineStore } from 'pinia'
import ApiService from '@/common/services/ApiService.js'

export const useCommonStore = defineStore('common', {
  state: () => ({
    // was common/auth.js
    keycloak: null,

    // was common/config.js
    config: null,

    // was common/documents.js
    isPrivate: false,
    uploadFiles: [],
    filesUploading: false,
    fileUploadErrors: [],
    fileUploadError: false,
    fileUploadSuccess: false,
    shapefileUploading: false,
    shapefileUploadMessage: '',
    shapefileUploadSuccess: false,
    shapefile: null
  }),

  getters: {
    // ---- Auth ----
    userRoles (state) {
      if (state.keycloak && state.keycloak.authenticated) {
        // map SSO roles to web app permissions
        // IMPORTANT: One should be relying on SSO composite roles (which can be found alongside all of the
        // granular roles on Common Hosted SSO) to assign the appropriate roles.
        // e.g. We don't need to understand what a Statutory Authority is here, we should
        // only be concerned if the right to edit/approve is set. It's up to keycloak to associate some
        // group called Statutory Authority with the edit/approve roles.

        // NOTE: keycloak.js comes with hasResourceRole(role, resource) for checking if the user has a
        // particular role, but it doesn't seem to look at the correct JWT so using it will return false
        // even if the user does have that role.
        // Instead, we have to look at the "raw" list of roles contained inside the keycloak instance.
        const clientRoles = state.keycloak.idTokenParsed['client_roles']
        return {
          registry: {
            view: clientRoles.includes('registries_viewer'),
            edit: clientRoles.includes('registries_edit'),
            approve: clientRoles.includes('registries_approve'),
            admin: clientRoles.includes('gwells_admin') || clientRoles.includes('admin') // Prod v. Dev
          },
          wells: {
            view: clientRoles.includes('wells_viewer'),
            edit: clientRoles.includes('wells_edit'),
            approve: clientRoles.includes('wells_approve')
          },
          submissions: {
            view: clientRoles.includes('wells_submission_viewer'),
            edit: clientRoles.includes('wells_submission'),
            approve: clientRoles.includes('wells_approve')
          },
          aquifers: {
            edit: clientRoles.includes('aquifers_edit')
          },
          surveys: {
            edit: clientRoles.includes('surveys_edit')
          },
          bulk: {
            wellAquiferCorrelation: clientRoles.includes('bulk_well_aquifer_correlation_upload'),
            wellDocuments: clientRoles.includes('bulk_well_documents_upload'),
            aquiferDocuments: clientRoles.includes('bulk_aquifer_documents_upload'),
            verticalAquiferExtents: clientRoles.includes('bulk_vertical_aquifer_extents_upload')
          }
        }
      } else {
        return {
          registry: {},
          wells: {},
          submissions: {},
          aquifers: {},
          surveys: {},
          bulk: {}
        }
      }
    },
    authenticated (state) {
      return Boolean(state.keycloak && state.keycloak.authenticated)
    }
  },

  actions: {
    // ---- Auth ----
    setKeycloak (payload) {
      this.keycloak = payload
    },

    // ---- Config ----
    fetchConfig (params) {
      // We only fetch config if we don't have a copy cached
      if (this.config === null) {
        return new Promise((resolve, reject) => {
          ApiService.query('config', params)
            .then((response) => {
              this.setConfig(response.data)
            })
            .catch((error) => {
              reject(error)
            })
        })
      }
    },
    setConfig (payload) {
      this.config = payload
    },

    // ---- Documents ----
    uploadShapefile (payload) {
      const file = this.shapefile
      let formData = new FormData()
      formData.append('geometry', file)
      const url = `${payload.documentType}/${payload.recordId}/geometry`
      this.shapefileUploading = true
      return ApiService.post(url, formData)
        .then(() => {
          this.shapefileUploadSuccess = true
          this.shapefileUploadMessage = ''
        })
        .catch(e => {
          this.shapefileUploading = false
          this.shapefileUploadSuccess = false
          console.error('failed to save shapefile', e.response)
          this.shapefileUploadMessage = e.response.data.message || 'Server Error'
          throw e
        })
    },
    uploadTheFiles (payload) {
      this.filesUploading = true
      let documentType = payload.documentType
      let recordId = payload.recordId
      const files = payload.files || this.uploadFiles
      const fileNames = payload.fileNames || []

      // Driller documents are always private
      let isPrivate = this.isPrivate
      if (documentType === 'drillers') {
        isPrivate = true
      }

      return files.reduce((previousPromise, file, i) => {
        return previousPromise.then((results) => {
          // use override file name if it exists
          let fileName
          if (file.file) {
            fileName = file.file.name
            isPrivate = file.private
            file = file.file
          } else {
            fileName = fileNames[i] || file.name
          }
          return ApiService.presignedPutUrl(
            documentType,
            recordId,
            encodeURIComponent(fileName),
            isPrivate
          )
            .then(response => {
              let url = response.data.url
              let objectName = response.data.object_name

              let options = {
                headers: {
                  'Content-Type': file.type
                }
              }

              return ApiService.fileUpload(url, file, options)
                .then(() => {
                  console.log('successfully added file: ' + objectName)
                  if (documentType === 'wells') {
                    const fileNameSplit = objectName.split('_')
                    const fileDocumentType = fileNameSplit.length > 2 ? `${fileNameSplit[0]}_${fileNameSplit[1]}` : fileNameSplit[0]
                    ApiService.incrementFileCount(`wells/${recordId}`, fileDocumentType)
                  }
                })
                .catch(error => {
                  console.log(error)
                  this.addError(error)
                  return Promise.reject(error)
                })
            })
            .catch(error => {
              console.log(error)
              this.addError(error)
            })
        })
      }, Promise.resolve())
    },
    fileUploadSucceeded () {
      this.filesUploading = false
      this.fileUploadSuccess = true
      this.uploadFiles = []
      this.isPrivate = false
      setTimeout(() => {
        this.fileUploadSuccess = false
      }, 5000)
    },
    fileUploadFail () {
      this.filesUploading = true
      this.fileUploadSuccess = false
      this.uploadFiles = []
      this.isPrivate = false
    },
    resetUploadFiles () {
      this.uploadFiles = []
    },
    clearUploadShapeFileMessage () {
      this.shapefileUploadMessage = ''
    },
    clearUploadFilesMessage () {
      this.clearErrors()
    },
    addError (payload) {
      this.fileUploadErrors.push(payload)
    },
    clearErrors () {
      this.fileUploadErrors = []
      this.fileUploadError = false
    },
    setShapefileUploadMessage (payload) {
      this.shapefileUploadMessage = payload
    },
    setFilesUploading (payload) {
      this.filesUploading = payload
    },
    setShapefileUploading (payload) {
      this.shapefileUploading = payload
    },
    setFileUploadError (payload) {
      this.fileUploadError = payload
    },
    setFileUploadSuccess (payload) {
      this.fileUploadSuccess = payload
    },
    setShapefileUploadSuccess (payload) {
      this.shapefileUploading = false
      this.shapefileUploadSuccess = payload
    },
    setFiles (payload) {
      if (payload.length > 0) {
        this.uploadFiles.push(...payload)
      } else {
        this.uploadFiles = payload
      }
    },
    setShapefile (payload) {
      this.shapefile = payload
    },
    removeFile (file) {
      this.uploadFiles = this.uploadFiles.filter(item => item !== file)
    },
    setPrivate (payload) {
      this.isPrivate = payload
    }
  }
})

export default useCommonStore
