<template>
  <fieldset>
    <legend>Description</legend>
    <b-row>
      <b-col cols="12" md="8">
        <div class="table-responsive">
          <table class="table table-sm">
            <thead>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Decommission Material</th>
                <th>Observations</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr
                  v-for="(item, index) in closureDescriptionSet"
                  :key="`closureDescription${index}`">

                <td class="input-width-small pb-0">
                  <form-input
                      group-class="my-0"
                      :id="`closureFrom${index}`"
                      v-model="item.start"
                  />
                </td>
                <td class="input-width-small pb-0">
                  <form-input
                      group-class="my-0"
                      :id="`closureTo${index}`"
                      v-model="item.end"
                  />
                </td>
                <td class="pb-0">
                  <form-input
                      group-class="my-0"
                      :id="`decommissionMaterial${index}`"
                      v-model="item.material"
                  />
                </td>
                <td class="pb-0">
                  <form-input
                      group-class="my-0"
                      :id="`closureObservations${index}`"
                      v-model="item.observations"
                  />
                </td>
                <td class="align-middle pb-0">
                  <b-btn size="sm" variant="primary" @click="removeClosureRow(index)" :id="`removeClosureRowButton${index}`"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <b-btn size="sm" variant="primary" @click="addClosureRow" id="addClosureRowButton"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  mixins: [inputBindingsMixin],
  props: {
    closureDescriptionSet: Array,
    errors: Array,
    fieldsLoaded: Object
  },
  fields: {
    closureDescriptionSetInput: 'closureDescriptionSet'
  },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    addClosureRow () {
      this.closureDescriptionSetInput.push({start: '', end: '', material: '', observations: ''})
    },
    removeClosureRow (rowNumber) {
      this.closureDescriptionSetInput.splice(rowNumber, 1)
    }
  }
}
</script>

<style>

</style>
