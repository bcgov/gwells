import authEntry from '@/registry/router/authEntry.js'

class LocalStorageMock {
  constructor () {
    this.store = {}
  }
  clear () {
    this.store = {
      token: 'token-123',
      tokenExpiry: '9520537238',
      username: 'user'
    }
  }
  getItem (key) {
    return this.store[key] || null
  }
  setItem (key, value) {
    this.store[key] = value
  }
  removeItem (key) {
    delete this.store[key]
  }
}
// make the localStorage mock available in node's global object
global.localStorage = new LocalStorageMock()

describe('authEntry.js', () => {
  beforeEach(() => {
    localStorage.clear()
  })
  it('allows user to continue even if no user/token found (does not block entry)', () => {
    const to = { name: 'FakeRouteName' }
    const from = { name: 'PageWeCameFrom' }
    const next = jest.fn()
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('tokenExpiry')
    authEntry(to, from, next)
    expect(next).toHaveBeenCalledWith()
  })
  it('continues to "next" when a token is found', () => {
    const to = { name: 'FakeRouteName' }
    const from = { name: 'PageWeCameFrom' }
    const next = jest.fn()
    authEntry(to, from, next)
    expect(next).toHaveBeenCalledWith()
  })
  it('removes token/user if token looks expired', () => {
    const to = { name: 'FakeRouteName' }
    const from = { name: 'PageWeCameFrom' }
    const next = jest.fn()
    localStorage.setItem('tokenExpiry', 111)
    authEntry(to, from, next)
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('username')
    expect(token).toEqual(null)
    expect(user).toEqual(null)
  })
})
