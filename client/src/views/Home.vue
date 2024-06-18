<template>
  <div class="max-w-2xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6 text-center">Model Builder</h1>
    <form @submit.prevent="trainModel" class="space-y-6">
      <div class="flex items-center justify-center">
        <div class="text-sm text-gray-400 w-fit ml-1/2 mb-4">
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
        <label
          for="dataset"
          class="block text-sm font-medium text-gray-400 mb-2"
          >Dataset</label
        >
        <div
          class="relative w-full h-16 border border-gray-900 rounded-md flex items-center justify-center px-3 py-2 bg-blue-500 hover:bg-blue-600 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        >
          <input
            type="file"
            id="dataset"
            @change="handleFileUpload"
            class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <span v-if="!dataset" class="text-white">Click to select a file</span>
          <span v-else class="text-gray-700">{{ dataset.name }}</span>
        </div>
      </div>
      <div>
        <label
          for="features"
          class="block text-sm font-medium text-gray-400 mb-2"
          >Features</label
        >
        <input
          type="text"
          id="features"
          v-model="features"
          class="block w-full px-3 py-2 border border-gray-900 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., x1, x2, x3"
        />
      </div>
      <div>
        <label for="target" class="block text-sm font-medium text-gray-400 mb-2"
          >Target</label
        >
        <input
          type="text"
          id="target"
          v-model="target"
          class="block w-full px-3 py-2 border border-gray-900 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., y"
        />
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 text-white text-sm px-4 py-2 rounded-md shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :disabled="loading"
      >
        <span v-if="!loading">Train Model</span>
        <span v-else>Loading...</span>
      </button>
    </form>
    <div v-if="score !== null" class="mt-6 text-center">
      <h2 class="text-xl font-bold">Model Score: {{ score }}</h2>
    </div>
    <chart-component
      v-if="modelData.length > 0"
      :data="modelData"
      class="mt-6"
    ></chart-component>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import ChartComponent from '../components/ChartComponent.vue'
import { ModelData } from '../types'

export default defineComponent({
  name: 'Home',
  components: {
    ChartComponent,
  },
  setup() {
    const features = ref('')
    const target = ref('')
    const score = ref<number | null>(null)
    const dataset = ref<File | null>(null)
    const modelData = ref<ModelData[]>([])
    const loading = ref(false)

    const handleFileUpload = (event: Event) => {
      const input = event.target as HTMLInputElement
      if (input.files && input.files.length > 0) {
        dataset.value = input.files[0]
      }
    }

    const trainModel = async () => {
      if (dataset.value) {
        loading.value = true
        const formData = new FormData()
        formData.append('dataset', dataset.value)
        formData.append('features', features.value)
        formData.append('target', target.value)

        try {
          const response = await axios.post(`/api/models/train`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          score.value = response.data.score
          modelData.value = response.data.data.map((row: any) => ({
            x: row[features.value],
            y: row[target.value],
            predicted: row.predicted,
          }))
        } catch (error) {
          console.error('Error:', error)
        } finally {
          loading.value = false
        }
      }
    }

    return {
      features,
      target,
      score,
      dataset,
      modelData,
      loading,
      handleFileUpload,
      trainModel,
    }
  },
})
</script>
