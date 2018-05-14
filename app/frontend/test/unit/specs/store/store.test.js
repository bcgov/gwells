import { store } from '@/registry/store'
import {
  SET_ERROR,
  SET_LOADING,
  SET_LIST_ERROR,
  SET_USER,
  SET_CITY_LIST,
  SET_DRILLER,
  SET_DRILLER_LIST } from '@/registry/store/mutations.types.js'

describe('store', () => {
  beforeEach(() => {
    jest.resetAllMocks()
    jest.resetModules()
  })
  it('error mutation type commits error to state', () => {
    store.commit(SET_ERROR, 'whoa there!')
    expect(store.getters.error).toBe('whoa there!')
  })
  it('listError mutation type commits listError to state', () => {
    store.commit(SET_LIST_ERROR, 'list error')
    expect(store.getters.listError).toBe('list error')
  })
  it('loading mutation type commits loading=true to state', () => {
    store.commit(SET_LOADING, true)
    expect(store.getters.loading).toBe(true)
  })
  it('user mutation type commits user object to state', () => {
    store.commit(SET_USER, { username: 'Bob' })
    expect(store.getters.user.username).toBe('Bob')
  })
  it('cityList mutation type commits list of cities to state', () => {
    store.commit(SET_CITY_LIST, ['Anytown', 'Chicago', 'Smallville'])
    expect(store.getters.cityList.length).toBe(3)
  })
  it('drillerList mutation commits list of drillers to state', () => {
    store.commit(SET_DRILLER_LIST, [{ first_name: 'Bob', surname: 'Driller' }, { first_name: 'Billy', surname: 'Wells' }])
    expect(store.getters.drillers.length).toBe(2)
  })
  it('cityList mutation commits new driller object state', () => {
    store.commit(SET_DRILLER, { first_name: 'Bob', surname: 'Driller' })
    expect(store.getters.currentDriller.surname).toBe('Driller')
  })
})
