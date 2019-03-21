<template>
  <b-card class="container p-1 vpHeight">
    <b-row>
      <b-col sm="2"/>
      <b-col class="centerItems" sm="8">
        <h1>We're sorry, the page you're looking for doesn't exist.</h1>
        <div class="links">
          <b-link :to="{ path: '/' }" class="linkTxt">Search for a Groundwater Well</b-link><br>
          <b-link :to="{ path: '/aquifers/' }" class="linkTxt">Search for an Aquifer</b-link><br>
          <b-link :to="{ path: '/registries/'}" class="linkTxt">Search the Register of Well Drillers and Well Pump Installers</b-link><br>
        </div>
      </b-col>
      <b-col sm="2"/>
    </b-row>
  </b-card>
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
  .vpHeight {
    height:80vh;
  }
  .links {
    padding:20px;
  }
  .linkTxt {
    font-size:20px;
    text-decoration: underline;
  }
  .centerItems {
    padding-top:100px;
  }
</style>
