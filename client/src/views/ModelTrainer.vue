<template>
  <div class="max-w-2xl mx-auto p-4 pb-24 font-light">
    <h1 class="text-4xl font-bold mb-6 py-6 text-center">Model Trainer</h1>
    <form @submit.prevent="trainModel" class="space-y-6">
      <div class="text-gray-400 mb-4">
        <p class="mb-2">Follow these steps to train your model:</p>
        <ol class="list-decimal list-inside">
          <li>Select a dataset file (CSV format).</li>
          <li>Select feature columns from the list.</li>
          <li>Enter the target column.</li>
          <li>Select the regression model.</li>
          <li>Enter polynomial degree (optional).</li>
          <li>Click "Train Model" to train the model.</li>
        </ol>
      </div>

      <!-- Upload Dataset -->
      <div>
        <label for="dataset" class="block font-medium text-gray-400 mb-2"
          >Dataset</label
        >
        <div class="flex items-center justify-between gap-2">
          <div
            class="relative w-full border border-gray-900 rounded-md px-3 py-2 bg-blue-500 hover:bg-blue-600 text-sm cursor-pointer"
          >
            <input
              type="file"
              id="dataset"
              @change="handleFileUpload"
              class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <span v-if="!dataset" class="text-white"
              >Click to select a file</span
            >
            <span v-else class="text-yellow-50">{{ dataset.name }}</span>
          </div>
          <button
            v-if="dataset"
            @click.prevent="showFeatures"
            class="border border-gray-900 rounded-md px-3 py-2 bg-blue-500 hover:bg-blue-600"
          >
            <i class="fas fa-eye"></i> Features
          </button>
        </div>
      </div>

      <!-- Features Selection (Checkbox) -->
      <div v-if="featuresList.length" class="mt-4">
        <h3 class="text-md font-medium text-gray-400 mb-2">Select Features:</h3>
        <div class="grid grid-cols-2 gap-2">
          <label
            v-for="feature in featuresList"
            :key="feature"
            class="flex items-center space-x-2 text-gray-300"
          >
            <input
              type="checkbox"
              v-model="selectedFeatures"
              :value="feature"
              class="form-checkbox text-blue-500"
            />
            <span>{{ feature }}</span>
          </label>
        </div>
      </div>

      <!-- Target Selection -->
      <div>
        <label for="target" class="block text-sm font-medium text-gray-400 mb-2"
          >Target Column</label
        >
        <select
          v-model="target"
          id="target"
          class="block w-full px-3 py-2 border border-gray-900 bg-gray-950 rounded-md shadow-sm"
        >
          <option
            v-for="feature in featuresList"
            :key="feature"
            :value="feature"
          >
            {{ feature }}
          </option>
        </select>
      </div>

      <!-- Regression Model -->
      <div>
        <label
          for="modelType"
          class="block text-sm font-medium text-gray-400 mb-2"
          >Regression Model</label
        >
        <select
          v-model="modelType"
          id="modelType"
          class="block w-full px-3 py-2 border border-gray-900 bg-gray-950 rounded-md shadow-sm"
        >
          <option value="LinearRegression">Linear Regression</option>
          <option value="Ridge">Ridge Regression</option>
          <option value="Lasso">Lasso Regression</option>
          <option value="ElasticNet">ElasticNet</option>
          <option value="RandomForest">Random Forest</option>
          <option value="GradientBoosting">Gradient Boosting</option>
        </select>
      </div>

      <!-- Polynomial Degree -->
      <div>
        <label
          for="polyDegree"
          class="block text-sm font-medium text-gray-400 mb-2"
          >Polynomial Degree</label
        >
        <input
          v-model="polyDegree"
          type="number"
          id="polyDegree"
          min="1"
          placeholder="e.g., 2"
          class="block w-full px-3 py-2 border border-gray-900 bg-gray-950 rounded-md shadow-sm sm:text-sm"
        />
      </div>

      <!-- Train Button -->
      <button
        type="submit"
        class="w-full bg-blue-500 text-white font-light text-sm px-4 py-2 rounded-md shadow hover:bg-blue-600 flex justify-center items-center"
        :disabled="loading"
      >
        <span v-if="!loading">Train Model</span>
        <span v-else class="flex items-center">
          <svg class="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24">
            <circle
              cx="12"
              cy="12"
              r="10"
              fill="none"
              stroke="white"
              stroke-width="4"
            />
          </svg>
          Training...
        </span>
      </button>
    </form>

    <!-- Display Training Results -->
    <div v-if="error" class="mt-4 text-red-600 text-center">{{ error }}</div>
    <div v-if="score !== null" class="mt-6">
      <h2 class="text-xl font-bold text-center mb-4">Model Metrics</h2>
      <p>
        R² Score: <span class="font-semibold">{{ score }}</span>
      </p>
      <p>
        Adjusted R²: <span class="font-semibold">{{ adjustedR2 }}</span>
      </p>
      <p>
        MAE: <span class="font-semibold">{{ mae }}</span>
      </p>
      <p>
        MSE: <span class="font-semibold">{{ mse }}</span>
      </p>
      <p>
        RMSE: <span class="font-semibold">{{ rmse }}</span>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios, { AxiosError } from 'axios'

export default defineComponent({
  name: 'ModelTrainer',
  setup() {
    const dataset = ref<File | null>(null)
    const featuresList = ref<string[]>([])
    const selectedFeatures = ref<string[]>([])
    const target = ref('')
    const modelType = ref('LinearRegression')
    const polyDegree = ref(1)
    const loading = ref(false)
    const error = ref<string | null>(null)
    const score = ref<number | null>(null)
    const adjustedR2 = ref<number | null>(null)
    const mae = ref<number | null>(null)
    const mse = ref<number | null>(null)
    const rmse = ref<number | null>(null)

    const handleFileUpload = (event: Event) => {
      const input = event.target as HTMLInputElement
      if (input.files) dataset.value = input.files[0]
    }

    const showFeatures = async () => {
      if (!dataset.value) return
      const formData = new FormData()
      formData.append('dataset', dataset.value)
      try {
        const response = await axios.post('/api/models/show_features', formData)
        featuresList.value = response.data.features
      } catch (err) {
        const axiosError = err as AxiosError<{ error: string }>
        error.value =
          axiosError.response?.data?.error || 'Failed to load features'
      }
    }

    const trainModel = async () => {
      if (
        !dataset.value ||
        selectedFeatures.value.length === 0 ||
        !target.value
      ) {
        error.value =
          'Please upload a dataset, select features, and choose a target column.'
        return
      }

      loading.value = true
      const formData = new FormData()
      formData.append('dataset', dataset.value)
      formData.append('features', selectedFeatures.value.join(','))
      formData.append('target', target.value)
      formData.append('model_type', modelType.value)
      formData.append('poly_degree', polyDegree.value.toString())

      try {
        const response = await axios.post('/api/models/train', formData)
        ;({
          score: score.value,
          adjusted_r2: adjustedR2.value,
          mae: mae.value,
          mse: mse.value,
          rmse: rmse.value,
        } = response.data)
      } catch (err) {
        const axiosError = err as AxiosError<{ error: string }>
        error.value = axiosError.response?.data?.error || 'Error training model'
      } finally {
        loading.value = false
      }
    }

    return {
      dataset,
      featuresList,
      selectedFeatures,
      target,
      modelType,
      polyDegree,
      loading,
      error,
      score,
      adjustedR2,
      mae,
      mse,
      rmse,
      handleFileUpload,
      showFeatures,
      trainModel,
    }
  },
})
</script>
