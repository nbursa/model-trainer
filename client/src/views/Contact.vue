<template>
  <div class="max-w-2xl mx-auto p-4 pb-24 font-light">
    <h1 class="text-4xl font-bold mb-6 py-6 text-center">Contact</h1>

    <div class="mb-8">
      <p class="text-sm text-center">
        Ready to transform your data into powerful insights? Start training your model today and unlock the potential of your datasets! Dive into smarter decision-making with our intuitive ML Dashboard. Get started now!
      </p>
    </div>

    <div>
      <ContactForm />
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ContactForm from '../components/ContactForm.vue';

export default defineComponent({
  name: 'ContactPage',
  components: { ContactForm }
});
</script>
