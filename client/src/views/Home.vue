<template>
  <div class="mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">ML Model Builder</h1>
    <form @submit.prevent="trainModel">
      <div class="mb-4 flex flex-col items-center justify-center">
        <label for="dataset" class="block text-sm font-medium text-gray-700 mb-2">Dataset</label>
        <div class="relative w-64 h-16 border border-gray-300 rounded-lg flex items-center justify-center">
          <input type="file" id="dataset" @change="handleFileUpload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
          <span v-if="!dataset" class="text-gray-500">Click to select a file</span>
          <span v-else class="text-gray-700">{{ dataset.name }}</span>
        </div>
      </div>
      <div class="mb-4">
        <label for="features" class="block text-sm font-medium text-gray-700">Features</label>
        <input type="text" id="features" v-model="features" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="e.g., x" />
      </div>
      <div class="mb-4">
        <label for="target" class="block text-sm font-medium text-gray-700">Target</label>
        <input type="text" id="target" v-model="target" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="e.g., y" />
      </div>
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Train Model</button>
    </form>
    <div v-if="score !== null" class="mt-4">
      <h2 class="text-xl font-bold">Model Score: {{ score }}</h2>
    </div>
    <chart-component v-if="modelData.length > 0" :data="modelData" class="mt-4"></chart-component>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import axios from "axios";
import ChartComponent from "../components/ChartComponent.vue";

interface ModelData {
  x: number;
  y: number;
  predicted: number;
}

export default defineComponent({
  name: "Home",
  components: {
    ChartComponent,
  },
  setup() {
    const features = ref("");
    const target = ref("");
    const score = ref<number | null>(null);
    const dataset = ref<File | null>(null);
    const modelData = ref<ModelData[]>([]);

    const handleFileUpload = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files.length > 0) {
        dataset.value = input.files[0];
      }
    };

    const trainModel = async () => {
      if (dataset.value) {
        const formData = new FormData();
        formData.append("dataset", dataset.value);
        formData.append("features", features.value);
        formData.append("target", target.value);

        try {
          const response = await axios.post(
            `/api/models/train`,
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data"
              }
            }
          );
          score.value = response.data.score;
          modelData.value = response.data.data.map((row: any) => ({
            x: row[features.value],
            y: row[target.value],
            predicted: row.predicted,
          }));
        } catch (error) {
          console.error("Error:", error);
        }
      }
    };

    return {
      features,
      target,
      score,
      dataset,
      modelData,
      handleFileUpload,
      trainModel,
    };
  },
});
</script>
