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
  <b-container id="bulk-home-screen">
    <b-card>
      <div v-if="noPerm">
        <b-alert show variant="danger" >
          You do not have permission to make any bulk changes to Gwells.
        </b-alert>
        Return <router-link to="/">home</router-link>
      </div>
      <h2 class="border-bottom pb-1 mb-3">Bulk Operations</h2>
      <p>
        Update multiple wells or aquifers at the same time with the following bulk operation utilities.
      </p>
      <ul>
        <li>
          <h5><router-link v-if="perms.wellAquiferCorrelation" :to="{ name: 'bulk-well-aquifer-correlation' }">Well Aquifer Correlation</router-link></h5>
          <p>
            Allow bulk changes to well aquifer correlations to be performed based on an uploaded CSV file.
          </p>
        </li>
        <li>
          <h5><router-link v-if="perms.wellAquiferCorrelation" :to="{ name: 'bulk-aquifer-documents' }">Aquifer Documents</router-link></h5>
          <p>
            Upload multiple documents to one or more aquifers.
          </p>
        </li>
      </ul>
    </b-card>
  </b-container>
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
      return !Object.values(this.perms).every(x => x)
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
