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
  <div>
    <gwells-header/>
    <main role="main" class="p-0 mt-0 mt-sm-4 container container-wide">
      <router-view/>
    </main>
    <gwells-footer/>
  </div>
</template>

<script>
import Header from '@/common/components/Header'
import Footer from '@/common/components/Footer'

export default {
  name: 'App',
  components: {
    'gwells-header': Header,
    'gwells-footer': Footer
  }
}
</script>

<style lang="scss">
@import "../common/common.scss";

.container-wide {
  max-width: 1400px;
}

main a {
  text-decoration: underline;
}
</style>
