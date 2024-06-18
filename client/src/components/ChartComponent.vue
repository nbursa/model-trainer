<template>
  <div>
    <line-chart :chart-data="chartData" :options="chartOptions"></line-chart>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watchEffect } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

interface DataPoint {
  x: number;
  y: number;
  predicted: number;
}

export default defineComponent({
  name: "ChartComponent",
  components: {
    LineChart: Line,
  },
  props: {
    data: {
      type: Array as () => DataPoint[],
      required: true,
    },
  },
  setup(props) {
    const chartData = ref({
      labels: [],
      datasets: [
        {
          label: "Actual",
          data: [],
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: false,
        },
        {
          label: "Predicted",
          data: [],
          borderColor: "rgb(255, 99, 132)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          fill: false,
        },
      ],
    });

    const chartOptions = ref({
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Predicted vs Actual Values",
        },
      },
    });

    watchEffect(() => {
      if (props.data.length > 0) {
        chartData.value.labels = props.data.map((d) => d.x);
        chartData.value.datasets[0].data = props.data.map((d) => d.y);
        chartData.value.datasets[1].data = props.data.map((d) => d.predicted);
      }
    });

    return {
      chartData,
      chartOptions,
    };
  },
});
</script>
