<template>
  <div>
    <h1>天花板地板線</h1>
    <form>
      <label for="stockSymbol"> 股票代號：</label>
      <input id="stockSymbol" v-model="stockSymbol" placeholder="例: 2330" />

      <label> 歷史資料起始日期:</label>
      <input type="date" id="start_date" v-model="start_date" />

      <label for="MA"> MA長度:</label>
      <input type="number" id="MA" v-model="MA" placeholder="輸入MA長度" />

      <label for="MA_type"> MA類型:</label>
      <select id="MA_type" v-model="MA_type">
        <option value="SMA">SMA</option>
        <option value="WMA">WMA</option>
      </select>

      <label for="method_type"> 計算方法:</label>
      <select id="method_type" v-model="method_type">
        <option value="1">方法一</option>
        <option value="2">方法二</option>
        <option value="3">方法三</option>
      </select>

      <button @click.prevent="renderCharts(data)">搜尋</button>
    </form>

    <Wait v-show="isLoading" />
    <div class="chart_container" v-show="!isLoading">
      <div id="method_1" v-show="method_type === '1'"></div>
      <div id="method_2" v-show="method_type === '2'"></div>
      <div id="method_3" v-show="method_type === '3'"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Highcharts from '@/utils/highcharts-setup'

const stockSymbol = ref('2330')
const start_date = ref('2024-01-01')
const MA = ref(5)
const MA_type = ref('SMA')
const method_type = ref('1')
const isLoading = ref(false)

const fetchChartData = async () => {
  isLoading.value = true
  try {
    const response = await axios.get(
      `/day3/api/ceiling-floor/${stockSymbol.value}/${start_date.value}/${MA.value}/${MA_type.value}/${method_type.value}`,
    )
    isLoading.value = false
    return response.data
  } catch (error) {
    isLoading.value = false
    console.error('Error fetching chart data:', error)
    return null
  }
}
function combineDateValue(dates, values) {
  return values.map((val, index) => [
    new Date(dates[index]).getTime(), // 轉成毫秒時間戳
    val,
  ])
}
const renderCharts = async () => {
  const data = await fetchChartData()
  const dates = generateDates(start_date.value, data.MA.length)
  if (!data) return

  const chartId = `method_${method_type.value}`
  console.log('data:', data)

  // 格式化交易量數據
  const volumeData = data.volume.map((volume, index) => ({
    x: new Date(dates[index]).getTime(),
    y: volume,
    color:
      volume >
      (2 * data.volume.slice(Math.max(0, index - 20), index).reduce((sum, v) => sum + v, 0)) / 20
        ? 'red'
        : 'gray', // 判斷是否符合條件
  }))

  const formatOHLCData = (ohlc, dates) => {
    const length = ohlc.Close.length // 假設 Close、High、Low 和 Open 長度一致
    const formattedData = []
    for (let i = 0; i < length; i++) {
      const timestamp = new Date(dates[i]).getTime()
      formattedData.push([
        timestamp, // X 軸索引（日期）
        ohlc.Open[i],
        ohlc.High[i],
        ohlc.Low[i],
        ohlc.Close[i],
      ])
    }
    return formattedData
  }

  const generateFlagData = (flags, dates, label) => {
    return flags
      .map((flag, index) => {
        if (flag === 1) {
          return {
            x: index,
            title: label,
            text: `Date: ${dates[index]}`,
          }
        }
        return null
      })
      .filter((point) => point !== null)
  }

  const seriesData = [
    {
      type: 'candlestick',
      name: 'Stock Price',
      data: formatOHLCData(data.candle_data, dates),
      upColor: 'red',
      color: 'green',
      upLineColor: 'red',
      lineColor: 'green',
    },
    {
      name: 'Floor',
      data: combineDateValue(dates, data.floor),
      type: 'line',
    },
    {
      name: 'Ceiling',
      data: combineDateValue(dates, data.ceiling),
      type: 'line',
    },
    {
      name: 'MA',
      data: combineDateValue(dates, data.MA),
      type: 'line',
    },
  ]

  // 僅在 method_type 為 '3' 時，才加入這些 series
  if (method_type.value === '3') {
    seriesData.push(
      {
        name: 'Ceiling 99%',
        data: combineDateValue(dates, data.ceiling_99),
        dashStyle: 'Dash',
        type: 'line',
      },
      {
        name: 'Floor 1%',
        data: combineDateValue(dates, data.floor_1),
        dashStyle: 'Dash',
        type: 'line',
      },
      {
        name: 'Volume',
        type: 'column',
        data: volumeData, // [[timestamp, volume], [timestamp, volume], ...]
        yAxis: 1,
      },
    )
  }

  Highcharts.stockChart(chartId, {
    title: {
      text: `Method ${method_type.value}`,
    },
    xAxis: {
      type: 'datetime',
      title: {
        text: 'Date', // 這裡加入 X 軸標籤
        align: 'middle', // 標籤對齊方式 (可選)
        style: {
          fontSize: '12px',
          color: '#666',
        },
      },
    },
    yAxis: [
      {
        labels: { align: 'right' },
        height: '70%', // 蠟燭圖、線圖佔上方 70%
        resize: {
          enabled: true, // 可以拖曳調整大小
        },
        title: {
          text: 'Price',
        },
      },
      {
        labels: { align: 'right' },
        top: '75%', // 從下方 25% 處開始
        height: '25%', // 交易量佔 25%
        offset: 0,
        title: {
          text: 'Volume',
        },
      },
    ],
    accessibility: {
      description: `This is the chart for method ${method_type.value}`,
    },
    series: seriesData,
    plotOptions: {
      line: {
        dataLabels: {
          enabled: false,
        },
      },
    },
  })
}

const generateDates = (startDate, length) => {
  const dates = []
  let currentDate = new Date(startDate)
  for (let i = 0; i < length; i++) {
    dates.push(currentDate.toISOString().split('T')[0]) // 格式化為 'YYYY-MM-DD'
    currentDate.setDate(currentDate.getDate() + 1) // 每次加一天
  }
  console.log('dates:', dates)
  return dates
}
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
