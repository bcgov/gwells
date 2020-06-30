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
  <div id="single-aquifer-map" class="map">
    <p id="unsupported-browser" v-if="browserUnsupported">Your browser is unable to view the map</p>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'
import { mapGetters } from 'vuex'

import {
  DATABC_ROADS_SOURCE,
  DATABC_CADASTREL_SOURCE,
  WELLS_SOURCE_ID,
  AQUIFERS_SOURCE_ID,
  DATABC_ROADS_SOURCE_ID,
  DATABC_CADASTREL_SOURCE_ID,
  DATABC_ROADS_LAYER,
  DATABC_CADASTREL_LAYER,
  DATABC_CADASTREL_LAYER_ID,
  wellsEmsLayer,
  wellsUncorrelatedLayer,
  wellsBaseAndArtesianLayer,
  aquifersLineLayer,
  aquifersFillLayer,
  setupAquiferHover,
  DATABC_ECOCAT_LAYER_ID,
  DATABC_SURFACE_WATER_LICENCES_LAYER_ID,
  DATABC_ECOCAT_SOURCE,
  DATABC_ECOCAT_SOURCE_ID,
  AQUIFERS_FILL_LAYER_ID,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  WELLS_EMS_LAYER_ID,
  WELLS_UNCORRELATED_LAYER_ID,
  aquiferLayerFilter,
  DATABC_GROUND_WATER_LICENCES_LAYER_ID,
  ecoCatLayer,
  surfaceWaterLicencesLayer,
  groundWaterLicencesLayer,
  DATABC_WATER_LICENCES_SOURCE_ID,
  DATABC_WATER_LICENCES_SOURCE,
  WELLS_SOURCE,
  AQUIFERS_SOURCE,
  observationWellsLayer,
  WELLS_OBSERVATION_LAYER_ID
} from '../../common/mapbox/layers'
import { computeBoundsFromMultiPolygon } from '../../common/mapbox/geometry'
import { LayersControl, LegendControl } from '../../common/mapbox/controls'
import { createAquiferPopupElement, createWellPopupElement, createEcocatPopupElement, createWaterLicencePopupElement } from '../popup'

import cadastralLegendSrc from '../../common/assets/images/cadastral.png'
import ecoCatWaterLegendSrc from '../../common/assets/images/ecocat-water.svg'
import surfaceWaterLicenceActiveLegendSrc from '../../common/assets/images/swater-licence-active.svg'
import groundWaterLicenceActiveLegendSrc from '../../common/assets/images/gwater-licence.svg'
import ecoCatGroundWaterLegendSrc from '../../common/assets/images/ecocat-groundwater.svg'
import observationWellInactiveLegendSrc from '../../common/assets/images/owells-inactive.svg'
import observationWellActiveLegendSrc from '../../common/assets/images/owells-active.svg'

import wellsAllLegendSrc from '../../common/assets/images/wells-all.svg'
import wellsArtesianLegendSrc from '../../common/assets/images/wells-artesian.svg'
import uncorrelatedWellsIconSrc from '../../common/assets/images/wells-uncorrelated.svg'
import emsWellsIconSrc from '../../common/assets/images/wells-ems.svg'
import { setupFeatureTooltips } from '../../common/mapbox/popup'

const CURRENT_AQUIFER_FILL_LAYER_ID = 'cur-aquifer-fill'
const CURRENT_AQUIFER_LINE_LAYER_ID = 'cur-aquifer-line'

