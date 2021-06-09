$(function () {
    var url = 'http://122.51.255.207:8080/pieChartModelTrain';
    var msgdata = Ajax({}, url, 'GET');
    if(msgdata['msg']==='error'){
        alert('An error found!');
        return false;
    }
    var result = msgdata['data'];

    piechart(result['category'], result['algorithm']);
    function piechart(category, algorithm){
        var chartDom = document.getElementById('piechart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            // tooltip: {
            //     trigger: 'item',
            //     formatter: '{a} <br/>{b}: {c} ({d}%)'
            // },
            legend: {
                data: ['二分类', '三分类', '四分类']
            },
            series: [
                {
                    name: '访问来源',
                    type: 'pie',
                    selectedMode: 'single',
                    radius: [0, '30%'],
                    label: {
                        position: 'inner',
                        fontSize: 14,
                    },
                    labelLine: {
                        show: false
                    },
                    data: [
                        {value: category['twoCategories'], name: '二分类'},
                        {value: category['threeCategories'], name: '三分类'},
                        {value: category['fourCategories'], name: '四分类'}
                    ],
                    color: ['rgba(223, 83, 83, .5)', 'rgba(119, 152, 191, .5)', '#e5f890']
                },
                {
                    name: '访问来源',
                    type: 'pie',
                    radius: ['55%', '45%'],
                    labelLine: {
                        length: 30,
                    },
                    label: {
                        // formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                        formatter: '{b|{b}:}{per|{d}%}  ',
                        backgroundColor: '#F6F8FC',
                        borderColor: '#8C8D8E',
                        borderWidth: 1,
                        borderRadius: 6,
                        
                        rich: {
                            a: {
                                color: '#6E7079',
                                lineHeight: 22,
                                align: 'center'
                            },
                            hr: {
                                borderColor: '#8C8D8E',
                                width: '100%',
                                borderWidth: 1,
                                height: 0
                            },
                            b: {
                                color: '#4C5058',
                                fontSize: 10,
                                fontWeight: 'bold',
                                lineHeight: 20
                            },
                            per: {
                                color: '#fff',
                                backgroundColor: '#4C5058',
                                padding: [2, 2],
                                borderRadius: 1,
                                fontSize: 10
                            }
                        }
                    },
                    data: [
                        {value: algorithm['RF'], name: 'RF'},
                        {value: algorithm['SVM'], name: 'SVM'},
                        {value: algorithm['AlexNet'], name: 'AlexNet'},
                        {value: algorithm['SCNN'], name: 'SCNN'},
                        {value: algorithm['ResNet'], name: 'ResNet'},
                        {value: algorithm['VGG'], name: 'VGG'},
                    ]
                }
            ]
        };

        option && myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

})
