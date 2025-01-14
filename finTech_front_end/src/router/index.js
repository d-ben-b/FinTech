import { createRouter, createWebHistory } from 'vue-router'
import Day1 from '@/views/Day1.vue'
import Day2 from '@/views/Day2.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Day1',
      component: Day1,
    },
    {
      path: '/day1',
      name: 'Day1',
      component: Day1,
    },
    {
      path: '/day2',
      name: 'Day2',
      component: Day2,
    },
    {
      path: '/day3',
      name: 'Day3',
      component: Day1,
    },
    {
      path: '/day4',
      name: 'Day4',
      component: Day1,
    },
    {
      path: '/day5',
      name: 'Day5',
      component: Day1,
    },
  ],
})

export default router
