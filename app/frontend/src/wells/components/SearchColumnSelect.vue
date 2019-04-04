/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
  <div>
    <b-button
      variant="dark"
      v-b-modal.columnSelectModal>
      Add/remove columns
    </b-button>
    <b-modal
      id="columnSelectModal"
      title="Column Display"
      ok-title="Apply"
      @ok="updateSelectedColumns()">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Column Name</th>
            <th scope="col">Display</th>
            <th scope="col">Order</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="column in columns" :key="column.id">
            <td>{{ column.label }}</td>
            <td>
              <b-form-checkbox
                :id="`${column.id}ColumnSelect`"
                :checked="column.selected"
                @input="$event ? selectColumn(column.id) : deselectColumn(column.id)"
              />
            </td>
            <td>
              <b-form-select
                :id="`${column.id}ColumnOrder`"
                :options="columnOrderRange"
                :value="column.order"
                @input="setColumnOrder(column.id, $event)" />
            </td>
          </tr>
        </tbody>
      </table>
    </b-modal>
  </div>
</template>

<script>
import {resultColumns, searchFields} from '@/wells/searchFields.js'

export default {
  model: {
    prop: 'selectedColumns',
    event: 'update'
  },
  props: {
    selectedColumns: Array, // Array of column ids
    columnData: Object
  },
  data () {
    return {
      localSelectedColumns: [...this.selectedColumns],
      columnOrders: {}
    }
  },
  computed: {
    availableColumnIds () {
      return [...resultColumns.default, ...resultColumns.optional].filter((columnId) => {
        if (this.columnData[columnId] !== undefined) {
          return true
        }

        return false
      })
    },
    columns () {
      return this.availableColumnIds.map((columnId) => {
        return {
          id: columnId,
          label: searchFields[columnId].label,
          order: this.columnOrders[columnId],
          selected: this.localSelectedColumns.includes(columnId)
        }
      })
    },
    columnOrderRange () {
      return Array.from(Array(this.availableColumnIds.length).keys()).map(i => i + 1)
    }
  },
  methods: {
    selectColumn (columnId) {
      this.localSelectedColumns.push(columnId)
    },
    deselectColumn (columnId) {
      const index = this.localSelectedColumns.indexOf(columnId)

      if (index >= 0) {
        this.localSelectedColumns.splice(index, 1)
      }
    },
    setColumnOrder (columnId, order) {
      this.columnOrders[columnId] = order
    },
    initColumnOrders () {
      let index = 0
      this.selectedColumns.forEach((columnId) => {
        index += 1
        this.setColumnOrder(columnId, index)
      })
      this.availableColumnIds.forEach((columnId) => {
        if (!this.selectedColumns.includes(columnId)) {
          index += 1
          this.setColumnOrder(columnId, index)
        }
      })
    },
    updateSelectedColumns () {
      const columnIds = [...this.localSelectedColumns]
      columnIds.sort((columnA, columnB) => {
        return this.columnOrders[columnA] - this.columnOrders[columnB]
      })
      this.$emit('update', columnIds)
    }
  },
  created () {
    this.initColumnOrders()
  }
}
</script>

<style>
</style>
