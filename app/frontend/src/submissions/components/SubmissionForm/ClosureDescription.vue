<template>
  <fieldset>
    <legend>Decommission Description</legend>
    <b-row>
      <b-col cols="12">
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
                  :key="`closureDescription${index}`"
                  :id="`closureDescription${index}`">

                <td class="input-width-small">
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`closureFrom${index}`"
                      v-model="item.start"
                      :errors="getClosureError(index).start"
                      :loaded="getFieldsLoaded(index).start"
                  />
                </td>
                <td class="input-width-small">
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`closureTo${index}`"
                      v-model="item.end"
                      :errors="getClosureError(index).end"
                      :loaded="getFieldsLoaded(index).end"
                  />
                </td>
                <td>
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`decommissionMaterial${index}`"
                      v-model="item.material"
                      :errors="getClosureError(index).material"
                      :loaded="getFieldsLoaded(index).material"
                  />
                </td>
                <td>
                  <form-input
                      group-class="mt-1 mb-0"
                      :id="`closureObservations${index}`"
                      v-model="item.observations"
                      :errors="getClosureError(index).observations"
                      :loaded="getFieldsLoaded(index).observations"
                  />
                </td>
                <td class="align-middle">
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
    closureDescriptionSet: {
      type: Array,
      default: () => ([])
    },
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
    },
    getClosureError (index) {
      if (this.errors && 'closure_description_set' in this.errors && index in this.errors['closure_description_set']) {
        return this.errors['closure_description_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'closure_description_set' in this.fieldsLoaded && index in this.fieldsLoaded['closure_description_set']) {
        return this.fieldsLoaded['closure_description_set'][index]
      }
      return {}
    }
  },
  created () {
    if (!this.closureDescriptionSet.length) {
      this.addClosureRow()
    }
  }
}
</script>

<style>

</style>
