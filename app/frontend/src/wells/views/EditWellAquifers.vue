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

<template>
  <div class="edit-well-aquifers">
    <div v-if="loading">
      <div class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
    </div>
    <div v-else>
      <b-card no-body class="mb-3 container d-print-none">
        <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"/>
      </b-card>
      <b-card v-if="errorNotFound" class="container p-1">
        <h1>Not Found</h1>
        <p>The page you are looking for was not found.</p>
      </b-card>
      <b-card v-else class="container">
        <api-error v-if="error" :error="error"/>

        <b-alert variant="success" show v-if="showSavedMessage" id="aquifer-success-alert">
          Well {{wellTagNumber}} has had it's vertical aquifer extents updated
        </b-alert>

        <h2 id="page-title">Well {{wellTagNumber}} Vertical Aquifer Extents</h2>

        <b-alert v-if="warnings.length > 0" variant="warning" show id="warnings">
          Possible invalid data. Double check the warnings listed below before you save.
          <ul>
            <li v-for="(warning, index) in warnings" :key="index">{{warning}}</li>
          </ul>
        </b-alert>

        <b-form @submit.prevent="save" @reset.prevent="resetForm" :disabled="isSaving">
          <div>
            <div id="vertical-aquifer-extents-table">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th class="font-weight-normal pl-0 from-col">From ft (bgl)</th>
                    <th class="font-weight-normal to-col">To ft (bgl)</th>
                    <th class="font-weight-normal aquifer-col">Aquifer</th>
                    <th class="font-weight-normal latitude-col">Latitude</th>
                    <th class="font-weight-normal longitude-col pr-0">Longitude</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(aquifer, index) in aquifersData" :key="aquifer.id">
                    <td class="input-width-small py-0 pl-0">
                      <form-input
                        group-class="my-1"
                        :id="`aquiferDepthFrom_${index}`"
                        type="number"
                        aria-label="Depth from (feet)"
                        v-model="aquifer.start"
                        :errors="getRowError(index).start"
                        />
                    </td>
                    <td class="input-width-small py-0">
                      <form-input
                        group-class="my-1"
                        :id="`aquiferDepthTo_${index}`"
                        type="number"
                        aria-label="Depth to (feet)"
                        v-model="aquifer.end"
                        :errors="getRowError(index).end"
                        />
                    </td>
                    <td class="input-width-small py-0 pr-0">
                      <b-form-group
                        class="aquifer-search-dropdown"
                        :class="{'has-error': getRowError(index).aquifer_id}">
                        <v-select
                          v-model="aquifer.aquifer_id"
                          :id="`aquifer_${index}`"
                          :filterable="false"
                          :options="aquiferList || []"
                          :key="aquifer.aquifer_id"
                          :reduce="aquifer => aquifer.aquifer_id"
                          class="my-1"
                          label="description"
                          index="aquifer_id"
                          @search="onAquiferSearch">
                          <template slot="no-options">
                            Search for an aquifer by name or id number
                          </template>
                          <template slot="option" slot-scope="option">
                            <div>
                              {{ option.description }}
                            </div>
                          </template>
                          <template slot="selected-option" slot-scope="option">
                            <div>
                              {{ option.description }}
                            </div>
                          </template>
                        </v-select>
                        <b-form-invalid-feedback :id="`aquifer${index}InvalidFeedback`">
                          <div v-for="(error, errIndex) in getRowError(index).aquifer_id" :key="`aquifer${index}Input error ${errIndex}`">
                            {{ error }}
                          </div>
                        </b-form-invalid-feedback>
                      </b-form-group>
                    </td>
                    <td class="input-width-small py-0">
                      <form-input
                        group-class="my-1"
                        :id="`aquiferDepthLat_${index}`"
                        type="number"
                        aria-label="Latitude"
                        :step="0.00001"
                        v-model="aquifer.lat"
                        :errors="getRowError(index).lat"
                        />
                    </td>
                    <td class="input-width-small py-0">
                      <form-input
                        group-class="my-1"
                        :id="`aquiferDepthLng_${index}`"
                        type="number"
                        aria-label="Longitude"
                        :step="0.00001"
                        v-model="aquifer.lng"
                        :errors="getRowError(index).lng"
                        />
                    </td>
                    <td class="py-0 text-right">
                      <b-btn size="sm" variant="primary" @click="removeRowIfOk(index)" :id="`removeAquiferRowButton${index}`" class="mt-2" :disabled="isSaving"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <b-btn class="mt-2" size="sm" variant="primary" @click="addAquiferRow" id="addAquiferRowButton" :disabled="isSaving"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
          </div>
          <b-row class="mt-3">
            <b-col>
              <b-btn type="submit" variant="primary" class="mr-2" :disabled="isSaving">
                <i v-if="isSaving" class="fa fa-circle-o-notch fa-spin ml-1"/>
                Save
              </b-btn>
              <b-btn type="reset" variant="default" :disabled="isSaving">Reset</b-btn>
            </b-col>
          </b-row>
        </b-form>
        <b-modal
          v-model="confirmRemoveModal"
          centered
          title="Confirm remove"
          @shown="focusRemoveModal">
          Are you sure you want to remove this row?
          <div slot="modal-footer">
            <b-btn variant="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn">
              Cancel
            </b-btn>
            <b-btn variant="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)">
              Remove
            </b-btn>
          </div>
        </b-modal>
      </b-card>
    </div>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'
