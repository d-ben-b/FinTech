<template>
  <div>
    <h1>本益比河流圖</h1>
    <form>
      <label for="stockSymbol">股票代號：</label>

      <input id="stockSymbol" v-model="stockSymbol" placeholder="例: 2330" />

      <label> 歷史幾年資料:</label>
      <select id="option" v-model="option">
        <option value="MONTH">月</option>
        <option value="QUAR">季</option>
        <option value="YEAR">年</option>
      </select>

      <label for="time"> 時間區段:</label>
      <input type="number" id="time" v-model="time" placeholder="輸入時間區段" />

      <button @click.prevent="renderCharts">搜尋</button>
    </form>

    <Wait v-show="isLoading" />
    <div class="chart_container" v-show="!isLoading">
      <div id="chart"></div>
      <div id="price_chart"></div>
    </div>
  </div>
</template>

<script setup>
import Highcharts from '@/utils/highcharts-setup'
import axios from 'axios'
import { ref } from 'vue'
const stockSymbol = ref('2330')
const option = ref('MONTH')
const isLoading = ref(false)
const time = ref(5)
const fetchChartData = async () => {
  console.log('Fetching data...')
  if (!stockSymbol.value) {
    alert('請輸入股票代號！')
    return
  }
  isLoading.value = true
  try {
    const res = await axios.get(
      `/day3/api/stock-analyze/${stockSymbol.value}/${option.value}/${time.value}`,
    )

    console.log('DATA:', res.data)
    isLoading.value = false
    return res.data
  } catch (error) {
    isLoading.value = false
    console.error('ERROR:', error)
    alert('發生錯誤，請稍後再試！')
  }
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
  Highcharts.stockChart('chart', {
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
    marker: {
      enabled: false,
    },
    series: [
      {
        name: data.amg[5],
        data: data.Lines.line1,
        color: 'red', // 對應圖中 27X 的顏色
      },
      {
        name: data.amg[4],
        data: data.Lines.line2,
        color: 'blue', // 對應圖中 24.6X 的顏色
      },
      {
        name: data.amg[3],
        data: data.Lines.line3,
        color: 'orange', // 對應圖中 22.2X 的顏色
      },
      {
        name: data.amg[2],
        data: data.Lines.line4,
        color: 'green', // 對應圖中 19.8X 的顏色
      },
      {
        name: data.amg[1],
        data: data.Lines.line5,
        color: 'black', // 對應圖中 17.4X 的顏色
      },
      {
        name: data.amg[0],
        data: data.Lines.line6,
        color: 'cyan', // 對應圖中 15X 的顏色
      },
      {
        type: 'candlestick',
        name: 'Stock Price',
        data: formattedData,
        tooltip: {
          valueDecimals: 2,
        },
        upColor: 'red',
        color: 'green',
        upLineColor: 'red',
        lineColor: 'green',
      },
    ],
  })
  Highcharts.stockChart('price_chart', {
    chart: {
      type: 'bar',
    },
    title: {
      text: '價格區間顯示',
    },
    xAxis: {
      categories: data.months, // 使用月份作為 X 軸
    },
    yAxis: {
      title: {
        text: '價格',
      },
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
        },
        stacking: 'overlap',
      },
    },
    series: [
      {
        name: '最高價',
        data: [data.max_price],
        color: 'darkred',
      },
      {
        name: '昂貴價格區間',
        data: [data.high_price],
        color: 'red',
      },
      {
        name: '合理價格區間',
        data: [data.avg_price],
        color: 'yellow',
      },
      {
        name: '便宜價格區間',
        data: [data.low_price],
        color: 'green',
      },
      {
        name: '現價',
        type: 'line',
        data: [[0, data.now_price]],
        color: 'blue',
        marker: {
          enabled: true,
        },
        lineWidth: 4,
      },
    ],
  })
}
</script>

<style scoped>
.container {
  width: 80%;
  margin: 0 auto;
}
</style>
