// 封装paint画图函数，传入特征名和对应的p-value作为参数
    function paint(feature, msgdata){
        var chart = Highcharts.chart(feature,{
        chart: {
            type: 'column'
        },
        title: {
            text: feature + '   p-value值统计检验'
            // text: null ，将text设置为null可以隐藏标题
        },
        // 隐藏右下角的hightcharts官方链接
        credits: {
            enabled: false
        },
        // 隐藏右上角的图片导出按钮
        exporting: {
            enabled:false
        },
        subtitle: {
            text: '数据来源: 向广利密文技术部'
        },
        xAxis: {
            title: {
                text: 'p-value'
            },
            categories: [
                '0','0.01','0.02','0.03','0.04','0.05','0.06','0.07','0.08','0.09',
                '0.1','0.11','0.12','0.13','0.14','0.15','0.16','0.17','0.18','0.19',
                '0.20','0.21','0.22','0.23','0.24','0.25','0.26','0.27','0.28','0.29',
                '0.30','0.31','0.32','0.33','0.34','0.35','0.36','0.37','0.38','0.39',
                '0.40','0.41','0.42','0.43','0.44','0.45','0.46','0.47','0.48','0.49',
                '0.50','0.51','0.52','0.53','0.54','0.55','0.56','0.57','0.58','0.59',
                '0.60','0.61','0.62','0.63','0.64','0.65','0.66','0.67','0.68','0.69',
                '0.70','0.71','0.72','0.73','0.74','0.75','0.76','0.77','0.78','0.79',
                '0.80','0.81','0.82','0.83','0.84','0.85','0.86','0.87','0.88','0.89',
                '0.90','0.91','0.92','0.93','0.94','0.95','0.96','0.97','0.98','0.99',
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            // title: {
            //     text: '数量'
            // },
            title: null
        },
        tooltip: {
            // head + 每个 point + footer 拼接成完整的 table
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.0f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointWidth: 4,
                borderWidth: 1
            },
            series: {
                colorByPoint: true
            }
        },
        series: [{
            name: feature,
            // showInLegend设置为false表示不显示该图标
            showInLegend: false,
            data: msgdata
        }]
    });
    }
