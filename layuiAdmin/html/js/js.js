$(function () {
    var url = 'http://122.51.255.207:8080/getModelTrainRecords';
    var msgdata = Ajax({}, url, 'GET');
    if(msgdata['msg']==='error'){
        alert('An error found!');
        return false;
    }
    var result = msgdata['data'];

    heightchart('echart1', 'RF', result['RF']);
    heightchart('echart2', 'SVM', result['SVM']);
    heightchart('echart3', 'AlexNet', result['AlexNet']);
    heightchart('echart4', 'SCNN', result['SCNN']);
    heightchart('echart5', 'ResNet', result['ResNet']);
    heightchart('echart6', 'VGG', result['VGG']);
    // echarts_1();
    // echarts_2();
    // echarts_4();
    // echarts_31();
    // echarts_32();
    // echarts_33();
    // echarts_5();
    // echarts_6();
    function heightchart(container, title, data) {
        // 基于准备好的dom，初始化echarts实例
        var chart = Highcharts.chart(container, {
            chart: {
                type: 'scatter',
                zoomType: 'xy'
            },
            title: {
                text: title
            },
            subtitle: {
                text: null
            },
            // 隐藏右下角的hightcharts官方链接
            credits: {
                enabled: false
            },
            // 隐藏右上角的图片导出按钮
            exporting: {
                enabled:false
            },
            xAxis: {
                title: {
                    enabled: true,
                    text: null
                },
                // startOnTick: true,
                // endOnTick: true,
                // showLastLabel: true
            },
            yAxis: {
                title: {
                    text: null
                }
            },
            // legend: {
            //     layout: 'vertical',
            //     align: 'left',
            //     verticalAlign: 'top',
            //     x: 30,
            //     y: 10,
            //     floating: true,
            //     backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            //     // borderWidth: 1,
            //     itemStyle : {
            //         'fontSize' : '10px'
            //     }
            // },
            plotOptions: {
                scatter: {
                    marker: {
                        radius: 2,
                        states: {
                            hover: {
                                enabled: true,
                                lineColor: 'rgb(100,100,100)'
                            }
                        }
                    },
                    states: {
                        hover: {
                            marker: {
                                enabled: false
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<b>{series.name}</b><br>',
                        pointFormat: '{point.x} MB, {point.y} %'
                    }
                }
            },
            series: [{
                name: '二分类',
                color: 'rgba(223, 83, 83, .5)',
                showInLegend: false,
                data: data['twoCategories']
            }, {
                name: '三分类',
                color: 'rgba(119, 152, 191, .5)',
                showInLegend: false,
                data: data['threeCategories']
            }, {
                name: '四分类',
                color: '#e5f890',
                showInLegend: false,
                data: data['fourCategories']
            }]
        });
    }
})
