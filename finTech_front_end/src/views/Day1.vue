<template>
  <div class="container">
    <h1>股票分析</h1>
    <!-- User Input Form -->
    <form @submit.prevent="analyzeStock">
      <label for="stock">股票代號：</label>
      <input v-model="symbol" type="text" id="stock" placeholder="e.g., AAPL, TSLA" required />

      <label for="start_date">起始日期：</label>
      <input v-model="startDate" type="date" id="start_date" required />

      <label for="end_date">終止日期：</label>
      <input v-model="endDate" type="date" id="end_date" required />

      <button type="submit">Analyze</button>
    </form>

    <!-- Analysis Section -->
    <div v-if="error" style="margin-top: 20px">
      <p class="error">{{ error }}</p>
    </div>
    <div
      style="margin-top: 20px; display: flex; flex-direction: column; align-items: center"
      v-show="stockSymbol"
    >
      <h2>Stock: {{ stockSymbol }}</h2>
      <p>From {{ startDate }} to {{ endDate }}</p>

      <!-- Candle Chart -->
      <div id="candle-chart" style="height: 600px; margin: 50px 0"></div>

      <!-- Volume Chart -->
      <div id="volume-chart" style="height: 300px; margin: 50px 0"></div>

      <!-- Volume Table -->
      <table id="volume-table" class="display">
        <thead>
          <tr>
            <th>Date</th>
            <th>High Volume</th>
            <th>Five Day MA</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Highcharts from '@/utils/highcharts-setup'
import $ from 'jquery'
import 'datatables.net-dt'

export default {
  data() {
    return {
      symbol: 'TSLA',
      startDate: '2024-01-01',
      endDate: '2024-03-01',
      stockSymbol: '',
      error: '',
      volumeData: [],
      stockData: [],
      tableData: [],
    }
  },
  methods: {
    async analyzeStock() {
      try {
        const response = await axios.get('day1/analyze', {
          params: {
            symbol: this.symbol,
            start: this.startDate,
            end: this.endDate,
          },
        })

        const { volume_data, stock_data, table_data, stock_symbol } = response.data
        this.volumeData = volume_data
        this.stockData = stock_data
        this.tableData = table_data
        this.stockSymbol = stock_symbol

        this.renderCharts()
        this.renderTable()
      } catch (err) {
        console.error(err)
        this.error = 'An error occurred while analyzing the stock.'
      }
    },
    renderCharts() {
      const volume = []
      const avgVolume = []
      this.volumeData.forEach((point) => {
        const date = new Date(point.date).getTime()
        volume.push({
          x: date,
          y: point.volume,
          color: point.is_spike ? 'red' : 'blue',
        })
        if (point.avg_volume) {
          avgVolume.push([date, point.avg_volume])
        }
      })

      Highcharts.chart('volume-chart', {
        chart: { type: 'column' },
        title: { text: 'Volume Data with Spikes' },
        xAxis: { type: 'datetime' },
        yAxis: { title: { text: 'Volume' } },
        series: [
          { name: 'Volume', data: volume },
          { name: '5-Day Average Volume', type: 'line', data: avgVolume, color: 'orange' },
        ],
      })

      const ohlc = this.stockData.map((point) => [
        new Date(point[0]).getTime(),
        point[1],
        point[2],
        point[3],
        point[4],
      ])

      Highcharts.stockChart('candle-chart', {
        rangeSelector: { selected: 1 },
        title: { text: 'Stock Price and OHLC Data' },
        series: [
          {
            type: 'candlestick',
            name: 'Stock Price',
            data: ohlc,
            upColor: 'green',
            color: 'red',
            upLineColor: 'green',
            lineColor: 'red',
          },
        ],
      })
    },
    renderTable() {
      $('#volume-table').DataTable({
        data: this.tableData, // 測試數據
        columns: [
          { data: 'date', title: 'Date' },
          { data: 'high_volume', title: 'High Volume' },
          { data: 'five_day_ma', title: 'Five Day MA' },
        ],
        destroy: true, // 確保重新初始化
        pageLength: 10,
        order: [[0, 'asc']],
      })
    },
  },
}
</script>

<style scoped>
/* Chart Containers */
#candle-chart,
#volume-chart {
  display: flex; /* 使用Flexbox確保內容居中 */
  justify-content: center;
  align-items: center;
  background-color: white;
  border: 1px solid #d4ebd4;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 20px auto;
  width: 90%;
  max-width: 800px;
  height: 400px; /* 固定高度，避免圖表過小或過大 */
}

/* Error Message */
.error p {
  text-align: center;
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
p {
  text-align: center;
  color: #0b5b2e;
  font-weight: bold;
  margin-top: 10px;
}
</style>
