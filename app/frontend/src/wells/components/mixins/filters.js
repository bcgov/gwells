/* Shared logic for handling search filters. */
import { mapGetters } from 'vuex'
import { searchFields } from '@/wells/searchFields.js'

export default {
  data () {
    return {
      filterParams: {} // filterId: {param1: val, param2: val}
    }
  },
  computed: {
    ...mapGetters([
      'codes',
      'drillerNames',
      'organizationNames',
      'userRoles'
    ]),
    searchFields () {
      const fields = { ...searchFields }

      if (!(this.userRoles.wells && this.userRoles.wells.view)) {
        Object.entries(fields).forEach(([fieldId, field]) => {
          if (field.authenticated) {
            delete fields[fieldId]
          }
        })
      }

      return fields
    },
    landDistrictOptions () {
      if (this.codes.land_district_codes === undefined || (this.codes.land_district_codes && Object.entries(this.codes.land_district_codes).length === 0)) {
        return []
      }
      return this.codes.land_district_codes.map((district) => {
        return {
          value: district.land_district_code,
          text: `${district.land_district_code} - ${district.name}`
        }
      })
    },
    wellSubclassOptions () {
      if (!this.codes.well_classes) {
        return []
      }
      const options = []
      this.codes.well_classes.forEach((wellClass) => {
        wellClass.wellsubclasscode_set.forEach((wellSubclass) => {
          options.push({
            value: wellSubclass.well_subclass_guid,
            text: `${wellClass.description} - ${wellSubclass.description}`
          })
        })
      })

      return options
    },
    filterSelectOptions () {
      const options = {
        aquiferLithology: this.codes.aquifer_lithology_codes || [],
        coordinateAcquisitionCode: this.codes.coordinate_acquisition_codes || [],
        decommissionMethod: this.codes.decommission_methods || [],
        developmentMethods: this.codes.development_methods || [],
        drillingMethods: this.codes.drilling_methods || [],
        filterPackMaterial: this.codes.filter_pack_material || [],
        filterPackMaterialSize: this.codes.filter_pack_material_size || [],
        groundElevationMethod: this.codes.ground_elevation_methods || [],
        intendedWaterUse: this.codes.intended_water_uses || [],
        landDistrict: this.landDistrictOptions,
        licencedStatus: this.codes.licenced_status_codes || [],
        linerMaterial: this.codes.liner_material_codes || [],
        observationWellStatus: this.codes.observation_well_status || [],
        orgResponsible: this.organizationNames || [],
        ownerProvince: this.codes.province_codes || [],
        personResponsible: this.drillerNames || [],
        screenIntakeMethod: this.codes.screen_intake_methods || [],
        screenBottoms: this.codes.screen_bottoms || [],
        screenMaterial: this.codes.screen_materials || [],
        screenOpenings: this.codes.screen_openings || [],
        screenType: this.codes.screen_types || [],
        surfaceSealMaterial: this.codes.surface_seal_materials || [],
        surfaceSealMethod: this.codes.surface_seal_methods || [],
        waterQualityCharacteristics: this.codes.water_quality_characteristics || [],
        waterQualityColour: this.codes.water_quality_colours || [],
        wellClass: this.codes.well_classes || [],
        wellStatus: this.codes.well_status_codes || [],
        wellSubclass: this.wellSubclassOptions,
        yieldEstimationMethod: this.codes.yield_estimation_methods || []
      }

      Object.keys(options).forEach(optionId => {
        if (!this.searchFields.hasOwnProperty(optionId)) {
          delete options[optionId]
        }
      })

      return options
    },
    searchQueryParams () {
      const searchQueryParams = Object.entries(this.filterParams).reduce((allParams, [id, filterParams]) => {
        return Object.assign(allParams, filterParams)
      }, {})

      return searchQueryParams
    }
  },
  methods: {
    getParamNames ({ param, type }) {
      if (type === 'range') {
        return [`${param}_min`, `${param}_max`]
      } else if (type === 'dateRange') {
        return [`${param}_after`, `${param}_before`]
      } else if (type === 'booleanOrRange') {
        return [`${param}_min`, `${param}_max`, `${param}_has_value`]
      } else if (type === 'booleanOrText') {
        return [param, `${param}_has_value`]
      } else {
        return [param]
      }
    },
    getFilterFields (fieldIds) {
      return fieldIds.map(id => {
        const field = this.searchFields[id]
        const params = this.getParamNames(field)
        return { ...field, params: params, id: id }
      })
    }
  }
}
