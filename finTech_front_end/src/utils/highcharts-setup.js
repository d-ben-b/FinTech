import Highcharts from 'highcharts/highstock' // Import Highstock

// Set up localization
const isChinese = navigator.language === 'zh-CN' || navigator.language === 'zh-TW'

Highcharts.setOptions({
  lang: {
    loading: isChinese ? '加載中...' : 'Loading...',
    months: isChinese
      ? [
          '一月',
          '二月',
          '三月',
          '四月',
          '五月',
          '六月',
          '七月',
          '八月',
          '九月',
          '十月',
          '十一月',
          '十二月',
        ]
      : [
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December',
        ],
    weekdays: isChinese
      ? ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
      : ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    shortMonths: isChinese
      ? [
          '一月',
          '二月',
          '三月',
          '四月',
          '五月',
          '六月',
          '七月',
          '八月',
          '九月',
          '十月',
          '十一月',
          '十二月',
        ]
      : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    thousandsSep: ',',
    decimalPoint: '.',
  },
  accessibility: {
    enabled: true, // Enable accessibility
  },
})

export default Highcharts
