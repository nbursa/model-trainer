<template>
  <div class="max-w-2xl mx-auto p-4 pb-24 font-light">
    <h1 class="text-4xl font-bold mb-6 py-6 text-center">Model Trainer</h1>
    <form @submit.prevent="trainModel" class="space-y-6">
      <div class="text-gray-400 mb-4">
        <p class="mb-2">Follow these steps to train your model:</p>
        <ol class="list-decimal list-inside">
          <li>Select a dataset file (CSV format).</li>
          <li>Enter the feature columns (comma-separated).</li>
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

      <!-- Features List -->
      <div v-if="featuresList.length" class="mt-4">
        <h3 class="text-md font-medium text-gray-400 mb-2">Features:</h3>
        <ul class="list-disc list-inside text-gray-200">
          <li v-for="feature in featuresList" :key="feature">{{ feature }}</li>
        </ul>
      </div>

      <!-- Feature Selection -->
      <div>
        <label
          for="features"
          class="block text-sm font-medium text-gray-400 mb-2"
          >Features</label
        >
        <input
          v-model="features"
          type="text"
          id="features"
          placeholder="e.g., x1, x2, x3"
          class="block w-full px-3 py-2 border border-gray-900 bg-gray-950 rounded-md shadow-sm sm:text-sm"
        />
      </div>

      <!-- Target Selection -->
      <div>
        <label for="target" class="block text-sm font-medium text-gray-400 mb-2"
          >Target</label
        >
        <input
          v-model="target"
          type="text"
          id="target"
          placeholder="e.g., y"
          class="block w-full px-3 py-2 border border-gray-900 bg-gray-950 rounded-md shadow-sm sm:text-sm"
        />
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
          placeholder="e.g., 2"
          class="block w-full px-3 py-2 border border-gray-900 bg-gray-950 rounded-md shadow-sm sm:text-sm"
        />
      </div>

      <!-- Train Button -->
      <button
        type="submit"
        class="w-full bg-blue-500 text-white font-light text-sm px-4 py-2 rounded-md shadow hover:bg-blue-600"
        :disabled="loading"
      >
        <span v-if="!loading">Train Model</span>
        <span v-else>Loading...</span>
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
import axios from 'axios'

export default defineComponent({
  name: 'ModelTrainer',
  setup() {
    const features = ref('')
    const target = ref('')
    const modelType = ref('LinearRegression')
    const polyDegree = ref(1)
    const score = ref<number | null>(null)
    const adjustedR2 = ref<number | null>(null)
    const mae = ref<number | null>(null)
    const mse = ref<number | null>(null)
    const rmse = ref<number | null>(null)
    const dataset = ref<File | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)
    const featuresList = ref<string[]>([])

    const handleFileUpload = (event: Event) => {
      const input = event.target as HTMLInputElement
      if (input.files) dataset.value = input.files[0]
    }

    const showFeatures = async () => {
      if (dataset.value) {
        const formData = new FormData()
        formData.append('dataset', dataset.value)
        try {
          const response = await axios.post(
            '/api/models/show_features',
            formData
          )
          featuresList.value = response.data.features
        } catch (err) {
          error.value = 'Failed to load features'
        }
      }
    }

    const trainModel = async () => {
      if (!dataset.value) return
      loading.value = true
      const formData = new FormData()
      formData.append('dataset', dataset.value)
      formData.append('features', features.value)
      formData.append('target', target.value)
      formData.append('model_type', modelType.value)
      formData.append('poly_degree', polyDegree.value.toString())

      try {
        const response = await axios.post('/api/models/train', formData)
        score.value = response.data.score
        adjustedR2.value = response.data.adjusted_r2
        mae.value = response.data.mae
        mse.value = response.data.mse
        rmse.value = response.data.rmse
      } catch (err) {
        error.value = 'Error training model'
      } finally {
        loading.value = false
      }
    }

    return {
      features,
      target,
      modelType,
      polyDegree,
      score,
      adjustedR2,
      mae,
      mse,
      rmse,
      dataset,
      loading,
      error,
      featuresList,
      handleFileUpload,
      showFeatures,
      trainModel,
    }
  },
})
</script>
