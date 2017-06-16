$(function() {
	$("#submit-btn").click(function() {
		this.blur();
		$.each($(".field-warning"), function(i, item) {
			$(item).css("visibility", "hidden");// 先把错误字段隐藏，防止已通过的字段还出现上一次的错误
		});
		var pub_date = $("#id_pub_date").val();
		var category = $("#id_category").val();
		var price = $("#id_price").val();
		var comment = $("#id_comment").val();
		var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
		var cur_url = window.location.href;
		$.ajax({
			url: cur_url,
			dataType: "json",
			method: "POST",
			data: {"csrfmiddlewaretoken": csrf_token, "pub_date": pub_date, 
					"category":category, "price": price, "comment": comment},
			success: function(ret) {
				if(ret[0] == true) {
					$("#prompt-info").css("visibility", "visible");
					setTimeout(function() {window.location.href = "/jizhang";} , 1000);
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
