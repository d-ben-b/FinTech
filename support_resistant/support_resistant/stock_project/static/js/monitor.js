// 將訊號自動生成radio buttom
function addRadioButtonbuy(labelText, radioButtonId, radioGroupName) {
    // 创建单选按钮元素
    var radioButton = $('<input>').attr({
        type: 'radio',
        value: radioButtonId,
        id: radioButtonId,
        name: radioGroupName // 设置单选按钮的组名，确保只能选择其中一个
    }).addClass('form-check-input').css({
        'font-size': '10px',
    });

    // 创建标签元素
    var label = $('<label>').addClass('form-check-label').text(' ' + labelText).attr('for', radioButtonId);

    // 直接将单选按钮和标签添加到容器中
    $('#radio-container-buy').append(radioButton, label, '<br>');
}
// 將訊號自動生成radio buttom
function addRadioButtonsell(labelText, radioButtonId, radioGroupName) {
    // 创建单选按钮元素
    var radioButton = $('<input>').attr({
        type: 'radio',
        value: radioButtonId,
        id: radioButtonId,
        name: radioGroupName // 设置单选按钮的组名，确保只能选择其中一个
    }).addClass('form-check-input').css({
        'font-size': '10px',
    });

    // 创建标签元素
    var label = $('<label>').addClass('form-check-label').text(' ' + labelText).attr('for', radioButtonId);

    // 直接将单选按钮和标签添加到容器中
    $('#radio-container-sell').append(radioButton, label, '<br>');
}
// 將讀取買訊號
function addScatterSeriesbuy(dataArray) {
    var signalData = [];
    dataArray.forEach(function(dataPoint) {
        var date = dataPoint[0];
        signalData.push([date,1]);
    });

    return signalData;
}
// 將讀取賣訊號
function addScatterSeriessell(dataArray) {
    var signalData = [];
    dataArray.forEach(function(dataPoint) {
        var date = dataPoint[0];
        signalData.push([date, -1]);
    });

    return signalData;
}
// 將線段資料active push上Highchart stock的k線圖上
function createlineactiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            visible: true,
        })
    }
}
// 將線段資料inactive push上Highchart stock的k線圖上
function createlineinactiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            visible: false,
        })
    }
}
// 將方塊條狀資料inactive push上Highchart stock的k線圖上
function createbarinactiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            fillOpacity: 0.3,
            visible: false,
        })
    }
}
// 將方塊條狀資料active push上Highchart stock的k線圖上
function createbaractiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            fillOpacity: 0.8,
            visible: true,
        })
    }
}
// 前端active, inactive 點選時需要重新產生的線段
function checkboxSeriesVisibility(startIndex, endIndex, obj) {
    for (var time = startIndex; time < endIndex; time++) {
        obj.series[time].visible = !obj.series[time].visible;
    }
    Highcharts.stockChart('highchart-container', obj).destroy();
    new Highcharts.stockChart('highchart-container', obj);
    return true;
}

function remove_from_track_list(track_row){

    var track_spread = new FormData;
    track_spread.append("start_date", track_row['start_date']);
    track_spread.append("symbol", track_row['symbol']);

    $.ajax({
      url: "/supRes/monitor/remove_track/",
      data:track_spread, 
      type:'POST',
      dataType: 'json',
      processData:false,
      contentType:false,
      success:function(data)
      {
        alert("Remove successfully!");
      }
    });
}

