<template>
  <div>
    <h1>本益比河流圖</h1>
    <form>
      <label for="stockSymbol">
        股票代號：
        <input id="stockSymbol" v-model="stockSymbol" placeholder="例: 2330" />
      </label>
      <label>
        歷史幾年資料:
        <select id="option" v-model="option">
          <option value="MONTH">月</option>
          <option value="QUAR">季</option>
          <option value="YEAR">年</option>
        </select>
      </label>
      <button @click.prevent="renderCharts">搜尋</button>
    </form>
  </div>
  <Wait v-if="isLoading" />
  <div id="chart"></div>
</template>

<script setup>
import Highcharts from '@/utils/highcharts-setup'
import axios from 'axios'
import { ref } from 'vue'
const stockSymbol = ref('2330')
const option = ref('MONTH')
let chartInstance = null
const isLoading = ref(false)
const fetchChartData = async () => {
  if (!stockSymbol.value) {
    alert('請輸入股票代號！')
    return
  }
  isLoading.value = true
  try {
    const res = await axios.get(`/day3/api/stock-analyze/${stockSymbol.value}/${option.value}`)
    isLoading.value = false
    return res.data
  } catch (error) {
    isLoading.value = false
    alert('發生錯誤，請稍後再試！')
  }

  return res.data
}
const formatOHLCData = (ohlc) => {
  return ohlc.map((item, index) => [
    index, // 用索引作為時間戳
    parseFloat(item[0]), // Open
    parseFloat(item[1]), // High
    parseFloat(item[2]), // Low
    parseFloat(item[3]), // Close
  ])
}
const renderCharts = async () => {
  const data = await fetchChartData()
  const formattedData = formatOHLCData(data.ohlc)
  Highcharts.chart('chart', {
    title: {
      text: '本益比河流圖',
    },
    xAxis: {
      categories: data.months, // 使用月份作為 X 軸
    },
    yAxis: {
      title: {
        text: '本益比',
      },
    },
    accessibility: {
      point: {
        valueDescriptionFormat: '{index}. {xDescription}, {value}.',
      },
    },
    series: [
      {
        name: 'Line 1',
        data: data.Lines.line1, // 第一條數據線
      },
      {
        name: 'Line 2',
        data: data.Lines.line2,
      },
      {
        name: 'Line 3',
        data: data.Lines.line3,
      },
      {
        name: 'Line 4',
        data: data.Lines.line4,
      },
      {
        name: 'Line 5',
        data: data.Lines.line5,
      },
      {
        name: 'Line 6',
        data: data.Lines.line6,
      },
      {
        type: 'candlestick',
        name: 'Stock Price',
        data: formattedData,
        tooltip: {
          valueDecimals: 2,
        },
      },
    ],
  })
}
</script>

<style scoped>
/* Styles for your component */
</style>
