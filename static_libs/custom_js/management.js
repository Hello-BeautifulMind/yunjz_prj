$(function() {
	$("#modify-pwd").click(function() {
		var old_pwd = $("#id_old_password").val();
		var new_pwd = $("#id_new_password").val();
		var re_new_pwd = $("#id_re_new_password").val();

		var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
		$.ajax({
			url: "/accounts/modify_password/",
			dataType: "json",
			method: "POST",
			data: {"csrfmiddlewaretoken": csrf_token, "old_password": old_pwd, 
					"new_password": new_pwd, "re_new_password": re_new_pwd},
			success: function(ret) {
				if(ret[0] == true) {
					$("#prompt-info").css("visibility", "visible");
					setTimeout(function() {window.location.href = "/accounts/logout";} , 1000);
				}
				else {
					$.each($(".field-warning"), function(i, item) {
						$(item).css("visibility", "hidden");// 先把错误字段隐藏，防止已通过的字段还出现上一次的错误
					});
					$.each(ret[1], function(k, v) {
						$("#" + k + "-error").html(v[0]);
						$("#" + k + "-error").css("visibility", "visible");
					});
				}
			}
		});
		
	});
});