function polt_signals(res, ohlc, obj, long_signal, short_signal){
    var seriesCount_before = obj.series.length;
    var signalData = [];
    // long
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap"])) {
        signalData.push(addScatterSeriesbuy(res['gap_up_signal']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["big volume"])) {
        signalData.push(addScatterSeriesbuy(res['big_volume']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['resistance_signal']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['neckline_resistance_signal']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & big volume"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_upgap_bar']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_upgap_resistance']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_upgap_resistance_neckline']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["big volume & resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_bar_resistance']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["big volume & neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_bar_resistance_neckline']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["resistance break out & neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_resistance_resistance_neckline']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & big volume & resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['three_signals_upgap_bar_resistance']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & big volume & neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['three_signals_upgap_bar_resistance_neckline']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["big volume & resistance break out & neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['three_signals_bar_resistance_resistance_neckline']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & resistance break out & neckline resistance break out"])) {
        signalData.push(addScatterSeriesbuy(res['three_signals_upgap_resistance_resistance_neckline']))
    }
    if (JSON.stringify(long_signal) === JSON.stringify(["all signals"])) {
        signalData.push(addScatterSeriesbuy(res['four_signals_buy']))
    }
    // short
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap"])) {
        signalData.push(addScatterSeriessell(res['gap_down_signal']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["big volume"])) {
        signalData.push(addScatterSeriessell(res['big_volume']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["support break down"])) {
        signalData.push(addScatterSeriessell(res['support_signal']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['neckline_support_signal']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & big volume"])) {
        signalData.push(addScatterSeriesbuy(res['two_signals_downgap_bar']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & support break down"])) {
        signalData.push(addScatterSeriessell(res['two_signals_downgap_support']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['two_signals_downgap_support_neckline']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["big volume & support break down"])) {
        signalData.push(addScatterSeriessell(res['two_signals_bar_support']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["big volume & neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['two_signals_bar_support_neckline']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["support break down & neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['two_signals_support_support_neckline']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & big volume & support break down"])) {
        signalData.push(addScatterSeriessell(res['three_signals_downgap_bar_support']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & big volume & neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['three_signals_downgap_bar_support_neckline']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["big volume & support break down & neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['three_signals_bar_support_support_neckline']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & support break down & neckline support break down"])) {
        signalData.push(addScatterSeriessell(res['three_signals_downgap_support_support_neckline']))
    }
    if (JSON.stringify(short_signal) === JSON.stringify(["all signals"])) {
        signalData.push(addScatterSeriessell(res['four_signals_sell']))
    }
    var integratedData = [];
    var currentSignal = null;
    var signalDataresults = [].concat(...signalData) //將多維的陣列轉換為一維陣列
    var signalMap = {};
    if ((JSON.stringify(long_signal) === JSON.stringify(["big volume"]))&&
    (JSON.stringify(short_signal) === JSON.stringify(["big volume"]))) {
        signalDataresults.forEach(function(dataPoint) {
            var date = dataPoint[0];
            var signal = dataPoint[1];
            signalMap[date] = signal;
        });
        ohlc.forEach(function(ohlcPoint) {
            var date = ohlcPoint[0];
            var signal = signalMap[date];
            if (signal !== undefined) {
                currentSignal = 0;
            } else if (currentSignal === null) {
                currentSignal = 0;
            }
        
            // 添加整合後的資料到 integratedData 中，包括日期、OHLC 資料和相應的訊號值
            integratedData.push([date,currentSignal]);
            
        });
        var signal_line = {
            type: 'line', // 指定圖表類型（這裡使用線性圖表）
            showInLegend: false,
            name: 'new-series', // 指定 series 的名稱
            data: integratedData, // 指定 series 的數據（這裡 newDataArray 是一個包含數據點的陣列）
            yAxis: 2,// 其他你需要設置的屬性
            dataGrouping: {
                units: groupingUnits,
                enabled: false

            }
            ,lineWidth: 2
        };
        var longSignals = [];
        var shortSignals = [];
        var signalDataArray = Object.entries(signalMap).map(function(entry) {
            var date = parseInt(entry[0]);
            var signal = entry[1];
                if (signal === -1) {
                    shortSignals.push([date, 0]);
                    longSignals.push([date, 0])
                }

                return [date, signal];
                });
        var longSignalspoint = {
            type: 'scatter',
            data: longSignals , // 使用傳遞的數據
            name: 'Long',
            marker: {
                symbol: 'triangle',
                fillColor: 'green',
                lineColor: 'green',
                lineWidth: 2,
                name: 'buy',
                enabled: true,
                radius: 6
            },
            visibility: true,
            yAxis: 2
        
        };
        var shortSignalspoint = {
            type: 'scatter',
            data: shortSignals , // 使用傳遞的數據
            name: 'Sell',
            marker: {
                symbol: 'triangle-down',
                fillColor: 'red',
                lineColor: 'red',
                lineWidth: 2,
                name: 'sell',
                enabled: true,
                radius: 6
            },
            visibility: true,
            yAxis: 2
        
        };
        }
    else  {
        signalDataresults.forEach(function(dataPoint) {
            var date = dataPoint[0];
            var signal = dataPoint[1];
            signalMap[date] = signal;
        });
        ohlc.forEach(function(ohlcPoint) {
            var date = ohlcPoint[0];
            var signal = signalMap[date];
            if (signal !== undefined) {
                currentSignal = signal;
            } else if (currentSignal === null) {
                currentSignal = 0;
            }
            // 添加整合後的資料到 integratedData 中，包括日期、OHLC 資料和相應的訊號值
            integratedData.push([date,currentSignal]);
            
        });
    
        var signal_line = {
            type: 'line', // 指定圖表類型（這裡使用線性圖表）
            showInLegend: false,
            name: 'new-series', // 指定 series 的名稱
            data: integratedData, // 指定 series 的數據（這裡 newDataArray 是一個包含數據點的陣列）
            yAxis: 2,// 其他你需要設置的屬性
            dataGrouping: {
                units: groupingUnits,
                enabled: false
            }
            ,lineWidth: 2
        };
        var longSignals = [];
        var shortSignals = [];
        var signalDataArray = Object.entries(signalMap).map(function(entry) {
            var date = parseInt(entry[0]);
            var signal = entry[1];
                if (signal === 1) {
                    longSignals.push([date, signal]);
                } else if (signal === -1) {
                    shortSignals.push([date, signal]);
                }

                return [date, signal];
            });
        var longSignalspoint = {
                type: 'scatter',
                data: longSignals , // 使用傳遞的數據
                name: 'Long',
                marker: {
                    symbol: 'triangle',
                    fillColor: 'green',
                    lineColor: 'green',
                    lineWidth: 2,
                    name: 'buy',
                    enabled: true,
                    radius: 6
                },
                visibility: true,
                yAxis: 2
            
            };
        var shortSignalspoint = {
            type: 'scatter',
            data: shortSignals , // 使用傳遞的數據
            name: 'Sell',
            marker: {
                symbol: 'triangle-down',
                fillColor: 'red',
                lineColor: 'red',
                lineWidth: 2,
                name: 'sell',
                enabled: true,
                radius: 6
            },
            visibility: true,
            yAxis: 2
        
        };
    }

    var seriesCount_after= obj.series.length;
    if ((seriesCount_after-seriesCount_before) ==3){
        obj.series.splice(seriesCount_after - 3, 3)
    }
    // 將新的 series 物件添加到 obj 的 series 陣列中
    obj.series.push(signal_line);
    obj.series.push(longSignalspoint);
    obj.series.push(shortSignalspoint);
    Highcharts.stockChart('highchart-container', obj);
    //移除新的 series 物件
    var signal_lineIndex = obj.series.indexOf(signal_line);
    if (signal_lineIndex !== -1) {
        obj.series.splice(signal_lineIndex, 1);
    }

    var longSignalspointIndex = obj.series.indexOf(longSignalspoint);
    if (longSignalspointIndex !== -1) {
        obj.series.splice(longSignalspointIndex, 1);
    }

    var shortSignalspointIndex = obj.series.indexOf(shortSignalspoint);
    if (shortSignalspointIndex !== -1) {
        obj.series.splice(shortSignalspointIndex, 1);
    }
}

function run_monitor_analysis(track_row){
    var track_params = new FormData;    
    track_params.append('signals_selected_values', track_row['signals_selected_values']);
    track_params.append('start_date', track_row['start_date']);
    track_params.append('symbol', track_row['symbol']);
    track_params.append('peak_left', track_row['peak_left'])
    track_params.append('peak_right', track_row['peak_right'])
    track_params.append('valley_left', track_row['valley_left'])
    track_params.append('valley_right', track_row['valley_right'])
    track_params.append('diff', track_row['diff'])
    track_params.append('swap_times', track_row['swap_times'])
    track_params.append('previous_day', track_row['previous_day'])
    track_params.append('survival_time', track_row['survival_time'])
    track_params.append('gap_interval', track_row['gap_interval'])
    track_params.append('nk_valley_left', track_row['nk_valley_left'])
    track_params.append('nk_valley_right', track_row['nk_valley_right'])
    track_params.append('nk_peak_left', track_row['nk_peak_left'])
    track_params.append('nk_peak_right', track_row['nk_peak_right'])
    track_params.append('nk_startdate', track_row['nk_startdate'])
    track_params.append('nk_enddate', track_row['nk_enddate'])
    track_params.append('nk_interval', track_row['nk_interval'])
    track_params.append('nk_value', track_row['nk_value'])

    $.ajax({
        url: "/supRes/monitor/run_analysis/",
        data:track_params, 
        type:'POST',
        dataType: 'json',
        processData:false,
        contentType:false,
        beforeSend: function () { 
            $('#loader').show();
            //  每秒增加一次秒數 
            var minutesLabel = $("#minutes");
            var secondsLabel = $("#seconds");
            var totalSeconds = 0;
            interval = setInterval(setTime, 1000);
            function setTime() {
            ++totalSeconds;
            secondsLabel[0].innerHTML = pad(totalSeconds % 60);
            minutesLabel[0].innerHTML = pad(parseInt(totalSeconds / 60));
            }
            function pad(val) {
            var valString = val + "";
            if (valString.length < 2) {
                return "0" + valString;
            } else {
                return valString;
            }
            }
        },

        success:function(res){

        $('#staticBackdrop').modal('show');
        /*停止計數(避免不斷增加導致下一次點擊按鈕時出問題*/
        clearInterval(interval);

        var support_active = $("#support_active")[0].checked;
        var support_inactive = $("#support_inactive")[0].checked;
        var resistance_active = $("#resistance_active")[0].checked;
        var resistance_inactive = $("#resistance_inactive")[0].checked;
        var volume_active = $("#volume_active")[0].checked;
        var volume_inactive = $("#volume_inactive")[0].checked;
        var gap_up_active = $("#upgap_active")[0].checked;
        var gap_up_inactive = $("#upgap_inactive")[0].checked;
        var gap_down_active = $("#downgap_active")[0].checked;
        var gap_down_inactive = $("#downgap_inactive")[0].checked;
        var neckline_active = $("#neckline_active")[0].checked;
        var neckline_inactive = $("#neckline_inactive")[0].checked;


        // active,inactive的checkbox切換
        if (support_active == false) {
            $("#support_active").checked = true
        }
        if (support_inactive == true) {
            $("#support_inactive").checked = false
        }
        if (resistance_active == false) {
            $("#resistance_active").checked = true
        }
        if (resistance_inactive == true) {
            $("#resistance_inactive").checked = false
        }
        if (volume_active == false) {
            $("#volume_active").checked = true
        }
        if (volume_inactive == true) {
            $("#volume_inactive").checked = false
        }
        if (gap_up_active == false) {
            $("#upgap_active").checked = true
        }
        if (gap_up_inactive == true) {
            $("#upgap_inactive").checked = false
        }
        if (gap_down_active == false) {
            $("#downgap_active").checked = true
        }
        if (gap_down_inactive == true) {
            $("#downgap_inactive").checked = false
        }
        if (neckline_active == false) {
            $("#neckline_active").checked = true
        }
        if (neckline_inactive == true) {
            $("#neckline_inactive").checked = false
        }

        var ohlc = [];
        var volume = [];
        var gap_table = $('#GapTable').DataTable();
        var volume_table = $('#VolumeTable').DataTable();
        var neckline_table = $('#NecklineTable').DataTable();
        var sup_res_table = $('#SRTable').DataTable();

        gap_table.clear().draw();
        volume_table.clear().draw();
        neckline_table.clear().draw();
        sup_res_table.clear().draw();
        $('#short_signal_table').DataTable().clear().draw();
        $('#long_signal_table').DataTable().clear().draw();

        // show short signals table
        $('#short_signal_table').DataTable({
            "searching": true,
            "bAutoWidth": false,
            "bDestroy": true,
            "destroy": true,
            "aLengthMenu":[10, 20, 30],
            data: res["all_signals"]["Short"],
            pageLength:10,
            columns: [
            { data: "number_of_signals" },
            { data: "kind" },
            { data: "status" },
            { data: "date" },
            { data: "price" },
            ],
            columnDefs:[
                {
                    targets: [2],
                    createdCell: function (td, cellData, rowData, row, col) {
                        $(td).css('color', 'red')
                    },
                },
            ],


            dom: 'Bfrtip', // 添加 DataTables 按鈕
            buttons: [
                {
                    extend: 'excelHtml5',
                    title: "detail of signals",
                    text: "匯出Excel",
                    customize: function (xlsx) {
                    }
                },
                'copy',
                'csv', 
                'pdf', 
            ]
        });
        // show long signals table
        $('#long_signal_table').DataTable({
            "bAutoWidth": false,
            "bDestroy": true,
            "destroy": true,
            "aLengthMenu":[10, 20, 30],
            data: res["all_signals"]["Long"],
            pageLength:10,
            columns: [
                { data: "number_of_signals" },
                { data: "kind" },
                { data: "status" },
                { data: "date" },
                { data: "price" },
            ],
            columnDefs:[
                {
                    targets: [2],
                    createdCell: function (td, cellData, rowData, row, col) {
                        $(td).css('color', 'red')
                    },
                },
            ],
            dom: 'Bfrtip', // 添加 DataTables 按鈕
            buttons: [
                {
                    extend: 'excelHtml5',
                    title: "detail of signals",
                    text: "匯出Excel",
                    customize: function (xlsx) {
                    }
                },
                'copy',
                'csv', 
                'pdf', 
            ],
        });
        // gap 的report格式
        if (res['gap_up_active'] != []) {
            for (var i = 0; i < res['gap_up_active'].length; i++) {
                var rowData = res['gap_up_active'][i];
                var row = [
                    res['symbol'],
                    res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                    'Up Gap',
                    rowData[0][1],
                    rowData[0][2],
                    moment(rowData[0][0]).format('YYYY-MM-DD'),
                ];
                gap_table.row.add(row).draw();
            }
        }
        if (res['gap_down_active'] != []) {
            for (var i = 0; i < res['gap_down_active'].length; i++) {
                var rowData = res['gap_down_active'][i];
                var row = [
                    res['symbol'],
                    res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                    'Down Gap',
                    rowData[0][1],
                    rowData[0][2],
                    moment(rowData[0][0]).format('YYYY-MM-DD'),
                ];
                gap_table.row.add(row).draw();
            }
        }
        // volume的report格式
        if (res['bar_report'] != []) {
            for (var i = 0; i < res['bar_report'].length; i++) {
                var rowData = res['bar_report'][i];
                var row = [
                    res['symbol'],
                    res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                    moment(rowData[0]).format('YYYY-MM-DD'),
                    rowData[1],
                    rowData[2],
                    moment(rowData[3]).format('YYYY-MM-DD')
                ];
                volume_table.row.add(row).draw();
            }
        }
        // support的report格式
        if (res['support_active'] != []) {
            for (var i = 0; i < res['support_active'].length; i++) {
                var rowData = res['support_active'][i];
                var row = [
                    res['symbol'],
                    res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                    'Support',
                    rowData[0][1],
                    moment(rowData[0][0]).format('YYYY-MM-DD'),
                ];
                sup_res_table.row.add(row).draw();
            }
        }
        // resistance的report格式
        if (res['resistance_active'] != []) {
            for (var i = 0; i < res['resistance_active'].length; i++) {
                var rowData = res['resistance_active'][i];
                var row = [
                    res['symbol'],
                    res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                    'Resistance',
                    rowData[0][1],
                    moment(rowData[0][0]).format('YYYY-MM-DD'),
                ];
                sup_res_table.row.add(row).draw();
            }
        }
        // neckline的report格式
        if (res['neckline_report'] != []) {
            for (var i = 0; i < res['neckline_report'].length; i++) {
                var rowData = res['neckline_report'][i];
                var row = [
                    res['symbol'],
                    res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                    rowData[3],
                    rowData[0],
                    moment(rowData[1]).format('YYYY-MM-DD'),
                    rowData[3],
                ];
                neckline_table.row.add(row).draw();
            }
        }
        dataLength = res['stock_data'].length,
        // set the allowed units for data grouping
        groupingUnits = [[
            'week',             // unit name
            [1]               // allowed multiples
        ], [
            'month',
            [1, 2, 3, 4, 6]
        ]],
        i = 0;
        for (i; i < dataLength; i += 1) {
            ohlc.push([
                res['stock_data'][i][0], // the date
                res['stock_data'][i][1], // open
                res['stock_data'][i][2], // high
                res['stock_data'][i][3], // low
                res['stock_data'][i][4] // close
            ]);

            volume.push([
                res['stock_data'][i][0], // the date
                res['volume'][i][1] // the volume
            ]);
        }
        // 創建Highchart stock 圖
        var obj = {
            
            rangeSelector: {
                selected: 1,
            },
            navigator: {
                series: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            legend: {
                align: 'left', //水平方向位置
                verticalAlign: 'top', //垂直方向位置
                x: 0, //距离x轴的距离
                y: 20,
                enabled: true
            },

            xAxis: {
                title: {
                    text: 'time'
                }
            },
            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'OHLC'
                },
                height: '60%',
                lineWidth: 2,
                resize: {
                    enabled: true
                }
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Volume'
                },
                top: '60%',
                height: '20%',
                offset: 0,
                lineWidth: 2
            },{
                labels: {
                    align: 'right',
                    x: -3
                }, title: {
                    text: 'line'
                },
                top: '80%',
                height: '20%'
            }],

            title: {
                text: res['symbol'] + "  Stock Price",
            },
            tooltip: {
                split: true
            },
            series: [{
                type: 'candlestick',
                name: 'ohlc',
                showInLegend: false,
                data: ohlc,
                dataGrouping: {
                    units: groupingUnits,
                    enabled: false

                }
            }, {
                type: 'column',
                showInLegend: false,
                name: 'volume',
                data: volume,
                yAxis: 1,
                dataGrouping: {
                    units: groupingUnits,
                    enabled: false

                }
            }],
            stockTools: {
                gui: {
                    /* open/close the buttons by add/remove name in list */
                    /* separator means "-----" in tool bar*/
                    buttons: ['zoomChange', 'fullScreen',
                        'currentPriceIndicator',]
                }
            },
            plotOptions: {
                candlestick: {
                    color: 'red',
                    upColor: 'green'
                },
            }
        }

        createlineactiveSeries(res, 'line','support_active',obj,'#8085e9')
        createlineinactiveSeries(res,'line','support_inactive',obj,'#8085e9')
        createlineactiveSeries(res, 'line','resistance_active',obj,'#e4d354')
        createlineinactiveSeries(res,'line','resistance_inactive',obj,'#e4d354')
        createbaractiveSeries(res,'areasplinerange','bar_active',obj,'#434348')
        createbarinactiveSeries(res,'areasplinerange','bar_inactive',obj,'#434348')
        createbaractiveSeries(res,'areasplinerange','gap_up_active',obj,'#8085e9')
        createbarinactiveSeries(res,'areasplinerange','gap_up_inactive',obj,'#8085e9')
        createbaractiveSeries(res,'areasplinerange','gap_down_active',obj,'#f7a35c')
        createbarinactiveSeries(res,'areasplinerange','gap_down_inactive',obj,'#f7a35c')
        createlineactiveSeries(res, 'line','neckline_support_active',obj,'#8085e9')
        createlineinactiveSeries(res,'line','neckline_support_inactive',obj,'#8085e9')
        createlineactiveSeries(res, 'line','neckline_resistance_active',obj,'#e4d354')
        createlineinactiveSeries(res,'line','neckline_resistance_inactive',obj,'#e4d354')

        Highcharts.stockChart("highchart-container", obj);

        var radioButtonContainerbuy = $('#radio-container-buy')
        var radioButtonContainersell = $('#radio-container-sell')
        $('#radio-container-buy').empty();
        $('#radio-container-sell').empty();
        // long
        if (res['gap_up_signal'].length > 0) {
            addRadioButtonbuy('up gap', 'up_gap','long');
        }
        if (res['big_volume'].length > 0) {
            addRadioButtonbuy('big volume', 'big_volume_buy','long');
        }
        if (res['resistance_signal'].length > 0) {
            addRadioButtonbuy('resistance break out', 'resistance','long');
        }
        if (res['neckline_resistance_signal'].length > 0) {
            addRadioButtonbuy('neckline resistance break out', 'neckline_resistance','long');
        }
        if (res['two_signals_upgap_bar'].length > 0) {
            addRadioButtonbuy('up gap & big volume', 'up_gap_big_volume','long');
        }
        if (res['two_signals_upgap_resistance'].length > 0) {
            addRadioButtonbuy('up gap & resistance break out', 'up_gap_resistance','long');
        }
        if (res['two_signals_upgap_resistance_neckline'].length > 0) {
            addRadioButtonbuy('up gap & neckline resistance break out', 'up_gap_neckline_resistance','long');
        }
        if (res['two_signals_bar_resistance'].length > 0) {
            addRadioButtonbuy('big volume & resistance break out','big volume_resistance','long');
        }
        if (res['two_signals_bar_resistance_neckline'].length > 0) {
            addRadioButtonbuy('big volume & neckline resistance break out','big volume_neckline_resistance','long');
        }
        if (res['two_signals_resistance_resistance_neckline'].length > 0) {
            addRadioButtonbuy('resistance break out & neckline resistance break out','resistance_neckline_resistance','long');
        }
        if (res['three_signals_upgap_bar_resistance'].length > 0) {
            addRadioButtonbuy('up gap & big volume & resistance break out','up_gap_big_volume_resistance','long');
        }
        if (res['three_signals_upgap_bar_resistance_neckline'].length > 0) {
            addRadioButtonbuy('up gap & resistance break out & neckline resistance break out','up_gap_resistance_neckline_resistance','long');
        }
        if (res['three_signals_bar_resistance_resistance_neckline'].length > 0) {
            addRadioButtonbuy('big volume & resistance break out & neckline resistance break out',' big volume_resistance_neckline_resistance','long');
        }
        if (res['three_signals_upgap_resistance_resistance_neckline'].length > 0) {
            addRadioButtonbuy('up gap & resistance break out & neckline resistance break out','up_gap_resistance_neckline_resistance','long');
        }
        if (res['four_signals_buy'].length > 0) {
            addRadioButtonbuy('all signals',' all_signals');
        }
        radioButtonContainerbuy.show();

        // short
        if (res['gap_down_signal'].length > 0) {
            addRadioButtonsell('down gap', 'down_gap','short');
        }
        if (res['big_volume'].length > 0) {
            addRadioButtonsell('big volume', 'big_volume_sell','short');
        }
        if (res['support_signal'].length > 0) {
            addRadioButtonsell('support break down', 'support','short');
        }
        if (res['neckline_support_signal'].length > 0) {
            addRadioButtonsell('neckline support break down', 'neckline_support','short');
        }
        if (res['two_signals_downgap_bar'].length > 0) {
            addRadioButtonsell('down gap & big volume', 'down_gap_big_volume','short');
        }
        if (res['two_signals_downgap_support'].length > 0) {
            addRadioButtonsell('down gap & support break down', 'down_gap_support','short');
        }
        if (res['two_signals_downgap_support_neckline'].length > 0) {
            addRadioButtonsell('down gap & neckline support break down', 'down_gap_neckline_support','short');
        }
        if (res['two_signals_bar_support'].length > 0) {
            addRadioButtonsell('big volume & support break down','big volume_support','short');
        }
        if (res['two_signals_bar_support_neckline'].length > 0) {
            addRadioButtonsell('big volume & neckline support break down','big volume_neckline_support','short');
        }
        if (res['two_signals_support_support_neckline'].length > 0) {
            addRadioButtonsell('support break down & neckline support break down','support_neckline_support','short');
        }
        if (res['three_signals_downgap_bar_support'].length > 0) {
            addRadioButtonsell('down gap & big volume & support break down','down_gap_big_volume_support','short');
        }
        if (res['three_signals_downgap_bar_support_neckline'].length > 0) {
            addRadioButtonsell('down gap & big volume & neckline support break down','down_gap_big_volume_neckline_support','short');
        }
        if (res['three_signals_bar_support_support_neckline'].length > 0) {
            addRadioButtonsell('big volume & support break down & neckline support break down',' big volume_support_neckline_support','short');
        }
        if (res['three_signals_downgap_support_support_neckline'].length > 0) {
            addRadioButtonsell('down gap & support break down & neckline support break down','down_gap_support_neckline_support','short');
        }
        if (res['four_signals_sell'].length > 0) {
            addRadioButtonsell('all signals','all_signals','short');
        }
        radioButtonContainersell.show();
        
        // polt signals
        var radioContainerbuy = $("#radio-container-buy")[0];      
        var radioContainersell = $("#radio-container-sell")[0];
        if (radioContainerbuy.hasChildNodes() && radioContainerbuy.hasChildNodes()) {
            radioContainerbuy.querySelector('input[type="radio"]').checked = true;
            radioContainersell.querySelector('input[type="radio"]').checked = true;
            var radioElementsbuy = radioContainerbuy.querySelectorAll("input[type='radio']:checked");
            var radioElementssell = radioContainersell.querySelectorAll("input[type='radio']:checked");
            var long_signal = Array.from(radioElementsbuy).map(function(radio) {
                return radio.nextElementSibling.textContent.trim();
            });
            var short_signal = Array.from(radioElementssell).map(function(radio) {
                return radio.nextElementSibling.textContent.trim();
            });
            polt_signals(res, ohlc, obj, long_signal, short_signal)
        } 

        // polt signals
        $("#run_strategy").on("click", function () {
            var radioContainerbuy = $("#radio-container-buy")[0];
            var radioContainersell = $("#radio-container-sell")[0];
            var long_signal = [];
            var short_signal = [];
            var radioElementsbuy = radioContainerbuy.querySelectorAll("input[type='radio']:checked");
            var radioElementssell = radioContainersell.querySelectorAll("input[type='radio']:checked");
            var long_signal = Array.from(radioElementsbuy).map(function(radio) {
                return radio.nextElementSibling.textContent.trim();
            });
            var short_signal = Array.from(radioElementssell).map(function(radio) {
                return radio.nextElementSibling.textContent.trim();
            });
            polt_signals(res, ohlc, obj, long_signal, short_signal)
        })

        $("#support_active").on("click", function () {
            checkboxSeriesVisibility(2, 2 + res['support_active'].length, obj);
        });
        $("#support_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            2 + res['support_active'].length,
            res['support_active'].length + res['support_inactive'].length + 2, 
            obj);
        });
        $("#resistance_active").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length, 
            obj);
        });
        $("#resistance_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length, 
            obj);
        });
        $("#volume_active").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length,
            obj);
        });
        $("#volume_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length +2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length,
            obj);
        });
        $("#upgap_active").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + res['gap_up_active'].length,
            obj);
        });
        $("#upgap_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length+
            res['bar_active'].length + res['bar_inactive'].length + res['gap_up_active'].length+2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length +
            res['bar_active'].length + res['bar_inactive'].length + res['gap_up_active'].length+res['gap_up_inactive'].length,
            obj);
        });
        $("#downgap_active").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length+ res['gap_up_inactive'].length+2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length+ res['gap_up_inactive'].length+res['gap_down_active'].length,
            obj);
        });
        $("#downgap_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length+res['gap_up_inactive'].length+res['gap_down_active'].length+2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length+res['gap_up_inactive'].length+res['gap_down_active'].length+res['gap_down_inactive'].length,
            obj);
        });
        $("#neckline_active").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+ 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length,
            obj);
        });
        $("#neckline_active").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+ 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+res['neckline_resistance_active'].length,
            obj);
        });
        $("#neckline_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+res['neckline_support_active'].length+ 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length,
            obj);
        });
        $("#neckline_inactive").on("click", function () {
            checkboxSeriesVisibility( 
            res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+res['neckline_resistance_active'].length+ 2,
            res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
            res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+res['neckline_resistance_active'].length+res['neckline_resistance_inactive'].length,
            obj);
        });
        },
        complete: function () { // Set our complete callback, adding the .hidden class and hiding the spinner.
                $('#loader').hide();
                /* 將計數重製為0*/
                clearInterval(interval);
                var minutesLabel = $("#minutes");
                var secondsLabel = $("#seconds");
                minutesLabel[0].innerHTML = "00";
                secondsLabel[0].innerHTML = "00";
        },
    });
}

