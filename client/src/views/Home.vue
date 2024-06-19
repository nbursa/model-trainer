<template>
  <div class="max-w-2xl mx-auto p-4 pb-24 font-light">
    <h1 class="text-4xl font-bold mb-6 py-6 text-center">Welcome to Model Trainer</h1>

    <div class="mb-8">
      <p class="text-lg text-center">
        Model Trainer is a web application designed to help you create, train, and evaluate machine learning models with ease.
      </p>
    </div>

    <div class="flex flex-col items-center justify-center text-md mb-8">
      <div class="text-gray-400 mb-4">
        <div class="mb-2 text-center font-bold">Key Features:</div>
        <div class="ml-32">
          <div>User authentication and project management</div>
          <div>Dataset upload and preprocessing tools</div>
          <div>Selection and configuration of various machine learning models</div>
          <div>Evaluation of model performance metrics</div>
          <div>Visualization of model predictions</div>
          <div>Export of trained models for deployment</div>
        </div>
      </div>
    </div>

    <div class="flex flex-col items-center justify-center text-sm mb-8">
      <div class="text-gray-400 mb-4 ml-24">
        <p class="mb-2 font-bold">Follow these steps to get started:</p>
        <ol class="list-decimal list-inside">
          <li>Select a dataset file in CSV format.</li>
          <li>Enter the feature columns (comma-separated).</li>
          <li>Specify the target column.</li>
          <li>Choose a regression model type.</li>
          <li>(Optional) Enter the polynomial degree for regression models.</li>
          <li>Click "Train Model" to initiate model training.</li>
        </ol>
      </div>
    </div>

    <div class="text-center">
      <router-link to="/train" class="text-blue-500 hover:underline">Get Started</router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomePage',
});
</script>
