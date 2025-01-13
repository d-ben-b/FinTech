import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import HighchartsVue from 'highcharts-vue'

const app = createApp(App)

app.config.globalProperties.$axios = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/'

app.use(router)
app.use(HighchartsVue)
app.mount('#app')
