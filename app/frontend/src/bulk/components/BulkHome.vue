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
  <b-card id="bulk-home-screen" class="container p-1">
    <div v-if="noPerm">
      <b-alert show variant="danger" >
        You do not have permission to make any bulk changes to Gwells.
      </b-alert>
      Return <router-link to="/">home</router-link>
    </div>
    <div v-else>
      <h2 class="border-bottom pb-1 mb-3">Bulk Operations</h2>
      <p>
        Update multiple wells or aquifers at the same time with the following bulk operation utilities.
      </p>
      <ul>
        <li v-if="perms.wellAquiferCorrelation">
          <h5><router-link :to="{ name: 'bulk-well-aquifer-correlation' }">Well Aquifer Correlation</router-link></h5>
          <p>
            Allow bulk changes to well aquifer correlations to be performed based on an uploaded CSV file.
          </p>
        </li>
        <li v-if="perms.wellDocuments">
          <h5><router-link :to="{ name: 'bulk-well-documents' }">Well Documents</router-link></h5>
          <p>
            Upload multiple documents to one or more wells.
          </p>
        </li>
        <li v-if="perms.aquiferDocuments">
          <h5><router-link :to="{ name: 'bulk-aquifer-documents' }">Aquifer Documents</router-link></h5>
          <p>
            Upload multiple documents to one or more aquifers.
          </p>
        </li>
        <li v-if="perms.verticalAquiferExtents">
          <h5><router-link :to="{ name: 'bulk-vertical-aquifer-extents' }">Vertical Aquifer Extents</router-link></h5>
          <p>
            Upload a CSV with vertical aquifer extents.
          </p>
        </li>
      </ul>
    </div>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters(['userRoles']),
    perms () {
      return this.userRoles.bulk || {}
    },
    noPerm () {
      return Object.values(this.perms).every(x => !x)
    }
  }
}
</script>
<style lang="scss">
#bulk-home-screen {
  ul, li {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  li {
    margin-top: 1rem;
  }
}
</style>
