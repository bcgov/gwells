<template>
  <div>
    <div v-if="loading" class="row no-gutters">
      <div class="col-md-12">
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
              No additional documentation currently available for this well.
          </div>
        </div>
      </div>
      <div class="row no-gutters" v-if="userRoles.wellsView">
        <div class="col-md-12">
          <h4>Internal documentation - authorized access only</h4>
            <div v-if="error">
              {{error}}
            </div>
            <ul v-else-if="files && files.private && files.private.length">
              <li v-for="(file, index) in files.private" :key="index">
                <a :href="file.url" :download="file.name" target="_blank">{{file.name}}</a>
              </li>
            </ul>
              <div v-else>
                No additional private documentation currently available for this well.
              </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      loading: true,
      files: null,
      error: null
    }
  },
  watch: {
    // This is not ideal. If you are authorized, we need to show you a different set of wells, however,
    // auth is happening asynchronously somewhere else on the page.
    keycloak: function () {
      if (this.wellTag) {
        ApiService.query('wells/' + this.wellTag + '/files').then((response) => {
          this.files = response.data
        }).catch((e) => {
          console.error(e)
          this.error = 'Unable to retrieve file list.'
        }).finally(() => {
          this.loading = false
        })
      }
    }
  },
  computed: {
    ...mapGetters(['userRoles', 'keycloak']),
    wellTag () {
      const wellMeta = document.head.querySelector('meta[name="well.tag_number"]')
      if (wellMeta) {
        return wellMeta.content
      }
      return null
    }
  }
}
</script>

<style lang="scss">
@import url('https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css');
</style>
