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
  <div v-if="files">
    <p class="font-weight-bold">Download all wells</p>
    <ul>
      <li v-for="file in files" :key="file.name"><a :href="file.url">Well extract ({{file.description}})</a> ({{format_size(file.size)}}) - {{format_date(file.last_modified)}}</li>
    </ul>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'

export default {
  data () {
    return {
      files: null
    }
  },
  created () {
    ApiService.query('wells/extracts').then((response) => {
      this.files = response.data
    }).catch((e) => {
      console.error(e)
    })
  },
  methods: {
    format_date (dateString) {
      const theDate = new Date(dateString)
      return theDate.toLocaleString('en-CA', {year: 'numeric', month: 'long', day: 'numeric'})
    },
    format_size (size) {
      return `${Math.floor(size / 1024 / 1024)} MB`
    }
  }
}
</script>

<style lang="scss">
</style>
