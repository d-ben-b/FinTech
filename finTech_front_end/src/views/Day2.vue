<template>
  <div>
    <h1>股票分析</h1>
    <div>
      <label>股票代號：</label>
      <input v-model="stockId" placeholder="輸入股票代碼" />
      <label>月份：</label>
      <input v-model="n_months" type="number" placeholder="輸入月份" />
      <button @click="fetchStockPerformance">搜尋</button>
    </div>
    <div v-if="stockData">
      <h2>股票數據</h2>
      <table>
        <thead>
          <tr>
            <th v-for="header in stockData.headers" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in stockData.data" :key="index">
            <td v-for="col in row" :key="col">{{ col }}</td>
          </tr>
        </tbody>
      </table>
      <highcharts :options="chartOptions"></highcharts>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// 高charts相關
import Highcharts from 'highcharts'

const stockId = ref('')
const stockData = ref(null)
const error = ref(null)
const n_months = ref(10)

// 圖表配置
const chartOptions = ref({
  chart: { type: 'bar' },
  title: { text: '股票分析圖表' },
  xAxis: { categories: [] },
  yAxis: {
    title: { text: '數值' },
  },
  series: [{ name: '數據分析', data: [] }],
})

// 獲取數據函數
const fetchStockPerformance = async () => {
  error.value = null
  stockData.value = null

  try {
    const response = await axios.get(
      `/day2/api/stock-performance/${stockId.value}/${n_months.value}`,
    )
    console.log('Stock performance:', response.data)
    stockData.value = response.data

    // 更新圖表
    chartOptions.value.xAxis.categories = stockData.value.headers.slice(1) // 忽略第一列 (年度)
    chartOptions.value.series[0].data = stockData.value.data.map((row) => parseFloat(row[1]) || 0) // 假設抓取第 2 列的數值
  } catch (err) {
    console.error('Error fetching stock performance:', err)
    error.value = err.response?.data?.error || '無法取得股票數據！'
  }
}
</script>

<style>
.error {
  color: red;
  font-weight: bold;
}
</style>
