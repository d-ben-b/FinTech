<template>
  <div>
    <h1>股票定價結果</h1>
    <highcharts :options="chartOptions" />
  </div>
</template>

<script>
export default {
  name: 'StockChart',
  data() {
    return {
      // 從後端獲取的數據
      chartData: {
        PBR: { low: 526.66278, avg: 682.52296, high: 829.76698 },
        PER: { low: 351.181736, avg: 451.54157999999995, high: 546.8756599999999 },
        high_low: {
          high: 541.5454545454545,
          low: 366.72727272727275,
          avg: 496.54545454545456,
        },
        dividend: {
          low: 676.3636363636364,
          avg: 901.8181818181819,
          high: 1352.7272727272727,
        },
      },
      chartOptions: {},
    }
  },
  mounted() {
    this.initializeChart()
  },
  methods: {
    initializeChart() {
      const categories = ['1', '2', '3', '4']
      const lowPrices = [
        this.chartData.PER.low,
        this.chartData.PBR.low,
        this.chartData.high_low.low,
        this.chartData.dividend.low,
      ]
      const avgPrices = [
        this.chartData.PER.avg,
        this.chartData.PBR.avg,
        this.chartData.high_low.avg,
        this.chartData.dividend.avg,
      ]
      const highPrices = [
        this.chartData.PER.high,
        this.chartData.PBR.high,
        this.chartData.high_low.high,
        this.chartData.dividend.high,
      ]

      this.chartOptions = {
        chart: {
          type: 'bar',
        },
        title: {
          text: 'final',
        },
        xAxis: {
          categories: categories,
          title: {
            text: 'method',
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: 'price',
            align: 'high',
          },
          labels: {
            overflow: 'justify',
          },
        },
        tooltip: {
          valueSuffix: ' NT-dollar',
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        legend: {
          reversed: true,
        },
        series: [
          {
            name: 'Expensive',
            data: highPrices,
            color: '#FF0000', // 設置紅色
          },
          {
            name: 'Average',
            data: avgPrices,
            color: '#FFD700', // 設置黃色
          },
          {
            name: 'Cheap',
            data: lowPrices,
            color: '#00FF00', // 設置綠色
          },
        ],
      }
    },
  },
}
</script>

<style>
h1 {
  text-align: center;
}
</style>
