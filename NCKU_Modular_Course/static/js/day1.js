document.addEventListener("DOMContentLoaded", function () {
  const volumeData = JSON.parse(
    document.getElementById("volume-data").textContent
  );
  const ohlc = JSON.parse(document.getElementById("ohlc-data").textContent);
  const tableData = JSON.parse(
    document.getElementById("table-data").textContent
  );

  if (!volumeData || volumeData.length === 0) {
    console.error("Volume data not available.");
    return;
  }

  if (!ohlc || ohlc.length === 0) {
    console.error("OHLC data not available.");
    return;
  }

  const volume = [];
  const avgVolume = [];
  volumeData.forEach((point) => {
    const date = new Date(point.date).getTime();
    volume.push({
      x: date,
      y: point.volume,
      color: point.is_spike ? "red" : "blue", // 爆量紅色，其他藍色
    });
    if (point.avg_volume) {
      avgVolume.push([date, point.avg_volume]);
    }
  });

  // 初始化成交量圖
  Highcharts.chart("volume-chart", {
    chart: { type: "column" },
    title: { text: "Volume Data with Spikes" },
    xAxis: { type: "datetime" },
    yAxis: { title: { text: "Volume" } },
    series: [
      {
        name: "Volume",
        data: volume,
        tooltip: { valueDecimals: 0 },
      },
      {
        name: "5-Day Average Volume",
        type: "line", // 使用折線圖表示均線
        data: avgVolume,
        tooltip: { valueDecimals: 0 },
        color: "orange", // 五日均線顯示為橘色
      },
    ],
  });

  // 格式化 OHLC 數據
  const formattedOhlc = ohlc.map((point) => [
    new Date(point[0]).getTime(), // 日期轉換為時間戳
    point[1], // Open
    point[2], // High
    point[3], // Low
    point[4], // Close
  ]);

  // 初始化蠟燭圖
  Highcharts.stockChart("candle-chart", {
    rangeSelector: {
      selected: 1, // 預設選擇範圍
    },
    title: {
      text: "Stock Price and OHLC Data",
    },
    xAxis: { type: "datetime" },
    series: [
      {
        type: "candlestick",
        name: "Stock Price",
        data: formattedOhlc, // 蠟燭圖數據
        tooltip: {
          valueDecimals: 2, // 顯示小數點位數
        },
      },
    ],
  });

  // 初始化 DataTable
  $("#volume-table").DataTable({
    data: tableData,
    columns: [
      { data: "date", title: "Date" },
      { data: "high_volume", title: "High Volume" },
      { data: "five_day_ma", title: "Five Day MA" },
    ],
    order: [[0, "asc"]],
    pageLength: 10, // 每頁顯示 10 筆
  });
});
