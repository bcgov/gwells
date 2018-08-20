export const SET_KEYCLOAK = 'SET_KEYCLOAK'

const auth = {
  state: {
    keycloak: {}
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
            view: state.keycloak.hasRealmRole('wells_viewer'),
            edit: state.keycloak.hasRealmRole('wells_edit'),
            approve: state.keycloak.hasRealmRole('wells_approve')
          }
        }
      } else {
        return {
          registry: {},
          wells: {},
          submissions: {}
        }
      }
    }
  }
}

export default auth
