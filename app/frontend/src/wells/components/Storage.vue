<template>
  <div class="row no-gutters">
    <div class="col-md-12">
      <div v-if="loading" class="fa-2x text-center">
        <i class="fa fa-circle-o-notch fa-spin"></i>
      </div>
      <table v-else id="additional_documentation_table" class="table table-sm table-bordered table-striped">
        <thead>
            <th>Document Link</th>
        </thead>
        <tbody>
          <tr v-if="error">
            <td>{{error}}</td>
          </tr>
          <tr v-else v-for="(file, index) in files" :key="index">
            <td>
              <a :href="file.url" target="_blank">{{file.name}}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'

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
