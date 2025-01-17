import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import HighchartsVue from 'highcharts-vue'
import Navbar from './components/Navbar.vue'
import Wait from './components/Wait.vue'

const app = createApp(App)

app.config.globalProperties.$axios = axios
axios.defaults.baseURL = 'http://localhost:8081/'

app.use(router)
app.use(HighchartsVue)
app.component('Navbar', Navbar)
app.component('Wait', Wait)
app.mount('#app')
