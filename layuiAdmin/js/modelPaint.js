function modelPaint(container, twoCategories, threeCategories, fourCategories){
    var chart = Highcharts.chart(container, {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: '模型训练历史记录散点图'
        },
        credits: {
            enabled: false
        },
        // 隐藏右上角的图片导出按钮
        exporting: {
            enabled:false
        },
        // subtitle: {
        //     text: '数据来源: Heinz  2003'
        // },
        xAxis: {
            title: {
                enabled: true,
                text: '密文大小 (kb)'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: '准确率/%'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
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
            data: twoCategories
        }, {
            name: '三分类',
            color: 'rgba(119, 152, 191, .5)',
            data: threeCategories
        }, {
            name: '四分类',
            color: '#e5f890',
            data: fourCategories
        }]
    });
}