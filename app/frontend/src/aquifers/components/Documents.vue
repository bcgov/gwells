<template>
  <div id="aquifer-documents">
    <div v-if="loading" class="row no-gutters">
      <div class="col-md-12">
        Loading documents...
        <div class="fa-2x text-center">
          <i class="fa fa-circle-o-notch fa-spin"></i>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="row no-gutters mt-3">
        <div class="col-md-12">
          <!-- public documents -->
          <div v-if="error">
            {{error}}
          </div>
          <ul v-else-if="files && files.public && files.public.length">
            <li v-for="(file, index) in files.public" :key="index">
              <a :href="file.url" :download="file.name" target="_blank">{{file.name}}</a>
            </li>
          </ul>
          <div v-else>
              No additional documentation currently available for this aquifer.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'

export default {
  name: 'AquiferDocuments',
  props: {
    aquifer: null
  },
  data () {
    return {
      loading: false,
      files: null,
      error: null
    }
  },
  methods: {
    fetchDocuments () {
      this.loading = true
      ApiService.query('aquifers/' + this.aquifer + '/files').then((response) => {
        this.files = response.data
      }).catch((e) => {
        console.error(e)
        this.error = 'Unable to retrieve file list.'
      }).finally(() => {
        this.loading = false
      })
    }
  },
  created () {
    this.fetchDocuments()
  }
}
</script>

<style lang="scss">
</style>
