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
  <span class="observation-well" :class="{error: owell.errorFetching, loading: owell.fetchingAnalysis}">
    <a :href="observationWellUrl()" target="_blank" class="d-print-url">
      {{ owell.observation_well_number }}
    </a>
    <span v-if="owell.waterLevels">
      Water Level Analysis:
      <a :href="waterAnalysisUrl()" target="_blank" class="d-print-url">
        {{ owell.waterLevels }}
      </a>
    </span>

    <span v-if="owell.errorFetching">
      <i
        :id="popupId"
        class="fa fa-exclamation-circle fa-xs pt-0 mt-0 d-print-none"
        :class="{'fa-spin': owell.fetchingAnalysis}"
        @click="$emit('reload', owell)"/>
      <b-popover
        :target="popupId"
        triggers="hover"
        content="Error retrieving water levels information. Click to retry."/>
    </span>
  </span>
</template>

<style lang="scss">
.observation-well {
  i.fa {
    color: red;
    outline: none;

    &:hover {
      &:before {
        content: "\f021";
      }
    }
  }

  &.loading {
    i.fa {
      color: black;

      &:before {
        content: "\f021";
      }
    }
  }
}
</style>

<script>
export default {
  props: ['observationWell'],
  data () {
    return {

    }
  },
  computed: {
    owell () {
      return this.observationWell || {}
    },
    obsWellNumber () {
      return this.owell.observation_well_number
    },
    popupId () {
      return `obswell-${this.obsWellNumber}`
    }
  },
  methods: {
    waterAnalysisUrl () {
      if (this.owell.hasLevelAnalysis) {
        return 'http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html'
      }
      return null
    },
    observationWellUrl () {
      return `https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d&find=OBS WELL ${this.obsWellNumber}`
    }
  }
}
</script>
