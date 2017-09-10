$("#login").click(function(){
    $.ajax({
        type:"POST",    //请求类型
        url:"/userLogin",       //后台路由
        dataType:"json",        //后台给前端的data类型
        data:{
            URLID:id
        },
        success:function(data){     //返回成功后的动作，在这里更新前端的数据，也可以在这里发起下一个请求，具体看你怎做
            if(data.status==601){
                alert(data.errMsg);
            }
            else{
                alert(data.errMsg);
            }
        },
        error:function(jqXHR){      //错误处理
            alert("发生错误"+jqXHR.status);
        },
    })
})
