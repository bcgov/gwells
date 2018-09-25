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

                <td class="input-width-small">
                  <b-input
                      :id="`closureFrom${index}`"
                      v-model="item.start"
                  />
                </td>
                <td class="input-width-small">
                  <b-input
                      :id="`closureTo${index}`"
                      v-model="item.end"
                  />
                </td>
                <td>
                  <b-input
                      :id="`decommissionMaterial${index}`"
                      v-model="item.decommision_material"
                  />
                </td>
                <td>
                  <b-input
                      :id="`closureObservations${index}`"
                      v-model="item.observations"
                  />
                </td>
                <td class="align-middle">
                  <b-btn size="sm" variant="primary" :id="`removeClosureRowButton${index}`"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <b-btn size="sm" variant="primary" id="addClosureRowButton"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
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
    closureDescriptionSet: {
      type: Array,
      default: () => ([{start: '', end: '', decommision_material: '', observations: ''}, {start: '', end: '', decommision_material: '', observations: ''}])
    },
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    }
  },
  fields: {
    closureDescriptionSetInput: 'closureDescriptionSet'
  },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>