import { debounce, uniq } from 'lodash'
import ApiService from '@/common/services/ApiService.js'
import APIErrorMessage from '@/common/components/APIErrorMessage'

export default {
  components: {
    'api-error': APIErrorMessage
  },
  data () {
    return {
      loading: false,
      error: null,
      fieldErrors: [],
      confirmRemoveModal: false,
      rowIndexToRemove: null,
      aquifers: [],
      aquifersData: [],
      aquiferList: [],
      errorNotFound: false,
      showSavedMessage: false,
      isSaving: false
    }
  },
  computed: {
    ...mapGetters(['codes']),
    wellTagNumber () { return parseInt(this.$route.params.wellTagNumber) || null },
    breadcrumbs () {
      const breadcrumbs = [
        {
          text: 'Well Search',
          to: { name: 'wells-home' }
        },
        {
          text: `Well ${this.wellTagNumber} Summary`,
          to: { name: 'wells-detail', params: { id: this.wellTagNumber } }
        },
        {
          text: 'Edit Well',
          to: { name: 'SubmissionsEdit', params: { id: this.wellTagNumber } }
        },
        {
          text: this.errorNotFound ? 'Not found' : 'Edit Vertical Aquifer Extents',
          active: true
        }
      ]

      return breadcrumbs
    },
    filledInData () {
      return this.aquifersData.filter((row) => this.rowHasValues(row))
    },
    warnings () {
      const warnings = []

      const duplicatedAquiferIds = this.findDuplicatedAquiferIds()
      if (duplicatedAquiferIds.length > 0) {
        warnings.push(`Aquifer ${duplicatedAquiferIds.join(', ')} specified more then once.`)
      }

      const coordsNotSame = this.findCoordsNotSame()
      if (coordsNotSame.length > 0) {
        const firstCoord = [ this.filledInData[0].lat, this.filledInData[0].lng ]
        warnings.push(`Coordinates ${coordsNotSame.join(' and ')} are not the same as the first coordinate ${firstCoord.join(', ')}.`)
      }

      return warnings
    }
  },
  watch: {
    aquifers (aquifers) {
      this.initForm()
    }
  },
  methods: {
    addAquiferRow () {
      this.aquifersData.push(this.emptyObject())
    },
    emptyObject () {
      return {
        id: null,
        start: null,
        end: null,
        aquifer_id: null,
        lat: null,
        lng: null
      }
    },
    removeRowByIndex (index) {
      this.aquifersData.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.aquifersData[rowNumber])) {
        this.rowIndexToRemove = rowNumber
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(rowNumber)
      }
    },
    getRowError (index) {
      return this.fieldErrors[index] || {}
    },
    rowHasValues (row) {
      return !Object.values(row).every((x) => !x)
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    },
    aquiferSearch: debounce((loading, search, vm) => {
      if (!search) {
        loading(false)
        return
      }

      ApiService.query(`aquifers/names?search=${escape(search)}`).then((response) => {
        vm.aquiferList = response.data
        loading(false)
      }).catch(() => {
        loading(false)
      })
    }, 500),
    onAquiferSearch (search, loading) {
      loading(true)
      this.aquiferSearch(loading, search, this)
    },
    initForm () {
      // when component created, add an initial row of aquifers
      this.aquifersData = []

      if (!this.aquifers.length) {
        for (let i = 0; i < 3; i++) {
          this.addAquiferRow()
        }
      } else {
        this.aquifers.forEach((row) => {
          this.aquifersData.push({ ...row })
        })
        this.addAquiferRow()
      }
    },
    resetForm () {
      this.error = null
      this.fieldErrors = []
      this.aquifersData = []
      this.initForm()
    },
    save () {
      this.isSaving = true
      this.error = null
      this.fieldErrors = []
      this.showSavedMessage = false
      ApiService.post(`wells/${this.wellTagNumber}/vertical-aquifer-extents`, this.filledInData)
        .then((response) => {
          this.aquifers = response.data
          this.isSaving = false
          this.showSavedMessage = true
        })
        .catch((error) => {
          this.isSaving = false
          if (error.response.status === 400) {
            this.fieldErrors = error.response.data
          } else {
            this.error = error.response
          }
        })
    },
    fetchAquifersForWell () {
      this.loading = true
      return ApiService.query(`wells/${this.wellTagNumber}/vertical-aquifer-extents`)
        .then((response) => {
          this.loading = false
          this.aquifers = response.data
        }).catch((e) => {
          this.loading = false
          this.error = e.response
          if (this.error && this.error.status === 404) {
            this.errorNotFound = true
          }
        })
    },
    findDuplicatedAquiferIds () {
      const aquiferIds = this.filledInData.map((data) => data.aquifer_id).filter((x) => x !== null)
      return uniq(aquiferIds.filter((aquiferId) => {
        return aquiferIds.filter((aquiferId1) => {
          return aquiferId1 === aquiferId
        }).length > 1
      }))
    },
    findCoordsNotSame () {
      const coords = this.filledInData
        .map((data) => [data.lat, data.lng])
        .filter(([lat, lng]) => lat !== null && lng !== null)

      if (coords.length === 0) { return [] }

      const firstItem = coords[0]
      return coords.filter((data) => {
        return !this.checkCoordsAreTheSame(data, firstItem)
      })
    },
    checkCoordsAreTheSame (c1, c2) {
      const [lat1, lng1] = c1
      const [lat2, lng2] = c2
      const precision = 0.000001
      return Math.abs(lat1 - lat2) <= precision && Math.abs(lng1 - lng2) <= precision
    }
  },
  created () {
    if (this.wellTagNumber === null) {
      this.error = `Unable to load well '${this.wellTagNumber}'`
      return
    }

    this.fetchAquifersForWell()
  }
}
</script>

<style lang="scss">
.has-error {
  .v-select > .vs__dropdown-toggle {
    border-color: #dc3545;
  }

  .invalid-feedback {
    display: block !important;
  }
}

#vertical-aquifer-extents-table {
  overflow-x: auto;

  table {
    margin-bottom: 0;
  }

  .from-col, .to-col {
    min-width: 80px;
    width: 10%;
  }

  .aquifer-col {
    min-width: 200px;
    width: 50%;
  }

  .latitude-col, .longitude-col {
    min-width: 100px;
    width: 15%;
  }

  .aquifer-search-dropdown .vs__dropdown-toggle {
    padding-top: 2px;
    border-color: #ced4da
  }

  .form-group {
    margin-bottom: 0;
  }
}
</style>
