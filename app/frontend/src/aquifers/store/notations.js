/*
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
import axios from 'axios'
import { doPolygonsIntersect } from '../../common/mapbox/geometry'
import { SET_NATURAL_RESOURCE_REGIONS, SET_AQUIFER_NOTATIONS } from './mutations.types'

export default {
  namespaced: true,
  state: {
    naturalResourceRegions: [],
    aquiferNotations: [],
    aquiferNotationCodes: {
      'AR': 'Application Refused',
      'PWS': 'Possible Water Shortage',
      'FR': 'Fully Recorded',
      'FR-EXC': 'Fully Recorded Except',
      'OR': 'Office Reserve'
    }
  },
  mutations: {
    [SET_NATURAL_RESOURCE_REGIONS] (state, payload) {
      state.naturalResourceRegions = payload
    },
    [SET_AQUIFER_NOTATIONS] (state, payload) {
      state.aquiferNotations = payload
    }
  },
  actions: {
    fetchNotationsFromDataBC ({ commit, dispatch, state }) {
      if (state.naturalResourceRegions.length <= 0 ||
        state.aquiferNotationCodes.length <= 0) {
        dispatch('fetchNaturalResourceRegions')
        dispatch('fetchAquiferNotations')
      }
    },
    fetchNaturalResourceRegions ({ commit, state }) {
      const url = 'https://openmaps.gov.bc.ca/geo/pub/wfs?SERVICE=WFS&VERSION=2.0.0' +
        '&REQUEST=GetFeature&outputFormat=json&srsName=epsg:4326&typeNames=WHSE_ADMIN_BOUNDARIES.ADM_NR_REGIONS_SPG' +
        "&CQL_FILTER=REGION_NAME IN('South Coast Natural Resource Region','West Coast Natural Resource Region')"
      axios.get(url, { transformRequest: (data, headers) => {
        delete headers.common['Authorization']
        return data
      }
      }).then((response) => {
        const data = response.data
        if (data.features) {
          commit(SET_NATURAL_RESOURCE_REGIONS, data.features)
        }
      }).catch(error => console.log(error))
    },
    fetchAquiferNotations ({ commit, state }) {
      const url = 'https://openmaps.gov.bc.ca/geo/pub/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature' +
        '&outputFormat=json&srsName=epsg:4326&typeNames=WHSE_WATER_MANAGEMENT.WLS_WATER_NOTATION_AQUIFERS_SP' +
          '&propertyName=AQUIFER_ID,NOTATION_DESCRIPTION'
      axios.get(url, { transformRequest: (data, headers) => {
        delete headers.common['Authorization']
        return data
      }
      }).then((response) => {
        const data = response.data
        if (data.features) {
          commit(SET_AQUIFER_NOTATIONS, data.features)
        }
      }).catch(error => console.log(error))
    }
  },
  getters: {
    getAquiferNotationsById: (state, getters) => (id, geom) => {
      const aquiferNotations = state.aquiferNotations
        .filter(a => a.properties.AQUIFER_ID.toString() === id.toString())
      if (aquiferNotations) {
        const description = getters.getAquiferNotationDescription(aquiferNotations)
        if (description.includes('Possible Water Shortage')) {
          return getters.filterAquiferNotationsByRegion(description, geom)
        } else {
          return description
        }
      } else {
        return null
      }
    },
    getAquiferNotationDescription: (state) => (notations) => {
      let description = ''
      notations.forEach(notation => {
        for (const [key, value] of Object.entries(state.aquiferNotationCodes)) {
          if (notation.properties.NOTATION_DESCRIPTION.includes(key)) {
            description = description + value + ', '
          }
        }
      })
      description = description.replace(/,\s*$/, '')
      return description
    },
    filterAquiferNotationsByRegion: (state) => (description, geom) => {
      for (let feature of state.naturalResourceRegions) {
        const intersection = doPolygonsIntersect(feature, geom)
        if (intersection) {
          description = description.replace('Possible Water Shortage', 'Possible Water Shortage and/or Saline Intrusion Issues')
          break
        }
      }
      return description
    }
  }
}
