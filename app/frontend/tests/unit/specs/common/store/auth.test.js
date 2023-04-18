import auth from '@/common/store/auth.js'

describe('auth', () => {
  it('If user has role registries_viewer, then registry.view === true', () => {
    const state = { keycloak: { authenticated: true,
      idTokenParsed: {
        client_roles: ['registries_viewer']
      } } }
    expect(auth.getters.userRoles(state).registry.view).toBe(true)
  })
  it('If keycloak has role as wells_viewer, then wells.view === true', () => {
    const state = { keycloak: { authenticated: true,
      idTokenParsed: {
        client_roles: ['wells_viewer']
      } } }
    expect(auth.getters.userRoles(state).wells.view).toBe(true)
  })
  it('If keycloak has no roles, then wells.view === false', () => {
    const state = { keycloak: { authenticated: true,
      idTokenParsed: {
        client_roles: []
      } } }
    expect(auth.getters.userRoles(state).wells.view).toBe(false)
  })
  it('If keycloak has role as wells_edit, then wells.edit === true', () => {
    const state = { keycloak: { authenticated: true,
      idTokenParsed: {
        client_roles: ['wells_edit']
      } } }
    expect(auth.getters.userRoles(state).wells.edit).toBe(true)
  })
  it('If keycloak has role as wells_submission_viewer, then submissions.view === true', () => {
    const state = { keycloak: { authenticated: true,
      idTokenParsed: {
        client_roles: ['wells_submission_viewer']
      } } }
    expect(auth.getters.userRoles(state).submissions.view).toBe(true)
  })
  it('If keycloak has role as wells_submission, then submissions.edit === true', () => {
    const state = { keycloak: { authenticated: true,
      idTokenParsed: {
        client_roles: ['wells_submission']
      } } }
    expect(auth.getters.userRoles(state).submissions.edit).toBe(true)
  })
})
