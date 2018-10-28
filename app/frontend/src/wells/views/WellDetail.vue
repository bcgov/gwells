<template>
  <div>
    <b-card no-body class="mb-3 container container-wide">
      <b-breadcrumb :items="breadcrumbs" class="py-0 my-2"></b-breadcrumb>
    </b-card>
    <b-card class="container container-wide p-1">
      <h2>Well Summary</h2>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'WellDetail',
  data () {
    return {
      breadcrumbs: [
        {
          text: 'Well Search',
          to: { name: 'wells-home' }
        },
        {
          text: 'Well Summary',
          active: true
        }
      ]
    }
  }
}
</script>

<style>

</style>
