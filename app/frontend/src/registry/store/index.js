/**
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 */
import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/common/services/ApiService.js'
import {
  FETCH_CITY_LIST,
  FETCH_DRILLER,
  SEARCH,
  SEARCH_AGAIN,
  RESET_SEARCH,
  FETCH_DRILLER_OPTIONS,
  REQUEST_MAP_POSITION
} from './actions.types.js'
import {
  SET_ERROR,
  SET_LOADING,
  SET_LIST_ERROR,
  SET_USER,
  SET_CITY_LIST,
  SET_DRILLER,
  SET_SEARCH_RESPONSE,
  SET_DRILLER_OPTIONS,
  SET_LAST_SEARCHED_ACTIVITY,
  SET_HAS_SEARCHED,
  SET_SEARCH_PARAMS,
  SET_REQUESTED_MAP_POSITION  ,
  SET_CURRENT_MAP_BOUNDS,
  SET_DO_SEARCH_ON_BOUNDS_CHANGE,
  SET_LIMIT_SEARCH_TO_CURRENT_MAP_BOUNDS
} from './mutations.types.js'
import {
  DEFAULT_MAP_ZOOM,
  CENTRE_LNG_LAT_BC,
  convertLngLatBoundsToDirectionBounds
} from '../../common/mapbox/geometry'

//Vue.use(Vuex)

export const DEFAULT_SEARCH_PARAMS = {
  search: '',
  city: [''],
  activity: 'DRILL',
  status: 'A',
  limit: '10',
  ordering: ''
}

export const DEFAULT_MAP_POSITION = {
  centre: CENTRE_LNG_LAT_BC,
  zoom: DEFAULT_MAP_ZOOM
}