export default {
  name: 'SingleAquiferMap',
  props: ['aquifer-id', 'geom'],
  data () {
    return {
      map: null,
      browserUnsupported: false,
      mapLayers: [
        {
          show: true,
          id: DATABC_CADASTREL_LAYER_ID,
          label: 'Cadastrals',
          imageSrc: cadastralLegendSrc
        },
        {
          show: false,
          id: DATABC_ECOCAT_LAYER_ID,
          label: 'EcoCat',
          legend: [
            {
              imageSrc: ecoCatGroundWaterLegendSrc,
              label: 'groundwater reports'
            },
            {
              imageSrc: ecoCatWaterLegendSrc,
              label: 'water related reports'
            }
          ]
        },
        {
          show: false,
          id: DATABC_SURFACE_WATER_LICENCES_LAYER_ID,
          label: 'Surface water licences',
          imageSrc: surfaceWaterLicenceActiveLegendSrc
        },
        {
          show: false,
          id: DATABC_GROUND_WATER_LICENCES_LAYER_ID,
          label: 'Groundwater licences',
          imageSrc: groundWaterLicenceActiveLegendSrc
        },
        {
          show: true,
          id: WELLS_BASE_AND_ARTESIAN_LAYER_ID,
          label: 'Wells',
          legend: [
            {
              imageSrc: wellsAllLegendSrc,
              label: 'all'
            },
            {
              imageSrc: wellsArtesianLegendSrc,
              label: 'artesian'
            }
          ]
        },
        {
          show: false,
          id: WELLS_OBSERVATION_LAYER_ID,
          label: 'Observation wells',
          legend: [
            {
              imageSrc: observationWellActiveLegendSrc,
              label: 'active'
            },
            {
              imageSrc: observationWellInactiveLegendSrc,
              label: 'inactive'
            }
          ]
        },
        {
          show: false,
          id: WELLS_EMS_LAYER_ID,
          label: 'EMS wells',
          imageSrc: emsWellsIconSrc
        },
        {
          show: false,
          id: WELLS_UNCORRELATED_LAYER_ID,
          label: 'Uncorrelated wells',
          imageSrc: uncorrelatedWellsIconSrc
        }
      ],
      jumpToAquifer: true
    }
  },
  mounted () {
    this.$emit('mapLoading')

    this.initMapBox()
  },
  destroyed () {
    this.map.remove()
    this.map = null
  },
  computed: {
    ...mapGetters(['userRoles']),
    showUnpublished () {
      return Boolean(this.userRoles.aquifers.edit)
    }
  },
  methods: {
    initMapBox () {
      if (!mapboxgl.supported()) {
        this.browserUnsupported = true
        return
      }

      var mapConfig = {
        container: this.$el,
        zoom: 4,
        minZoom: 4,
        maxPitch: 0,
        dragRotate: false,
        center: [-126.5, 54.5],
        style: this.buildMapStyle()
      }

      this.map = new mapboxgl.Map(mapConfig)
      new GestureHandling({ modifierKey: 'ctrl' }).addTo(this.map)

      /* Add controls */

      this.map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-left')
      this.map.addControl(new mapboxgl.ScaleControl({
        maxWidth: 80,
        unit: 'imperial'
      }))
      this.map.addControl(new mapboxgl.ScaleControl({
        maxWidth: 80,
        unit: 'metric'
      }))
      this.map.addControl(new mapboxgl.AttributionControl({
        customAttribution: 'MapBox | Government of British Columbia, DataBC, GeoBC '
      }))
      this.map.addControl(new LayersControl({
        layers: this.mapLayers,
        onChange: this.layersChanged
      }))
      this.legendControl = new LegendControl({
        layers: this.mapLayers
      })
      this.map.addControl(this.legendControl, 'bottom-right')

      this.map.on('load', () => {
        /* Setup tooltips  */
        const tooltipLayers = {
          [AQUIFERS_FILL_LAYER_ID]: {
            createTooltipContent: this.createAquiferPopupElement
          },
          [CURRENT_AQUIFER_FILL_LAYER_ID]: {
            createTooltipContent: this.createAquiferPopupElement
          },
          [DATABC_ECOCAT_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createEcocatPopupElement
          },
          [DATABC_SURFACE_WATER_LICENCES_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createSurfaceWaterLicencePopupElement
          },
          [DATABC_GROUND_WATER_LICENCES_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createGroundWaterLicencePopupElement
          },
          [WELLS_OBSERVATION_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          },
          [WELLS_BASE_AND_ARTESIAN_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          },
          [WELLS_EMS_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          },
          [WELLS_UNCORRELATED_LAYER_ID]: {
            snapToCenter: true,
            createTooltipContent: this.createWellPopupElement
          }
        }
        setupFeatureTooltips(this.map, tooltipLayers)

        /* Setup aquifer hover effect */

        setupAquiferHover(this.map, AQUIFERS_FILL_LAYER_ID)
        setupAquiferHover(this.map, CURRENT_AQUIFER_FILL_LAYER_ID)

        /* Goto Aquifer */

        this.setSelectedAquifer(this.aquiferId, true)

        // On map load jump to the aquifer (if there is geom) by setting the `fitBounds()` duration
        // option to zero/
        this.zoomToAquifer({ duration: 0 })

        this.$emit('mapLoaded')
      })
    },
    buildMapStyle () {
      return {
        version: 8,
        sources: {
          [DATABC_ROADS_SOURCE_ID]: DATABC_ROADS_SOURCE,
          [DATABC_CADASTREL_SOURCE_ID]: DATABC_CADASTREL_SOURCE,
          [DATABC_ECOCAT_SOURCE_ID]: DATABC_ECOCAT_SOURCE,
          [DATABC_WATER_LICENCES_SOURCE_ID]: DATABC_WATER_LICENCES_SOURCE,
          [WELLS_SOURCE_ID]: WELLS_SOURCE,
          [AQUIFERS_SOURCE_ID]: AQUIFERS_SOURCE
        },
        layers: [
          DATABC_ROADS_LAYER,
          DATABC_CADASTREL_LAYER,
          aquifersFillLayer({ filter: this.allOtherAquiferFilter() }),
          aquifersLineLayer({ filter: this.allOtherAquiferFilter() }),
          aquifersFillLayer({ id: CURRENT_AQUIFER_FILL_LAYER_ID, filter: this.currentAquiferFilter() }),
          aquifersLineLayer({ id: CURRENT_AQUIFER_LINE_LAYER_ID, filter: this.currentAquiferFilter() }),
          ecoCatLayer({ layout: { visibility: 'none' } }),
          surfaceWaterLicencesLayer({ layout: { visibility: 'none' } }),
          groundWaterLicencesLayer({ layout: { visibility: 'none' } }),
          wellsBaseAndArtesianLayer(),
          observationWellsLayer({ layout: { visibility: 'none' } }),
          wellsEmsLayer({ layout: { visibility: 'none' } }),
          wellsUncorrelatedLayer({ layout: { visibility: 'none' } })
        ]
      }
    },
    currentAquiferFilter () {
      return [
        'case',
        ['==', ['get', 'aquifer_id'], this.aquiferId], true,
        false
      ]
    },
    allOtherAquiferFilter () {
      const filter = aquiferLayerFilter(this.showUnpublished, false)
      // splice in a filter to remove the current aquifer from this layer
      filter.splice(1, 0, ['==', ['get', 'aquifer_id'], this.aquiferId], false)
      return filter
    },
    layersChanged (layerId, show) {
      // Find the layer and mark it as shown so the legend can be updated properly
      this.mapLayers.find((layer) => layer.id === layerId).show = show

      this.legendControl.update()

      // Turn the layer's visibility on / off
      this.map.setLayoutProperty(layerId, 'visibility', show ? 'visible' : 'none')
    },
    zoomToAquifer (fitBoundsOptions) {
      if (!this.geom) { return }

      /* Compute the bounds from the MultiPolygon geometry coordinates */
      const bounds = computeBoundsFromMultiPolygon(this.geom.coordinates)

      const options = {
        padding: 40,
        ...fitBoundsOptions
      }

      this.map.fitBounds(bounds, options)
    },
    setSelectedAquifer (aquiferId, focused = true) {
      this.map.setFeatureState(
        { source: AQUIFERS_SOURCE_ID, id: aquiferId, sourceLayer: AQUIFERS_SOURCE_ID },
        { focused }
      )
    },
    createAquiferPopupElement (features, { canInteract }) {
      return createAquiferPopupElement(features, this.map, this.$router, {
        canInteract,
        currentAquiferId: this.aquiferId,
        aquiferLayerIds: [ AQUIFERS_FILL_LAYER_ID, CURRENT_AQUIFER_FILL_LAYER_ID ]
      })
    },
    createWellPopupElement (features, { canInteract }) {
      return createWellPopupElement(features, this.map, this.$router, {
        canInteract,
        currentAquiferId: this.aquiferId,
        wellLayerIds: [
          WELLS_BASE_AND_ARTESIAN_LAYER_ID,
          WELLS_OBSERVATION_LAYER_ID,
          WELLS_UNCORRELATED_LAYER_ID,
          WELLS_EMS_LAYER_ID
        ]
      })
    },
    createEcocatPopupElement (features, { canInteract }) {
      return createEcocatPopupElement(features, this.map, {
        canInteract,
        ecocatLayerIds: [ DATABC_ECOCAT_LAYER_ID ]
      })
    },
    createSurfaceWaterLicencePopupElement (features, { canInteract }) {
      return createWaterLicencePopupElement(features, this.map, this.$router, {
        canInteract,
        ecocatLayerIds: [ DATABC_ECOCAT_LAYER_ID ]
      })
    },
    createGroundWaterLicencePopupElement (features, { canInteract }) {
      return createWaterLicencePopupElement(features, this.map, this.$router, {
        canInteract,
        ecocatLayerIds: [ DATABC_ECOCAT_LAYER_ID ]
      })
    }
  },
  watch: {
    aquiferId (newAquiferId, oldAquiferId) {
      this.setSelectedAquifer(oldAquiferId, false)
      this.setSelectedAquifer(newAquiferId, true)
    },
    geom (newGeom, oldGeom) {
      if (newGeom && newGeom !== oldGeom) {
        const options = {}
        if (this.jumpToAquifer) {
          // We set the duration option to zero for `fitBounds()` to make it jump to the aquifer
          // which avoids a long fly-to which will end up loading too many vector tiles.
          options.duration = 0
        }
        // From now on when a user selects a different aquifer on the map we fly to it
        this.jumpToAquifer = false
        this.zoomToAquifer(options)
      }
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";

#single-aquifer-map {
  height: 600px;
}
</style>