$(document).ready(function (){
  
    $.ajax({
        url: "/supRes/monitor/get_track_list/",
        type: "post",
        dataType : 'json',
        processData : false,
        contentType : false,
        success: function (res) {

            var table=$("#monitor").DataTable(
                {
                data:res.track_data,
                "scrollX": true,
                columns:[

                    { data: 'symbol'},
                    { data: 'start_date'},
                    { data: 'signals_selected_values'},
                    { data: 'gap_interval'},
                    { data: 'diff'},
                    { data: 'peak_left'},
                    { data: 'peak_right'},
                    { data: 'valley_left'},
                    { data: 'valley_right'},
                    { data: 'swap_times'},
                    { data: 'previous_day'},
                    { data: 'survival_time'},
                    { data: 'nk_valley_left'},
                    { data: 'nk_valley_right'},
                    { data: 'nk_peak_left'},
                    { data: 'nk_peak_right'},
                    { data: 'nk_startdate'},
                    { data: 'nk_enddate'},
                    { data: 'nk_interval'},
                    { data: 'nk_value'},
                    { data: 'track_date'},
                    {
                        className: 'dt-remove-tracking',
                        orderable: false,
                        data: null,
                        defaultContent: '<button type="button" class="btn btn-danger">Untrack</button>',
                    },
                    {
                        className: 'dt-run-analysis',
                        orderable: false,
                        data: null,
                        defaultContent: '<button type="button" class="btn btn-success">Run_analysis</button>',
                    },
                ],
                order: [[1, 'asc']],
                });
            
            $('#monitor tbody').on('click', 'td.dt-remove-tracking', function () {
                var row = table.row($(this).parents('tr'));
                var data = row.data();
                remove_from_track_list(data);                        
                row.remove().draw();
            });

            $('#monitor tbody').on('click', 'td.dt-run-analysis', function () {
                var row = table.row($(this).parents('tr'));
                var track_row = row.data();
                run_monitor_analysis(track_row);
            });
        }
    });
});











