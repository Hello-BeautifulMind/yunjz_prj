$(function() {
	footerPosition = function (){
        $("#footer").removeClass("fixed-bottom");
        var contentHeight = document.body.scrollHeight,//网页正文全文高度
            winHeight = window.innerHeight;//可视窗口高度，不包括浏览器顶部工具栏
        if(!(contentHeight > winHeight)){
            //当网页正文高度小于可视窗口高度时，为footer添加类fixed-bottom
            $("#footer").addClass("fixed-bottom");
        }
    };
    footerPosition();
    $(window).resize(footerPosition);

    // 激活当前url
    var cur_path = window.location.pathname.split("/");
    if(cur_path.length > 0) {
    	if(cur_path.length <= 3){
    		var active_path = "items";
    	}
    	else {
    		var active_path = cur_path[cur_path.length - 2];
    	}
    	$("#" + active_path).css("background-color", "#e2e2e2");
    }
});