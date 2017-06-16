$(function() {
	$("#reg-btn").click(function() {
		this.blur();
		$.each($(".field-warning"), function(i, item) {
			$(item).css("visibility", "hidden");// 先把错误字段隐藏，防止已通过的字段还出现上一次的错误
		});
		var uname = $("#id_username").val();
		var email = $("#id_email").val();
		var pwd = $("#id_password").val();
		var re_pwd = $("#id_re_password").val();

		var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
		$.ajax({
			url: "/accounts/register/",
			dataType: "json",
			method: "POST",
			data: {"csrfmiddlewaretoken": csrf_token, "username": uname, 
					"email":email, "password": pwd, "re_password": re_pwd},
			success: function(ret) {
				if(ret[0] == true) {
					$("#prompt-info").css("visibility", "visible");
					setTimeout(function() {window.location.href = "/accounts/login";} , 1000);
				}
				else {
					$.each(ret[1], function(k, v) {
						$("#" + k + "-error").html(v[0]);
						$("#" + k + "-error").css("visibility", "visible");
					});
				}
			}
		});
		
	});
});
