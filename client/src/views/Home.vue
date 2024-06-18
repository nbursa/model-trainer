<template>
  <div class="max-w-2xl mx-auto p-4 pb-24 font-light">
    <h1 class="text-4xl font-bold mb-6 py-6 text-center">Model Trainer</h1>
    <form @submit.prevent="trainModel" class="space-y-6">
      <div class="flex flex-col items-center justify-center text-sm">
        <div class="text-gray-400 mb-4">
          <p class="mb-2">Follow these steps to train your model:</p>
          <ol class="list-decimal list-inside">
            <li>Select a dataset file (CSV format).</li>
            <li>Enter the feature columns (comma-separated).</li>
            <li>Enter the target column.</li>
            <li>Click "Train Model" to train the model.</li>
          </ol>
        </div>
      </div>
      <div>
        <label for="dataset" class="block text-sm font-medium text-gray-400 mb-2">Dataset</label>
        <div class="relative w-full h-16 border border-gray-900 rounded-md flex items-center justify-center px-3 py-2 bg-blue-500 hover:bg-blue-600 shadow-sm focus:outline-none active:text-yellow-100 text-sm">
          <input type="file" id="dataset" @change="handleFileUpload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
          <span v-if="!dataset" class="text-white">Click to select a file</span>
          <span v-else class="text-yellow-50">{{ dataset.name }}</span>
        </div>
      </div>
      <div>
        <label for="features" class="block text-sm font-medium text-gray-400 mb-2">Features</label>
        <input
          type="text"
          id="features"
          v-model="features"
          class="block w-full px-3 py-2 border border-gray-900 rounded-md shadow-sm focus:outline-none sm:text-sm"
          placeholder="e.g., x1, x2, x3"
        />
      </div>
      <div>
        <label for="target" class="block text-sm font-medium text-gray-400 mb-2">Target</label>
        <input
          type="text"
          id="target"
          v-model="target"
          class="block w-full px-3 py-2 border border-gray-900 rounded-md shadow-sm focus:outline-none sm:text-sm"
          placeholder="e.g., y"
        />
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 text-white font-light text-sm px-4 py-2 rounded-md shadow hover:bg-blue-600 focus:outline-none"
        :disabled="loading"
      >
        <span v-if="!loading">Train Model</span>
        <span v-else>Loading...</span>
      </button>
    </form>
    <div v-if="error" class="mt-4 text-red-600 text-center">{{ error }}</div>
    <div v-if="score !== null" class="mt-6 text-center">
      <h2 class="text-xl font-bold">Model Score: {{ score }}</h2>
    </div>
    <div v-if="modelData.length > 0" class="mt-6">
      <label for="xFeature" class="block text-sm font-medium text-gray-400 mb-2">Select x-axis feature</label>
      <select v-model="xFeature" id="xFeature" class="block w-full px-3 py-2 border border-gray-900 rounded-md shadow-sm focus:outline-none sm:text-sm">
        <option v-for="feature in featureList" :key="feature" :value="feature">{{ feature }}</option>
      </select>
      <chart-component :data="modelData" :xFeature="xFeature" class="mt-4"></chart-component>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import axios from "axios";
import ChartComponent from "../components/ChartComponent.vue";
import { ModelData } from "../types";

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
    const loading = ref(false);
    const error = ref<string | null>(null);
    const xFeature = ref<string>("");

    const featureList = computed(() => features.value.split(',').map(f => f.trim()));

    const handleFileUpload = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files.length > 0) {
        dataset.value = input.files[0];
      }
    };

    const trainModel = async () => {
      error.value = null;
      if (dataset.value) {
        loading.value = true;
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
            x: row[featureList.value[0]], // Use the first feature for x axis by default
            y: row[target.value],
            predicted: row.predicted,
          }));
          xFeature.value = featureList.value[0];
        } catch (err) {
          if (err.response && err.response.data && err.response.data.error) {
            error.value = err.response.data.error;
          } else {
            error.value = "An unexpected error occurred.";
          }
        } finally {
          loading.value = false;
        }
      }
    };

    return {
      features,
      target,
      score,
      dataset,
      modelData,
      loading,
      error,
      xFeature,
      featureList,
      handleFileUpload,
      trainModel,
    };
  },
});
</script>
