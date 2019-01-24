<template>
  <div id="person-documents">
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
              No additional documentation currently available for this person.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'PersonDocuments',
  props: {
    files: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      loading: false,
      error: null
    }
  }
}
</script>

<style lang="scss">
</style>
