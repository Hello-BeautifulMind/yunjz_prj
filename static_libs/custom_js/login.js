$(function() {
	// 回车事件
	document.onkeydown = function(e){
	    var ev = document.all ? window.event : e;
	    if(ev.keyCode==13) {
	    	$("#login-btn").click();
	     }
	};

	// 如果用户勾选记住用户名，下次登录时设置其为默认用户名
	var user_name = getCookie("username");
	if(user_name) {
		$("#id_username").val(user_name);
	}

	$("#login-btn").click(function() {
		var uname = $("#id_username").val();
		var pwd = $("#id_password").val();
		if(uname == "" || pwd == "") {
			$("#loging-warning").css("visibility", "visible");
			$("#loging-warning").html("账号和密码不能为空!");
			setTimeout(function() {$("#loging-warning").css("visibility", "hidden");}, 3000);
			if(uname == "") {
				$("#id_username").focus();
			}
			else {
				$("#id_password").focus();
			}
			
		}
		else {
			var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
			$.ajax({
				url: "/accounts/login/",
				dataType: "json",
				method: "POST",
				data: {"csrfmiddlewaretoken": csrf_token, "username": uname, "password": pwd},
				success: function(is_auth) {
					if(is_auth) {
						if($(":checkbox").get(0).checked) {
							setCookie("username", uname, 2);	// 保留2天
						}
						window.location.href = "/accounts/index";
					}
					else {
						$("#loging-warning").css("visibility", "visible");
						$("#loging-warning").html("账号或者密码输入错误!");
						setTimeout(function() {$("#loging-warning").css("visibility", "hidden");}, 3000);
						$("#id_username").focus();
					}
				}
			});
		}
	});
});

// 使用cookie记住用户名
function setCookie(name, value, timeout) {  
    var d = new Date();  
    d.setDate(d.getDate() + timeout);  
    document.cookie = name + '=' + value + ';expires=' + d;  
}  

function getCookie(name) {  
    var arr = document.cookie.split('; ');  
    for ( var i = 0; i < arr.length; i++) {  
	    var arr2 = arr[i].split('='); //['abc','cba']  
	    if (arr2[0] == name) {  
	    	return arr2[1];  
	    }  
	}  
    return '';
}  