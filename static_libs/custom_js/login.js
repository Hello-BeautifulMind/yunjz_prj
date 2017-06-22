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
		$.each($(".field-warning"), function(i, item) {
			$(item).css("visibility", "hidden");// 先把错误字段隐藏，防止已通过的字段还出现上一次的错误
		});
		var uname = $("#id_username").val();
		var pwd = $("#id_password").val();
		var captcha = $("#id_captcha").val();
		if(uname == "" || pwd == "" || captcha == "") {
			if(captcha == "") {
				$("#captcha-error").html("请输入验证码");
				$("#captcha-error").css("visibility", "visible");
				$("#id_captcha").focus();
			}
			if(pwd == "") {
				$("#password-error").html("请输入密码");
				$("#password-error").css("visibility", "visible");
				$("#id_password").focus();
			}
			if(uname == "") {
				$("#username-error").html("请输入用户名");
				$("#username-error").css("visibility", "visible");
				$("#id_username").focus();
			}
			
		}
		else {
			var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
			$.ajax({
				url: "/accounts/login/",
				dataType: "json",
				method: "POST",
				data: {"csrfmiddlewaretoken": csrf_token, "username": uname, "password": pwd, "captcha": captcha},
				success: function(auth) {
					if(auth[0]) {
						if($(":checkbox").get(0).checked) {
							setCookie("username", uname, 2);	// 保留2天
						}
						window.location.href = "/accounts/index";
					}
					else {
						if(auth[1] == "user_auth_failed") {
							$("#loging-warning").css("visibility", "visible");
							$("#loging-warning").html("账号或者密码输入错误!");
							setTimeout(function() {$("#loging-warning").css("visibility", "hidden");}, 3000);
							$("#id_username").focus();
						}
						else if(auth[1] == "auth_code_failed"){
							$("#captcha-error").html("验证码输入错误");
							$("#captcha-error").css("visibility", "visible");
							$("#id_captcha").focus();
						}
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