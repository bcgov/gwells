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
import { merge } from 'lodash'

export default {
  extends: Pie,
  props: ['data', 'labels', 'chartOptions'],
  data () {
    return {
      defaultChartOptions: {
        legend: {
          display: true
        },
        tooltips: {
          enabled: true
        },
        layout: {
          padding: {
            top: 20
          }
        },
        responsive: true,
        maintainAspectRatio: true
      }
    }
  },
  watch: {
    data (newChartData) {
      this.renderPieChart()
    },
    labels (labels) {
      this.renderPieChart()
    }
  },
  mounted () {
    this.renderPieChart()
  },
  methods: {
    renderPieChart (newChartData) {
      this.renderChart({
        labels: this.labels.map(l => `  ${l}`), // adds two spaces to prevent cut off text
        datasets: [
          {
            // color-blindness safe colors:
            backgroundColor: ['#E69F00', '#56B4E9', '#2B9F78', '#F0E442', '#CC79A7', '#D55E00', '#0072B2', '#EE442F', '#9C9EB5', '#8B7F47'],
            data: this.data
          }
        ]
      }, merge({}, this.defaultChartOptions, this.chartOptions))
    }
  }
}
</script>
