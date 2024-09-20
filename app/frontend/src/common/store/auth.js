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
  }
}

export default auth
