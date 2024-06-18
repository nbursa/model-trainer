<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">ML Model Builder</h1>
    <form @submit.prevent="trainModel">
      <div class="mb-4">
        <label for="dataset" class="block text-sm font-medium text-gray-700"
          >Dataset</label
        >
        <input type="file" id="dataset" @change="handleFileUpload" />
      </div>
      <div class="mb-4">
        <label for="features" class="block text-sm font-medium text-gray-700"
          >Features</label
        >
        <input type="text" id="features" v-model="features" />
      </div>
      <div class="mb-4">
        <label for="target" class="block text-sm font-medium text-gray-700"
          >Target</label
        >
        <input type="text" id="target" v-model="target" />
      </div>
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
        Train Model
      </button>
    </form>
    <div v-if="score !== null" class="mt-4">
      <h2 class="text-xl font-bold">Model Score: {{ score }}</h2>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Home",
  setup() {
    const features = ref("");
    const target = ref("");
    const score = ref<number | null>(null);
    const dataset = ref<File | null>(null);

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

        const response = await axios.post(
          "http://localhost:5000/api/models/train",
          {
            dataset: formData,
            features: features.value.split(","),
            target: target.value,
          },
        );

        score.value = response.data.score;
      }
    };

    return {
      features,
      target,
      score,
      handleFileUpload,
      trainModel,
    };
  },
});
</script>
