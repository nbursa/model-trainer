<template>
  <NavComponent class="fixed top-0 left-0 right-0" />
  <router-view  class="pt-[60px]"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import NavComponent from './components/Navigation.vue'

export default defineComponent({
  name: 'App',
  components: { NavComponent },
})
</script>
