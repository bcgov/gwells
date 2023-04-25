export const SET_KEYCLOAK = 'SET_KEYCLOAK'

const auth = {
  state: {
    keycloak: null
  },
  mutations: {
    [SET_KEYCLOAK] (state, payload) {
      state.keycloak = payload
    }
  },
  getters: {
    keycloak (state) {
      return state.keycloak
    },
    userRoles (state) {
      if (state.keycloak && state.keycloak.authenticated) {
        // map SSO roles to web app permissions
        // IMPORTANT: One should be relying on SSO groups to assign the appropriate roles.
        // e.g. We don't need to understand what a Statutory Authority is here, we should
        // only be concerned if the right to edit/approve is set. It's up to keycloak to associate some
        // group called Statutory Authority with the edit/approve roles.
        return {
          registry: {
            view: state.keycloak.hasRealmRole('registries_viewer'),
            edit: state.keycloak.hasRealmRole('registries_edit'),
            approve: state.keycloak.hasRealmRole('registries_approve')
          },
          wells: {
            view: state.keycloak.hasRealmRole('wells_viewer'),
            edit: state.keycloak.hasRealmRole('wells_edit'),
            approve: state.keycloak.hasRealmRole('wells_approve')
          },
          submissions: {
            view: state.keycloak.hasRealmRole('wells_submission_viewer'),
            edit: state.keycloak.hasRealmRole('wells_submission'),
            approve: state.keycloak.hasRealmRole('wells_approve')
          },
          aquifers: {
            edit: state.keycloak.hasRealmRole('aquifers_edit')
          },
          surveys: {
            edit: state.keycloak.hasRealmRole('surveys_edit')
          },
          bulk: {
            wellAquiferCorrelation: state.keycloak.hasRealmRole('bulk_well_aquifer_correlation_upload'),
            wellDocuments: state.keycloak.hasRealmRole('bulk_well_documents_upload'),
            aquiferDocuments: state.keycloak.hasRealmRole('bulk_aquifer_documents_upload'),
            verticalAquiferExtents: state.keycloak.hasRealmRole('bulk_vertical_aquifer_extents_upload')
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
  }
}

export default auth
