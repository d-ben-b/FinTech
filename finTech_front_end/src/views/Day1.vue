<template>
  <div>
    <h1>Stock Analysis</h1>

    <!-- User Input Form -->
    <form @submit.prevent="analyzeStock">
      <label for="stock">Stock Symbol:</label>
      <input v-model="symbol" type="text" id="stock" placeholder="e.g., AAPL, TSLA" required />

      <label for="start_date">Start Date:</label>
      <input v-model="startDate" type="date" id="start_date" required />

      <label for="end_date">End Date:</label>
      <input v-model="endDate" type="date" id="end_date" required />

      <button type="submit">Analyze</button>
    </form>

    <!-- Analysis Section -->
    <div v-if="error" style="margin-top: 20px">
      <p>{{ error }}</p>
    </div>
    <div v-else style="margin-top: 20px">
      <h2>Stock: {{ stockSymbol }}</h2>
      <p>From {{ startDate }} to {{ endDate }}</p>

      <!-- Candle Chart -->
      <div id="candle-chart" style="height: 600px; margin: 50px 0"></div>

      <!-- Volume Chart -->
      <div id="volume-chart" style="height: 300px; margin: 50px 0"></div>

      <!-- Volume Table -->
      <table id="volume-table" class="display"></table>
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
      symbol: '',
      startDate: '',
      endDate: '',
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
        series: [{ type: 'candlestick', name: 'Stock Price', data: ohlc }],
      })
    },
    renderTable() {
      $('#volume-table').DataTable({
        data: this.tableData,
        columns: [
          { data: 'date', title: 'Date' },
          { data: 'high_volume', title: 'High Volume' },
          { data: 'five_day_ma', title: 'Five Day MA' },
        ],
        destroy: true,
        order: [[0, 'asc']],
        pageLength: 10,
      })
    },
  },
}
</script>

<style>
/* Include your CSS here or link it externally */
</style>
