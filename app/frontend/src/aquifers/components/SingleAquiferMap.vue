<template>
  <div id="single-aquifer-map" class="map">
    <p id="unsupported-browser" v-if="browserUnsupported">Your browser is unable to view the map</p>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl'
import GestureHandling from '@geolonia/mbgl-gesture-handling'

import {
  DATABC_ROADS_SOURCE,
  DATABC_CADASTREL_SOURCE,
  vectorLayerConfig,
  WELLS_LAYER_SOURCE,
  AQUIFERS_LAYER_SOURCE,
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
  DATABC_WATER_LICENCES_LAYER_ID,
  DATABC_OBSERVATION_WELLS_LAYER_ID,
  DATABC_OBSERVATION_WELLS_LAYER,
  DATABC_WATER_LICENCES_LAYER,
  DATABC_ECOCAT_LAYER,
  DATABC_ECOCAT_SOURCE,
  DATABC_WATER_LICENCES_SOURCE_ID,
  DATABC_ECOCAT_SOURCE_ID,
  DATABC_OBSERVATION_WELLS_SOURCE_ID,
  DATABC_OBSERVATION_WELLS_SOURCE,
  DATABC_WATER_LICENCES_SOURCE,
  AQUIFERS_FILL_LAYER_ID,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  WELLS_EMS_LAYER_ID,
  WELLS_UNCORRELATED_LAYER_ID
} from '../../common/mapbox/layers'
import { computeBoundsFromMultiPolygon } from '../../common/mapbox/geometry'
import { LayersControl, LegendControl } from '../../common/mapbox/controls'
import { setupMapTooltips, setupMapPopups } from '../popup'

import cadastralLegendSrc from '../../common/assets/images/cadastral.png'
import ecoCatWaterLegendSrc from '../../common/assets/images/ecocat-water.svg'
import groundWaterLicenceActiveLegendSrc from '../../common/assets/images/gwater-licence-active.svg'
import groundWaterLicenceInactiveLegendSrc from '../../common/assets/images/gwater-licence-inactive.svg'
import observationWellInactiveLegendSrc from '../../common/assets/images/owells-inactive.svg'
import observationWellActiveLegendSrc from '../../common/assets/images/owells-active.svg'

import wellsAllLegendSrc from '../../common/assets/images/wells-all.svg'
import wellsArtesianLegendSrc from '../../common/assets/images/wells-artesian.svg'
import uncorrelatedWellsIconSrc from '../../common/assets/images/wells-uncorrelated.svg'
import emsWellsIconSrc from '../../common/assets/images/wells-ems.svg'

export default {
  name: 'SingleAquiferMap',
  props: ['aquifer-id', 'geom', 'wells'],
  data () {
    return {
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
          label: 'EcoCat – water related reports',
          imageSrc: ecoCatWaterLegendSrc
        },
        {
          show: false,
          id: DATABC_WATER_LICENCES_LAYER_ID,
          label: 'Water licences',
          legend: [
            {
              imageSrc: groundWaterLicenceActiveLegendSrc,
              label: 'active'
            },
            {
              imageSrc: groundWaterLicenceInactiveLegendSrc,
              label: 'inactive'
            }
          ]
        },
        {
          show: false,
          id: DATABC_OBSERVATION_WELLS_LAYER_ID,
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
          id: WELLS_EMS_LAYER_ID,
          label: 'EMS wells',
          imageSrc: emsWellsIconSrc
        },
        {
          id: WELLS_UNCORRELATED_LAYER_ID,
          label: 'Uncorrelated wells',
          imageSrc: uncorrelatedWellsIconSrc
        }
      ]
    }
  },
  mounted () {
    this.$emit('mapLoading')

    this.initMapBox()
  },
  destroyed () {
    this.map.remove()
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
      new GestureHandling().addTo(this.map)

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
        customAttribution: 'MapBox | Powered by Esri | Government of British Columbia, DataBC, GeoBC '
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
        /* Setup tooltips and popups  */

        setupMapTooltips(this.map, this.$router)

        setupMapPopups(this.map, this.$router)

        setupAquiferHover(this.map, AQUIFERS_FILL_LAYER_ID)

        /* Goto Aquifer */

        this.setSelectedAquifer(this.aquiferId, true)

        this.zoomToAquifer()

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
          [DATABC_OBSERVATION_WELLS_SOURCE_ID]: DATABC_OBSERVATION_WELLS_SOURCE,
          [WELLS_LAYER_SOURCE]: vectorLayerConfig(WELLS_LAYER_SOURCE),
          [AQUIFERS_LAYER_SOURCE]: vectorLayerConfig(AQUIFERS_LAYER_SOURCE, { promoteId: 'aquifer_id' })
        },
        layers: [
          DATABC_ROADS_LAYER,
          DATABC_CADASTREL_LAYER,
          DATABC_ECOCAT_LAYER,
          DATABC_WATER_LICENCES_LAYER,
          DATABC_OBSERVATION_WELLS_LAYER,
          aquifersFillLayer({ aquiferId: this.aquiferId }),
          aquifersLineLayer({ aquiferId: this.aquiferId }),
          wellsBaseAndArtesianLayer(),
          wellsEmsLayer({ layout: { visibility: 'none' } }),
          wellsUncorrelatedLayer({ layout: { visibility: 'none' } })
        ]
      }
    },
    layersChanged (layerId, show) {
      // Find the layer and mark it as shown so the legend can be updated properly
      this.mapLayers.find((layer) => layer.id === layerId).show = show

      this.legendControl.update()

      // Turn the layer's visibility on / off
      this.map.setLayoutProperty(layerId, 'visibility', show ? 'visible' : 'none')
    },
    zoomToAquifer (well) {
      if (!this.geom) { return }

      /* Compute the bounds from the MultiPolygon geometry coordinates */
      const bounds = computeBoundsFromMultiPolygon(this.geom.coordinates)

      this.map.fitBounds(bounds, {
        padding: 20
      })
    },
    setSelectedAquifer (aquiferId, focused = true) {
      this.map.setFeatureState(
        { source: AQUIFERS_LAYER_SOURCE, id: aquiferId, sourceLayer: AQUIFERS_LAYER_SOURCE },
        { focused }
      )
    }
  },
  watch: {
    aquiferId (newAquiferId, oldAquiferId) {
      this.setSelectedAquifer(oldAquiferId, false)
      this.setSelectedAquifer(newAquiferId, true)
    },
    geom (newGeom, oldGeom) {
      if (newGeom && newGeom !== oldGeom) {
        this.zoomToAquifer()
      }
    }
  }
}
</script>
<style lang="scss">
@import "~mapbox-gl/dist/mapbox-gl.css";

#single-aquifer-map {
  height: 600px;

  @import "@/common/mapbox.scss";
}
</style>
