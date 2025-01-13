import { createRouter, createWebHistory } from 'vue-router'
import Day1 from '@/views/Day1.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/day1',
      name: 'Day1',
      component: Day1,
    },
  ],
})

export default router
