// 封装ajax请求，传入strItem参数，声明为特征选择指标
function Ajax(Data, Url, Method){
    var msgdata = {};
    $.ajax({
            url: Url,
            method: Method,
            // data: {
            //     item: strItem
            // },
            data: Data,

            // ajax使用return返回数据时async必须声明为同步，而不能是异步
            // async: true,
            async: false,
            contentType: 'application/json',
            dataType: 'json',
            success: function(msg){
                // console.log(typeof msg);
                // console.log(msg['msg']);
                msgdata = msg;
            },
            error: function(msg){
                // console.log(typeof msg);
                // console.log(msg['msg']);
                alert('请求失败！');
            }

        })

    return msgdata;
}