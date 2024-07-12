import ApiService from '@/common/services/ApiService.js'

export const SET_CONFIG = 'SET_CONFIG'
export const FETCH_CONFIG = 'FETCH_CONFIG'

const config = {
  state: {
    config: null
  },
  mutations: {
    [SET_CONFIG] (state, payload) {
      state.config = payload
    }
  },
  getters: {
    config (state) {
      console.log("config: ", state)
      return state.config
    }
  },
  actions: {
    async [FETCH_CONFIG] ({ commit }, params) {
      // We only fetch config if we don't have a copy cached
      if (getters.config === null) {
        try {
            const response = await ApiService.query('config', params)
            console.log("config response", response)
            commit(SET_CONFIG, response.data)
        } catch (error) {
          console.log("Error: ", error)
        }
      }
    }
  }
}

export default config
