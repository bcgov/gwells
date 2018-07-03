<template>
  <div class="row no-gutters">
    <div class="col-md-12">
      <table id="additional_documentation_table" class="table table-sm table-bordered table-striped">
        <thead>
            <th>Document Link</th>
        </thead>
        <tbody>
          <tr v-for="(file, index) in files" :key="index">
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
      files: null,
      error: null
    }
  },
  methods: {

  },
  created () {
    ApiService.query('/gwells/api/v1/well/123/files').then((response) => {
      this.files = response.data
    }).catch((e) => {
      console.error(e)
      this.error = 'Unable to retrieve file list.'
    })
  }
}
</script>

<style lang="scss">
</style>
