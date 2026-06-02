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
  <fieldset>
    <legend :id="id">Type of Work</legend>
    <responsive-grid :cols="12" :md="6">
      <div class="flex flex-col gap-2">
        <label for="wellActivityTypeInput">Type of Work *</label>
        <RadioButtonGroup v-if="show.edit" v-model="wellActivityTypeInput" id="wellActivityTypeInput">
          <div class="flex align-items-center">
            <RadioButton inputId="wellActivityTypeInput.CON" value="CON"/>
            <label for="wellActivityTypeInput.CDN" class="ml-2">Construction</label>
          </div>
          <div class="flex align-items-center">
            <RadioButton inputId="wellActivityTypeInput.ALT" value="ALT"/>
            <label for="wellActivityTypeInput.ALT" class="ml-2">Alteration</label>
          </div>
          <div class="flex align-items-center">
            <RadioButton inputId="wellActivityTypeInput.DEC" value="DEC"/>
            <label for="wellActivityTypeInput.DEC" class="ml-2">Decommission</label>
          </div>
        </RadioButtonGroup>
      </div>
    </responsive-grid>
  </fieldset>
</template>

<script>
import { useCommonStore } from '@/stores/common.js'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ResponsiveGrid from '@/common/components/ResponsiveGrid.vue'

export default {
  mixins: [inputBindingsMixin],
  props: {
    wellActivityType: String,
    id: {
      type: String,
      isInput: false
    }
  },
  components: {
    ResponsiveGrid
  },
  computed: {
    commonStore () { return useCommonStore() },
    show () {
      return {
        edit: this.commonStore.userRoles.submissions.edit || this.commonStore.userRoles.wells.edit
      }
    }
  }
}
</script>

<style>
</style>
