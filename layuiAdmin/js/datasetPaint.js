function datasetPaint(container){
    var chart = Highcharts.chart(container, {
        title: {
            text: '数据集使用情况'
        },
        credits: {
            enabled: false
        },
        // 隐藏右上角的图片导出按钮
        exporting: {
            enabled:false
        },
        xAxis: {
            categories: ['LibriSpeech', 'Caltech256', 'CIFAR10', 'THUCNews']
        },
        yAxis: {
            min: 0,
            // title: {
            //     text: '数量'
            // },
            title: null
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        // labels: {
        //     items: [{
        //         html: '数据集占比',
        //         style: {
        //             left: '220px',
        //             top: '8px',
        //             color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
        //         }
        //     }]
        // },
        series: [{
            type: 'column',
            name: 'account for original',
            color: '#99d0f9',
            data: [8.47, 11.95, 13.97, 10.91]
        }, {
            type: 'column',
            name: 'account for after Cipher',
            color: '#78838b',
            data: [91.53, 88.05, 86.03, 89.09]
        }, 
        // {
        //     type: 'column',
        //     name: 'CIFAR10',
        //     data: [4, 3, 3, 9]
        // }, {
        //     type: 'column',
        //     name: 'THUCNews',
        //     data: [4, 3, 3, 9]
        // }, 
        // {
        //     type: 'spline',
        //     name: '平均值',
        //     data: [3, 2.67, 3, 6.33, 3.33],
        //     marker: {
        //         lineWidth: 2,
        //         lineColor: Highcharts.getOptions().colors[3],
        //         fillColor: 'white'
        //     }
        // }, 
	//     type: 'pie',
        //     name: '占比',
        //     data: [{
        //         name: 'LibriSpeech',
        //         y: 63.25,
        //         color: Highcharts.getOptions().colors[0] // Jane's color
        //     }, {
        //         name: 'Caltech256',
        //         y: 25.30,
        //         color: Highcharts.getOptions().colors[1] // John's color
        //     }, {
        //         name: 'CIFAR10',
        //         y: 10.88,
        //         color: Highcharts.getOptions().colors[2] // Joe's color
        //     }, {
        //         name: 'THUCNews',
        //         y: 0.57,
        //         color: Highcharts.getOptions().colors[3] // Joe's color
        //     }],
        //     center: [230, 60],
        //     size: 100,
        //     showInLegend: false,
        //     dataLabels: {
        //         enabled: false
        //     }
        // }
]
    });
}