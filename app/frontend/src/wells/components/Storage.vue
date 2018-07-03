<template>
  <div class="row no-gutters">
    <div class="col-md-12">
      <div v-if="loading" class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
      <div v-else>
        <!-- public documents -->
        <table id="additional_documentation_table" class="table table-sm table-bordered table-striped">
          <thead>
              <th>Document Link</th>
          </thead>
          <tbody>
            <tr v-if="error">
              <td>{{error}}</td>
            </tr>
            <tr v-else-if="files && files.public && files.public.length" v-for="(file, index) in files.public" :key="index">
              <td>
                <a :href="file.url" target="_blank">{{file.name}}</a>
              </td>
            </tr>
            <tr v-else>
              <td>
                <div class="row no-gutters hide-for-print show-for-screen">
                  <div id="no_documentation_msg">No additional documentation currently available for this well.</div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- private documents -->
        <div v-if="userRoles.wellsView">
          <table id="additional_documentation_table" class="table table-sm table-bordered table-striped">
            <thead>
                <th>Document Link (Internal documentation - authorized access only)</th>
            </thead>
            <tbody>
              <tr v-if="error">
                <td>{{error}}</td>
              </tr>
              <tr v-else-if="files && files.private && files.private.length" v-for="(file, index) in files.private" :key="index">
                <td>
                  <a :href="file.url" target="_blank">{{file.name}}</a>
                </td>
              </tr>
              <tr v-else>
                <td>
                  <div class="row no-gutters hide-for-print show-for-screen">
                    <div id="no_documentation_msg">No additional private documentation currently available for this well.</div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
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
  methods: {
  },
  computed: {
    ...mapGetters(['userRoles'])
  },
  created () {
    ApiService.query('well/123/files').then((response) => {
      this.files = response.data
    }).catch((e) => {
      console.error(e)
      this.error = 'Unable to retrieve file list.'
    }).finally(() => {
      this.loading = false
    })
  }
}
</script>

<style lang="scss">
@import url('https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css');
</style>
