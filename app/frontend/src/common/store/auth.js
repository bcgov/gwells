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
        return {
          registry: {
            // map SSO roles to web app permissions
            view: (state.keycloak.hasRealmRole('gwells_admin') ||
              state.keycloak.hasRealmRole('registries_statutory_authority') ||
              state.keycloak.hasRealmRole('registries_viewer') ||
              state.keycloak.hasRealmRole('registries_adjudicator')),
            edit: (state.keycloak.hasRealmRole('gwells_admin') ||
              state.keycloak.hasRealmRole('registries_statutory_authority') ||
              state.keycloak.hasRealmRole('registries_adjudicator')),
            approve: (state.keycloak.hasRealmRole('gwells_admin') ||
              state.keycloak.hasRealmRole('registries_statutory_authority'))
          },
          wells: {
            view: (!!state.keycloak.hasRealmRole('gwells_admin')),
            edit: (!!state.keycloak.hasRealmRole('gwells_admin')),
            approve: (!!state.keycloak.hasRealmRole('gwells_admin'))
          },
          submissions: {
            view: (!!state.keycloak.hasRealmRole('gwells_admin')),
            edit: (!!state.keycloak.hasRealmRole('gwells_admin')),
            approve: (!!state.keycloak.hasRealmRole('gwells_admin'))
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
