/**
 * 用于将$('form').serializeArray()获取的数组转换为对象
 */
window.formArray2Data=function(array=[]){
    var data={};
    for (var i = 0; i < array.length; i++) {
        data[array[i].name]=array[i].value;
    }
    return data;
};

/**
 * 类Vue路由设计
 */
function initRouter() {
    var url = window.location.href;
    // console.log(url);
    var router;
    // url.indexOf("#/")返回值为-1时表示url路由有'#/'这一片段
    if (url.indexOf("#/") > -1) {
        router = url.substring(url.indexOf('#/') + 2);
        console.log(router);
        if (router === '') {
            router = 'testSet.html';
        }
        $('#iframeParent').attr('src', 'html/' + router);
    } else {
        $('#iframeParent').attr('src', 'html/testSet.html');
        // 如果url中不存在 #/ 这一段地址，那么当前url直接访问的是.../index.html#/trainingSet.html
        history.replaceState(null, null, '#/testSet.html');
        // window.location.reload();
    }
    //地址栏修改不刷新的解决方案
    // $('a').click(function () {
    //     if ($(this).attr('href')) {
    //         window.location.href = $(this).attr('href');
    //         window.location.reload();
    //     }
    // });

    $('a').click(function () {
        // var url = $(this).attr('href');
        // var id = $(this).attr('id');
        // console.log(url, id);
        // console.log(url.substring(url.indexOf('#/') + 2));
        if ($(this).attr('href')) {
            if ($(this).attr('id')) {
                window.location.href = $(this).attr('href');
                window.location.reload();
            }
            else{
                window.location.href = $(this).attr('href');
                // $('#iframeParent').attr('src', $('#iframeParent').attr('src'));
                // $('#iframeParent').attr('src', 'html/' + $(this).attr('href').substring($(this).attr('href').indexOf('#/') + 2));
                // var str = $(this).attr('href');
                console.log($(this).attr('href').replace('#', 'html'));
                $('#iframeParent').attr('src', $(this).attr('href').replace('#', 'html'));
                // window.location.reload();
            }
        }
    });

}

var layuiModules=[];
var useKindEditor=false;

$(function () {
    console.log(layuiModules);
    //加载layui模块
    layui.use(layuiModules, function () {
        for (let layuiModule of layuiModules) {
            eval(`window.${layuiModule}=layui.${layuiModule}`);
        }
        if(useKindEditor){
            KindEditor.ready(function (K) {
                window.KindEditor=K;
                mounted();
            });
        }else{
            mounted();
        }

    });
}); 
