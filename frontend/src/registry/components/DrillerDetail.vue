<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-xs-12 col-sm-8">
        {{person.name}}          
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'person-detail',
  data () {
    return {
      person: {
        name: 'John Bobert',
        certNumber: 'CGWA930209',
        certAuthority: 'Canadian Groundwater Association',
        qualificationCode: 'DRILL'
      }
    }
  }

}
</script>

<style>

</style>
