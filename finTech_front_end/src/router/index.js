import { createRouter, createWebHistory } from 'vue-router'
import Day1 from '@/views/Day1.vue'
import Day2 from '@/views/Day2.vue'
import Day3_1 from '@/views/Day3_1.vue'
import Day3_2 from '@/views/Day3_2.vue'
import test from '@/views/test.vue'
import axios from 'axios'

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
      path: '/day3-1',
      name: 'Day3-1',
      component: Day3_1,
    },
    {
      path: '/day3-2',
      name: 'Day3-2',
      component: Day3_2,
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
    {
      path: '/test',
      name: 'Test',
      component: test,
    },
  ],
})
const queryParams = new URLSearchParams(window.location.search)
const username = queryParams.get('username')
localStorage.setItem('username', username)
router.beforeEach(async (to, from, next) => {
  console.log('username router', username)
  try {
    // 向後端發送請求，確認 Token 是否有效
    const response = await axios.post('http://localhost:8001/login_manager/check/', {
      username: username,
    })

    console.log(response.data.success)

    // Token 驗證通過，允許導航
    if (response.data.success) {
      next()
      return
    } else {
      window.location.href = 'http://localhost:5173'
    }
  } catch (error) {
    console.error('Token validation failed:', error)

    // Token 驗證失敗，重定向到登入頁面
    window.location.href = 'http://localhost:5173'
  }
})

export default router
