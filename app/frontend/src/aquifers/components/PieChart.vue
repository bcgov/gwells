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

<style>
</style>

<script>
import { Pie } from 'vue-chartjs'
import { groupBy, map, sumBy } from 'lodash'

export default {
  extends: Pie,
  props: ['chartData'],
  watch: {
    chartData (newChartData) {
      this.renderPieChart(newChartData)
    }
  },
  mounted () {
    this.renderPieChart(this.chartData)
  },

  methods: {
    renderPieChart (newChartData) {
      if (Object.keys(newChartData).length) {
        const groupedLabels = groupBy(newChartData, (o) => o.purpose__description)
        const groupedSum = map(groupedLabels, (val, key) => {
          let sum = {}
          sum[key] = sumBy(val, o => o.total_qty)
          return sum
        })
        const chartLabel = groupedSum.map(o =>
          Object.keys(o)[0].split(' - ')[1] + // the label, without code.
          ': ' +
          Object.values(o)[0]) // the value of the pie slice.
        const chartData = groupedSum.map(o => Object.values(o)[0])

        this.renderChart({
          labels: chartLabel,
          datasets: [
            {
              // color-blindness safe colors:
              backgroundColor: ['#E69F00', '#56B4E9', '#2B9F78', '#F0E442', '#CC79A7', '#D55E00', '#0072B2'],
              data: chartData
            }
          ]
        }, {
          legend: {
            display: true
          },
          tooltips: {
            enabled: false
          },
          responsive: true,
          maintainAspectRatio: true
        })
      }
    }
  }
}
</script>
