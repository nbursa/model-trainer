<template>
  <div
    class="min-h-screen flex flex-col justify-center items-center p-4 font-light"
  >
    <h1 class="text-5xl font-serif font-bold mb-6 py-6 text-center">
      Welcome to Model Trainer
    </h1>

    <div class="mb-8 text-lg text-center max-w-2xl">
      <p>
        Model Trainer is a web application designed to help you create, train,
        and evaluate machine learning models with ease.
      </p>
    </div>

    <div class="text-md mb-8 text-gray-400 text-center">
      <div class="mb-2 font-bold">Key Features:</div>
      <div class="space-y-1">
        <div>User authentication and project management</div>
        <div>Dataset upload and preprocessing tools</div>
        <div>
          Selection and configuration of various machine learning models
        </div>
        <div>Evaluation of model performance metrics</div>
        <div>Visualization of model predictions</div>
        <div>Export of trained models for deployment</div>
      </div>
    </div>

    <router-link
      to="/train"
      class="px-6 py-3 text-white text-lg font-semibold rounded-lg shadow-lg bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 transition-all duration-300"
    >
      Get Started
    </router-link>
  </div>
</template>
