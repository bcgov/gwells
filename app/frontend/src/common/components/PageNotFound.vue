<template>
  <Card class="rounded-lg ml-30 mr-30 bg-white">
    <template #content>
      <div class="m-30 mb-130">
        <h1 class="text-4xl">We're sorry, the page you're looking for doesn't exist.</h1>
        <div class="mt-5 ml-5 flex flex-col">
          <router-link  :to="{ path: '/' }" class="text-2xl underline text-blue-800 hover:text-blue-600">Search for a Groundwater Well</router-link >
          <router-link  :to="{ path: '/aquifers/' }" class="text-2xl underline w-full text-blue-800 hover:text-blue-600">Search for an Aquifer</router-link >
          <router-link  :to="{ path: '/registries/'}" class="text-2xl underline text-blue-800 hover:text-blue-600">Search the Register of Well Drillers and Well Pump Installers</router-link >
        </div>
      </div>
    </template>
  </Card>
</template>

<script>
export default {
  name: 'PageNotFound',
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<style>

</style>
