<template>
  <div>
    <select v-model="selectedChartType" class="mb-4 px-3 py-2 border border-gray-900 rounded-md shadow-sm focus:outline-none sm:text-sm">
      <option value="line">Line Chart</option>
      <option value="bar">Bar Chart</option>
      <option value="scatter">Scatter Plot</option>
    </select>
    <component :is="chartComponent" :data="chartData" :options="chartOptions"></component>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watchEffect } from "vue";
import { Line, Bar, Scatter } from "vue-chartjs";
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
  ChartData,
  ChartOptions,
  Point,
} from 'chart.js'
import { DataPoint } from '../types'

ChartJS.register(Title, Tooltip, Legend, LineElement, BarElement, PointElement, LinearScale, CategoryScale);

export default defineComponent({
  name: "ChartComponent",
  props: {
    data: {
      type: Array as () => DataPoint[],
      required: true,
    },
    xFeature: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const selectedChartType = ref<'line' | 'bar' | 'scatter'>('line');

    const chartData = ref<ChartData<'line' | 'bar' | 'scatter', (number | Point | null)[], unknown>>({
      labels: props.data.map((d) => d.x.toString()),
      datasets: [
        {
          label: "Actual",
          data: props.data.map((d) => d.y),
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: false,
        },
        {
          label: "Predicted",
          data: props.data.map((d) => d.predicted),
          borderColor: "rgb(255, 99, 132)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          fill: false,
        },
      ],
    });

    const chartOptions = ref<ChartOptions<'line' | 'bar' | 'scatter'>>({
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: `Predicted vs Actual Values (${props.xFeature})`,
        },
      },
    });

    const chartComponent = ref<typeof Line | typeof Bar | typeof Scatter>(Line);

    watchEffect(() => {
      if (selectedChartType.value === "line") {
        chartComponent.value = Line;
      } else if (selectedChartType.value === "bar") {
        chartComponent.value = Bar;
      } else if (selectedChartType.value === "scatter") {
        chartComponent.value = Scatter;
      }

      const labels = props.data.map((d) => d.x.toString());
      const actualData = props.data.map((d) => d.y);
      const predictedData = props.data.map((d) => d.predicted);

      if (selectedChartType.value === "line") {
        chartData.value = {
          labels,
          datasets: [
            {
              label: "Actual",
              data: actualData,
              borderColor: "rgb(75, 192, 192)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: false,
            },
            {
              label: "Predicted",
              data: predictedData,
              borderColor: "rgb(255, 99, 132)",
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              fill: false,
            },
          ],
        } as ChartData<'line', (number | Point | null)[], unknown>;
      } else if (selectedChartType.value === "bar") {
        chartData.value = {
          labels,
          datasets: [
            {
              label: "Actual",
              data: actualData,
              borderColor: "rgb(75, 192, 192)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: false,
            },
            {
              label: "Predicted",
              data: predictedData,
              borderColor: "rgb(255, 99, 132)",
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              fill: false,
            },
          ],
        } as ChartData<'bar', (number | Point | null)[], unknown>;
      } else if (selectedChartType.value === "scatter") {
        chartData.value = {
          labels,
          datasets: [
            {
              label: "Actual",
              data: actualData.map((y, i) => ({ x: i, y })),
              borderColor: "rgb(75, 192, 192)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: false,
            },
            {
              label: "Predicted",
              data: predictedData.map((y, i) => ({ x: i, y })),
              borderColor: "rgb(255, 99, 132)",
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              fill: false,
            },
          ],
        } as ChartData<'scatter', (number | Point | null)[], unknown>;
      }
    });

    return {
      chartData,
      chartOptions,
      selectedChartType,
      chartComponent,
    };
  },
});
</script>