const registriesStore = {
  namespaced: true,
  state: {
    searchParams: Object.assign({}, DEFAULT_SEARCH_PARAMS),
    hasSearched: false,
    user: null,
    loading: false,
    error: null,
    listError: null,
    cityList: {},
    searchResponse: [],
    currentDriller: {},
    drillerOptions: null,
    lastSearchedActivity: 'DRILL',
    requestedMapPosition: null, 
    currentMapBounds: null,
    doSearchOnBoundsChange: false,

    //this is a dual-purpopse property: 
    // when false, the implied property 'snapMapToSearchResults' is true
    // and when true, the 'snapMapToSearchResults' is false
    limitSearchToCurrentMapBounds: false
  },
  mutations: {
    [SET_SEARCH_PARAMS](state, payload) {      
      const params = Object.assign({}, DEFAULT_SEARCH_PARAMS, payload)
      state.searchParams = payload
    },    
    [SET_HAS_SEARCHED] (state, payload) {
      state.hasSearched = payload
    },
    [SET_LOADING](state, payload) {
      state.loading = payload
    },
    [SET_ERROR] (state, payload) {
      state.error = payload
    },
    [SET_LIST_ERROR] (state, payload) {
      state.listError = payload
    },
    [SET_USER] (state, payload) {
      state.user = payload
    },
    [SET_CITY_LIST] (state, payload) {
      state.cityList = payload
    },
    [SET_DRILLER] (state, payload) {
      state.currentDriller = payload
    },
    [SET_SEARCH_RESPONSE] (state, payload) {
      state.searchResponse = payload
    },
    [SET_DRILLER_OPTIONS] (state, payload) {
      state.drillerOptions = payload
    },
    [SET_LAST_SEARCHED_ACTIVITY] (state, payload) {
      state.lastSearchedActivity = payload
    }, 
    [SET_REQUESTED_MAP_POSITION](state, payload) {  
      if (payload.hasOwnProperty("centre") && !payload.hasOwnProperty("zoom")) {
        payload.zoom = 10;
      }
      if (payload.hasOwnProperty("bounds") && !payload.hasOwnProperty("maxZoom")) {
        payload.maxZoom = 10;
      }
      if (payload && !payload.hasOwnProperty("centre") && !payload.hasOwnProperty("bounds")) {
        throw("Must specify either the 'centre' or the 'bounds' parameter")
      }
      state.requestedMapPosition = payload;
    },
    [SET_CURRENT_MAP_BOUNDS] (state, payload) {
      state.currentMapBounds = payload
    }, 
    [SET_DO_SEARCH_ON_BOUNDS_CHANGE] (state, payload) {
      state.doSearchOnBoundsChange = payload
    }, 
    [SET_LIMIT_SEARCH_TO_CURRENT_MAP_BOUNDS] (state, payload) {
      state.limitSearchToCurrentMapBounds = payload
    }, 
  },
  actions: {
    [RESET_SEARCH]({ commit, state }, options = {}) {
      const searchParams = Object.assign({}, state.searchParams)
      searchParams.search = DEFAULT_SEARCH_PARAMS.search
      searchParams.city = DEFAULT_SEARCH_PARAMS.city
      searchParams.status = DEFAULT_SEARCH_PARAMS.status
      searchParams.ordering = DEFAULT_SEARCH_PARAMS.ordering
      if (!options.keepSearchResults) {
        commit(SET_HAS_SEARCHED, false)
        commit(SET_SEARCH_RESPONSE, [])
      }
      if (!options.keepActivity) {
        searchParams.activity = DEFAULT_SEARCH_PARAMS.activity
      }
      if (!options.keepLimit) {
        searchParams.limit = DEFAULT_SEARCH_PARAMS.limit
      }
      commit(SET_SEARCH_PARAMS, searchParams)
      commit(SET_REQUESTED_MAP_POSITION, Object.assign({},DEFAULT_MAP_POSITION))
    },
    [FETCH_CITY_LIST]({ commit }, activity) {
      ApiService.query('cities/' + activity)
        .then((response) => {
          const list = Object.assign({}, this.state.cityList)
          const data = response.data
          const listByProvince = []

          /**
           * iterate through each item in the response data and filter cities into
           * an array of provinces. e.g.:
           *
           * listByProvince = [
           *   {
           *     prov: 'BC',
           *     cities: [
           *       'Duncan',
           *       'Victoria'
           *     ]
           *   },
           *   {
           *     prov: 'AB',
           *     cities: [
           *       'Jasper',
           *       'Hinton'
           *     ]
           *   }
           * ]
           *
           */
          data.forEach((item) => {
            // if a province doesn't exist in listByProvince, create a new item
            if (!listByProvince.some(prov => prov.prov === item.province_state)) {
              listByProvince.push({ prov: item.province_state, cities: [] })
            }
            listByProvince.find(prov => prov.prov === item.province_state).cities.push(item.city)
          })

          // set the list for the activity (driller or well installer) to the list of provinces/cities
          list[activity] = listByProvince
          commit(SET_CITY_LIST, list)
        })
        .catch((error) => {
          commit(SET_ERROR, error.response)
        })
    },
    [FETCH_DRILLER] ({commit}, guid) {
      commit(SET_LOADING, true)
      ApiService.get('drillers', guid)
        .then((response) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, null)
          commit(SET_DRILLER, response.data)
        })
        .catch((error) => {
          commit(SET_LOADING, false)
          commit(SET_ERROR, error.response)
        })
    },
    [SEARCH]({ commit, state }, params) {
      // Search using the given parameters

      // If the 'limitSearchToCurrentMapBounds' property is set, 
      // add additional parameters to the search
      // to restrict by the current map bounds
      if (state.limitSearchToCurrentMapBounds && state.currentMapBounds) {
        params = Object.assign({}, params, convertLngLatBoundsToDirectionBounds(state.currentMapBounds))
        params.srid = 4326
      }
      else {
        params = Object.assign({}, params, {sw_lat: null, sw_long: null, ne_lat: null, ne_long: null})
        params.srid = null
      }

      return new Promise((resolve, reject) => {
        commit(SET_SEARCH_PARAMS, params)
        commit(SET_HAS_SEARCHED, true)
        commit(SET_LOADING, true)
        ApiService.query('drillers', params)
          .then((response) => {            
            commit(SET_LOADING, false)
            commit(SET_LIST_ERROR, null)
            commit(SET_SEARCH_RESPONSE, response.data)
            resolve()
          })
          .catch((error) => {
            commit(SET_LOADING, false)
            commit(SET_LIST_ERROR, error.response)
            reject(error)
          })
      })
    },
    [SEARCH_AGAIN]({ dispatch, state }) {
      //repeat the last search using the saved
      //search params
      if (state.searchParams){
        dispatch(SEARCH, state.searchParams)
      }
    },
    [FETCH_DRILLER_OPTIONS] ({commit}, params) {
      // We only fetch driller options if we don't already have a copy cached
      if (!this.state.drillerOptions) {
        return new Promise((resolve, reject) => {
          commit(SET_LOADING, true)
          ApiService.query('drillers/options', params)
            .then((response) => {
              commit(SET_LOADING, false)
              commit(SET_DRILLER_OPTIONS, response.data)
            })
            .catch((error) => {
              commit(SET_LOADING, false)
              reject(error)
            })
        })
      }
    },
    /* param mapPosition  is an object of the form 
      {centre: ..., zoom: ... }, or
      {bounds: ...}
    */
    [REQUEST_MAP_POSITION]({ commit }, mapPosition) {        
      commit(SET_REQUESTED_MAP_POSITION, mapPosition) 
    }
  },
  getters: {
    loading(state) {
      return state.loading
    },
    hasSearched(state) {
      return state.hasSearched
    },
    searchParams(state) {
      return state.searchParams
    },
    error(state) {
      return state.error
    },
    listError (state) {
      return state.listError
    },
    user (state) {
      return state.user
    },
    cityList (state) {
      return state.cityList
    },
    searchResponse (state) {
      return state.searchResponse
    },
    currentDriller (state) {
      return state.currentDriller
    },
    drillerOptions (state) {
      return state.drillerOptions
    },
    requestedMapPosition(state) {
      return state.requestedMapPosition;
    },
    currentMapBounds(state) {
      return state.currentMapBounds;
    },
    doSearchOnBoundsChange(state) {
      return state.doSearchOnBoundsChange;
    },
    limitSearchToCurrentMapBounds(state) {
      return state.limitSearchToCurrentMapBounds;
    },
    snapMapToSearchResults(state) {
      return !state.limitSearchToCurrentMapBounds;
    },
    activity (state) {
      /**
       * last searched activity, exposed to components as "activity"
       */
      return state.lastSearchedActivity
    },
    provinceStateOptions (state) {
      const options = []
      if (state.drillerOptions && state.drillerOptions.province_state_codes) {
        state.drillerOptions.province_state_codes.forEach((item) => {
          options.push(item.province_state_code)
        })
      }
      return options
    }
  }
    
}

export default registriesStore
