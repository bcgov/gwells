export default {
  namespaced: true,
  state: {
    demand_codes: [],
    known_water_use_codes: [],
    material_codes: [],
    productivity_codes: [],
    quality_concern_codes: [],
    subtype_codes: [],
    vulnerability_codes: []
  },
  mutations: {
    addCodes(state, payload) {
      state[payload.key] = payload.codeTable
    }
  }
}
