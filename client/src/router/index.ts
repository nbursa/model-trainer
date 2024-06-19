import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ModelTrainer from '../views/ModelTrainer.vue'
import Contact from '../views/Contact.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/train',
    name: 'ModelTrainer',
    component: ModelTrainer,
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
