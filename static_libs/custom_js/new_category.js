$(function() {
	$("#submit-btn").click(function() {
		this.blur();
		$.each($(".field-warning"), function(i, item) {
			$(item).css("visibility", "hidden");// 先把错误字段隐藏，防止已通过的字段还出现上一次的错误
		});
		var c_name = $("#id_category_name").val();
		var p_category = $("#id_p_category").val();
		var isIncome = $("#id_isIncome").val();
		var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
		var cur_url = window.location.href;
		$.ajax({
			url: cur_url,
			dataType: "json",
			method: "POST",
			data: {"csrfmiddlewaretoken": csrf_token, "category_name": c_name, 
					"p_category":p_category, "isIncome": isIncome},
			success: function(ret) {
				if(ret[0] == true) {
					$("#prompt-info").css("visibility", "visible");
					setTimeout(function() {$("#prompt-info").css("visibility", "visible");;
						window.location.href="/jizhang/categories";}, 1000);
				}
				else {
					$.each(ret[1], function(k, v) {
						$("#" + k + "-error").html(v[0]);
						$("#" + k + "-error").css("visibility", "visible");
					});
				}
			},
		});
		
	});	
});
