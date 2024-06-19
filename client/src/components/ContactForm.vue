<template>
  <div class="max-w-2xl mx-auto p-4 pb-24 font-light">
    <h1 class="text-4xl font-bold mb-6 py-6 text-center">Contact</h1>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-400">Name <span class="text-red-500">*</span></label>
        <input v-model="form.name" type="text" id="name" name="name" required
               class="block w-full px-3 py-2 border border-gray-900 !bg-gray-950 rounded-md shadow-sm focus:outline-none sm:text-sm">
      </div>

      <div>
        <label for="email" class="block text-sm font-medium text-gray-400">Email address <span class="text-red-500">*</span></label>
        <input v-model="form.email" type="email" id="email" name="email" required
               class="block w-full px-3 py-2 border border-gray-900 !bg-gray-950 rounded-md shadow-sm focus:outline-none sm:text-sm">
      </div>

      <div>
        <label for="message" class="block text-sm font-medium text-gray-400">Message <span class="text-red-500">*</span></label>
        <textarea v-model="form.message" id="message" name="message" rows="4" required
                  class="block w-full px-3 py-2 border border-gray-900 !bg-gray-950 rounded-md shadow-sm focus:outline-none sm:text-sm"></textarea>
      </div>

      <div>
        <button type="submit" :disabled="!formValid"
                class="w-full bg-blue-500 text-white font-light text-sm px-4 py-2 rounded-md shadow hover:bg-blue-600 focus:outline-none">
          Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'ContactForm',
  setup() {
    const form = ref({
      name: '',
      email: '',
      message: ''
    });

    const formValid = computed(() => {
      return form.value.name && form.value.email && form.value.message;
    });

    const submitForm = async () => {
      console.log('Form submitted with:', form.value);

      try {
        const response = await axios.post(`/api/email/send-email`, form.value, {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        console.log(response.data); // Handle response data as needed
        form.value.name = '';
        form.value.email = '';
        form.value.message = '';
      } catch (error) {
        console.error('Error:', error);
      }
    };

    return {
      form,
      formValid,
      submitForm
    };
  }
});
</script>
