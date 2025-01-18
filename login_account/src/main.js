import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'

const BaseURL = 'http://localhost:8001/login_manager/'
axios.defaults.baseURL = BaseURL
axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
axios.defaults.withCredentials = true

const app = createApp(App)
app.use(router)
app.mount('#app')
