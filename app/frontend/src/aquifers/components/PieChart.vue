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
  <Pie :data="dataValues" :options="options" />
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'PieChart',
  components: {
    Pie
  },
  props: ['data', 'labels', 'chartOptions'],
  data () {
    return {
      dataValues: {
        labels: this.$props.labels,
        datasets: [{
            backgroundColor: [
              '#E69F00', '#56B4E9', '#2B9F78', '#F0E442', '#CC79A7'
              , '#D55E00', '#0072B2', '#EE442F', '#9C9EB5', '#8B7F47'
            ],
            data: this.$props.data
        }]
      }
    }
  }
}
</script>
