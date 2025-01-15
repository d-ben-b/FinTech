<template>
  <div class="container">
    <h1>股票定價結果</h1>

    <!-- 搜索條件 -->
    <form class="form">
      <label>股票代號:</label>
      <input v-model="stockSymbol" placeholder="例: 2330" />

      <label>歷史幾年資料:</label>
      <input v-model="n_months" type="number" placeholder="例: 10" />

      <button @click.prevent="fetchStockData">搜尋</button>
    </form>

    <!-- 加載中 -->
    <Wait v-if="isLoading" />

    <!-- 最新價格 -->
    <div v-if="latestPrice !== null" class="latest-price">
      <h2>最新價格: {{ latestPrice }}</h2>
    </div>

    <!-- 定價結果圖表 -->
    <div id="bar-chart" v-show="!isLoading"></div>

    <!-- 錯誤訊息 -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Highcharts from '@/utils/highcharts-setup'
import Wait from '@/components/Wait.vue'

export default {
  name: 'StockChart',
  setup() {
    const stockSymbol = ref(2330)
    const n_months = ref(10)
    const latestPrice = ref(null)
    const error = ref(null)
    var data = ref(null)
    var isLoading = ref(false)
    var max_data = 0
    var line_data = 0

    const fetchStockData = async () => {
      error.value = null
      isLoading.value = true
      latestPrice.value = null

      try {
        const response = await axios.get(
          `/day2/api/stock-performance/${stockSymbol.value}/${n_months.value}`,
        )
        data = response.data
      } catch (error) {
        console.error('Failed to fetch stock performance:', error)
        error.value = 'Failed to fetch stock performance'
      }
      // 模擬最新價格
      latestPrice.value = data.price

      max_data = Math.max(
        data.PER.high,
        data.high_low.high,
        data.PBR.high,
        data.dividend.high,
        data.price,
      )
      line_data = (data.price / max_data) * 100

      // 更新圖表資料
      Highcharts.chart('bar-chart', {
        chart: {
          type: 'bar',
        },
        title: {
          text: '股票定價結果',
        },
        xAxis: {
          categories: ['本益比法', '高低價法', '本淨比法', '股利法'],
          title: {
            text: null,
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: '百分比',
            align: 'high',
          },
          labels: {
            overflow: 'justify',
          },
        },
        tooltip: {
          valueSuffix: ' 元',
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true,
            },
            stacking: 'percent',
          },
        },
        legend: {
          reversed: true,
        },
        series: [
          {
            name: '最高價',
            data: [max_data, max_data, max_data, max_data],
            color: 'darkred',
          },
          {
            name: '昂貴價格區間',
            data: [data.PER.high, data.high_low.high, data.PBR.high, data.dividend.high],
            color: 'red',
          },
          {
            name: '合理價格區間',
            data: [data.PER.avg, data.high_low.avg, data.PBR.avg, data.dividend.avg],
            color: 'yellow',
          },
          {
            name: '便宜價格區間',
            data: [data.PER.low, data.high_low.low, data.PBR.low, data.dividend.low],
            color: 'green',
          },
          {
            name: '現價',
            type: 'line',
            data: [
              [0, line_data],
              [1, line_data],
              [2, line_data],
              [3, line_data],
            ],
            color: 'blue',
            marker: {
              enabled: false,
            },
            lineWidth: 4,
          },
        ],
      })
      isLoading.value = false
    }

    return {
      stockSymbol,
      n_months,
      latestPrice,
      fetchStockData,
      isLoading,
      error,
    }
  },
}
</script>

<style>
.container {
  width: 80%;
  margin: 0 auto;
}

.loading p {
  font-size: 1.2em;
  color: #ff6600;
  margin-top: 20px;
}

.latest-price {
  margin: 20px 0;
  font-size: 1.5em;
  color: #28a745;
}

#error {
  color: red;
  margin-top: 20px;
}
</style>
