<template>
  <nav class="px-4 py-2 bg-[#242424] drop-shadow-xl">
    <div class="mx-auto flex justify-between items-center">
      <div>
        <router-link to="/" class="text-xl font-bold">ML Model Trainer</router-link>
      </div>
      <div class="hidden md:block">
        <router-link to="/" class="mx-4">Home</router-link>
        <router-link to="/train" class="mx-4">Train</router-link>
        <router-link to="/contact" class="mx-4">Contact</router-link>
      </div>
      <div class="md:hidden">
        <button @click="isOpen = !isOpen" class="text-white bg-white/10 p-2 rounded-full hover:bg-white/20">
          <svg class="h-6 w-6" :class="{'hidden': isOpen, 'block': !isOpen}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
          <svg class="h-6 w-6" :class="{'block': isOpen, 'hidden': !isOpen}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>
    <div class="md:hidden h-screen w-screen flex items-center justify-center z-40" v-show="isOpen">
      <div class="flex flex-col justify-start items-start">
        <router-link to="/" class="block text-white p-2">Home</router-link>
        <router-link to="/train" class="block text-white p-2">Train</router-link>
        <router-link to="/contact" class="block text-white p-2">Contact</router-link>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'NavComponent',
  setup() {
    const isOpen = ref(false);

    return { isOpen };
  }
})
</script>
