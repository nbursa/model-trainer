<template>
  <div>
    <select
      v-model="selectedChartType"
      class="mb-4 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    >
      <option value="line">Line Chart</option>
      <option value="bar">Bar Chart</option>
      <option value="scatter">Scatter Plot</option>
    </select>
    <component
      :is="chartComponent"
      :chart-data="chartData"
      :options="chartOptions"
    ></component>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watchEffect } from 'vue'
import { Line, Bar, Scatter } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
} from 'chart.js'
import { DataPoint } from '../types'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale
)

export default defineComponent({
  name: 'ChartComponent',
  props: {
    data: {
      type: Array as () => DataPoint[],
      required: true,
    },
  },
  setup(props) {
    const chartData = ref({
      labels: props.data.map((d) => d.x),
      datasets: [
        {
          label: 'Actual',
          data: props.data.map((d) => d.y),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          fill: false,
        },
        {
          label: 'Predicted',
          data: props.data.map((d) => d.predicted),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          fill: false,
        },
      ],
    })

    const chartOptions = ref({
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Predicted vs Actual Values',
        },
      },
    })

    const selectedChartType = ref('line')

    const chartComponent = ref(Line)

    watchEffect(() => {
      if (selectedChartType.value === 'line') {
        chartComponent.value = Line
      } else if (selectedChartType.value === 'bar') {
        chartComponent.value = Bar
      } else if (selectedChartType.value === 'scatter') {
        chartComponent.value = Scatter
      }
    })

    watchEffect(() => {
      chartData.value.labels = props.data.map((d) => d.x)
      chartData.value.datasets[0].data = props.data.map((d) => d.y)
      chartData.value.datasets[1].data = props.data.map((d) => d.predicted)
    })

    return {
      chartData,
      chartOptions,
      selectedChartType,
      chartComponent,
    }
  },
})
</script>
