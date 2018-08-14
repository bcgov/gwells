import auth from '@/common/store/auth.js'

describe('auth', () => {
  it('If keycloak has role as wells_viewer, then wells.view === true', () => {
    const state = { keycloak: { authenticated: true,
      hasRealmRole (key) {
        return key === 'wells_viewer'
      } } }
    expect(auth.getters.userRoles(state).wells.view).toBe(true)
  })
  it('If keycloak has no roles, then wells.view === false', () => {
    const state = { keycloak: { authenticated: true,
      hasRealmRole (key) {
        return false
      } } }
    expect(auth.getters.userRoles(state).wells.view).toBe(false)
  })
})
