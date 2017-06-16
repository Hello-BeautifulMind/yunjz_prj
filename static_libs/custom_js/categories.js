$(function() {
	// $.ajaxSetup({
	// 	data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
	// });
 
	// 解决单击链接时在按钮周围留下的虚边
	$("a").focus(function() {	
		this.blur();
	});

	// 全选功能的实现[通过和全选checkbox状态一致就可以了]
	$("#all").click(function() {
		var checked_status = this.checked
		$("input[name=del_id]").each(function() {
			this.checked = checked_status;
		});
	});

	//(jquery元素集合)[0] --> 转为相应的DOM对象，然后使用DOM对象提供的方法
	$("#reset-btn").click(function() {
		$(".form-inline")[0].reset();		
		this.blur();
	});

	// ajax方式删除操作
	$("#del-btn").click(function() {
		$("#myModal").modal("hide");
		$("#del-warning").css("visibility", "hidden");
		var c_list = $("input:checkbox[name='del_id']:checked").map(function() { return parseInt(this.value)}).get();
		var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
			url: CATEGORIES_URL,
			dataType: "json",
			method: "POST",
			data: {"csrfmiddlewaretoken":csrf_token, "del_id": c_list},
			success: function(ret) {	// 注意页面中的值为字符型，json返回的是int型
				// 已删除的隐藏
				$.each(ret[0],function(i, c_id) {
					if(c_list.indexOf(c_id) > -1) {
						$("#c_id" + c_id).hide();
					}
				});
				// 不能删除的标记
				$.each(ret[1], function(i, c_id) {
					if(c_list.indexOf(c_id) > -1) {
						$("#c_id" + c_id).addClass("warning");
					}
				});
				if(ret[1].length > 0) {
					$("#del-warning").css("visibility", "visible");
					// 3s后警告框隐藏
					setTimeout(function(){$("#del-warning").css("visibility", "hidden")},3000);
				}
			}
		})
	});  // ajax方式删除操作结束

		// ajax方式查询操作
	$("#search-btn").click(function() {
		//alert($("#items-info").offset().top);
		//alert($("#items-info").height());
		var category_search = $("#category-search").val();		// 分类id
		if("0" == category_search) {
			window.location.href = CATEGORIES_URL;				// 没有选择，刷新页面
		}
		else {
            var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
			$.ajax({
				url: FIND_CATEGORIES_URL,
				dataType: "json",
				method: "POST",
				data: {"csrfmiddlewaretoken":csrf_token, "c_id": category_search},
				beforeSend: function() {
					$("#search-btn").addClass("disabled");			// 发送ajax后暂时禁用按钮，防止重复提交
					var x = $("#items-info").offset();
					var info_height = $("#items-info").height();	// 内容高度
					var info_width = $("#items-info").width();		// 内容宽度
					var loadgif_height = $("#loading").height();	// loading内容高度和宽度
					var loadgif_width = $("#loading").width();
					var top = x.top + info_height/2 - loadgif_height/2 + "px";//使’加载中‘内容位于显示区中间
					var left = info_width/2 - loadgif_width/2 + "px";
					$("#loading").css({"top":top, "left":left});
					$("#loading").show();
				},
				success: update_node,
				complete: function() {
					$("#search-btn").removeClass("disabled");		// 移除按钮禁用状态
					$("#loading").hide();
				},
				error: function(data) {
					$("#search-btn").removeClass("disabled");
					$("#loading").hide();
					console.error("error: " + data.responseText);
				},
			})
		}

	});	// ajax方式查询操作结束

});



// 	// 导出excel
// 	$("#export-excel").click(function() {
// 		if($(".pagination li.active").length == 0) {
// 			return false;
// 		}
// 		var active_page = $(".pagination li.active:first").children('a:first').attr("href");
// 		var parms = parse_url(active_page);
// 		send_parms = parms["c_id"] == "" ? "?page=" : "?c_id=" + parms["c_id"] + "&page="
// 		window.location.href = EXPORT_EXCEL_URL+send_parms+parms["page"];
// 	});	// 导出excel结束 
// });

// ajax回调函数
function update_node(ret) {
	$("#footer").addClass("fixed-bottom");  // 页脚固定到底部
	var pages_num = ret.pop()["pages_num"];
	if( ret.length >0 ) {	// 
		$("#items-info").html("");
		// 在前端指定排序方法[如果在后台数据已经排好序了前台就不需要这个了，现在后台默认以pub_date降序排列]
		// ret = ret.sort(function(item1, item2) {
		// 	return item1["fields"]["pub_date"] < item2["fields"]["pub_date"]; // 按时间降序
		// });
		$.each(ret, function(i, item) {
			var new_node = $('<tr>' +
			'<td data-toggle="tooltip" data-placement="top" title="编辑该分类"><a href="' + EDIT_CATEGORY_URL + '"></a></td>' + 
			'<td data-toggle="tooltip" data-placement="top" title="编辑该分类"><a href="' + EDIT_CATEGORY_URL + '"></a></td>' +
			'<td data-toggle="tooltip" data-placement="left" title="编辑该分类"><a href="#"></a></td>' +
			'<td><input type="checkbox" name="del_id" value="" autocomplete="off"/></td>' +
			'</tr>');
			new_node.attr("id", "c_id"+item["pk"]);
			var a1 = new_node.find("a").eq(0);
			var a2 = new_node.find("a").eq(1);
			var a3 = new_node.find("a").eq(2);
			a1.attr("href", a1.attr("href").replace("0", item["pk"]));
			a1.text(item["fields"]["c_name"]);
			a3.text(item["fields"]["income"]);
			if(item["fields"]["p_name"][0] === null) {
				a2.parent().html(item["fields"]["p_name"][1]);
			}
			else {
				a2.attr("href", a2.attr("href").replace("0", item["fields"]["p_name"][0]));
				a2.text(item["fields"]["p_name"][1]);
			}
			new_node.find("input:first").val(item["pk"]);		// checkbox值设置

			$("#items-info").append(new_node);
			//new_node.appendTo($("#items-info"));
		});

		// POST请求才生成分页
		if(this["method"] == "POST") {
			var c_id = ret[0]["pk"];
			var pagination = $(".pagination:first");
			pagination.html("");
			pagination.append('<li class="page-turn"><a href="" class="btn btn-primary disabled" onclick="get_page(this.href); return false;"  onfocus="this.blur();" id="prev-page"><span>&laquo;</span></a></li>');
			for(var i=1; i<=pages_num && i<12; i++) {
				var active_class = 1==i ? "active" : "";
				if(i == 11 && "{{ pages_num }}" > 10) {
					var li_node = '<li id="omit-page"><span>...</span></li>'
				}
				else {
					var li_node = '<li class="' + active_class + '"><a href="?c_id=' + c_id + '&page=' + i + '" onclick="get_page(this.href); return false;" onfocus="this.blur();">' + i + '</a></li>'  
				}
				$(".pagination:first").append(li_node);
			}

			var next_page_class = pages_num <= 1 ? "btn btn-primary disabled" : "btn btn-primary";
			pagination.append('<li class="page-turn"><a href="?c_id=' + c_id + '&page=2" id="next-page" class="' + next_page_class + '" onclick="get_page(this.href); return false;" onfocus="this.blur();"><span>&raquo;</span></a></li>');

			pagination.append('<li class="page-turn"><span style="border:none; margin-left:20px; color:#999;">共<em id="pages-num">' + pages_num + '</em>页，到第</span><input type="text" id="skip-page" style="position:relative; float:left; margin-top: 1px; width: 40px; height:30px; border: 1px solid #ddd;" value="1" /><span style="border:none; padding-left:5px; color:#999;">页</span><a href="?c_id=' + c_id + '&page=" id="gogo" onclick="skip_page(this.href); return false;" onfocus="this.blur();">跳转</a><span id="input-error" style="visibility: hidden; color: red; border:none;">请输入一个大于0的数字</span></li>');
		}
		// GET请求更新分页栏
		else {
			update_pagination(this["url"], pages_num);
		}
	}
	else {
		var n = ['<tr><td colspan="5" style="text-align: center; background-color: #F5F5F5;"><img src="', NO_DATA_IMG_URL, '" alt=', "'暂无数据' /></td></tr>"];
		var nodata = n.join('');
		$("#items-info").html(nodata);
		$(".pagination:first").html("");
	}
	footerPosition();		// 重新计算页脚
}	// update_node 结束

// ajax 方式获取某一页内容
function get_page(page_url) {
	$.ajax({
		url: page_url,
		dataType: "json",
		method: "GET",
		beforeSend: function() {
			var x = $("#items-info").offset();
			var info_height = $("#items-info").height();			// 内容高度
			var info_width = $("#items-info").width();				// 内容宽度
			var loadgif_height = $("#loading").height();			// loading内容高度和宽度
			var loadgif_width = $("#loading").width();
			var top = x.top + info_height/2 - loadgif_height/2 + "px";//使’加载中‘内容位于显示区中间
			var left = info_width/2 - loadgif_width/2 + "px";
			$("#loading").css({"top":top, "left":left});
			$("#loading").show();
		},
		success: update_node,
		complete: function() {
			// 取消加载中图片
			$("#loading").hide();
		},
	});
}	// ajax 方式获取某一页内容结束

// 跳转
function skip_page(page_url) {
	var page = $("#skip-page").val();
	$("#input-error").css("visibility", "hidden");			// 先隐藏错误
	if(page == "" || isNaN(page) || parseInt(page) <= 0) {	// 注意：空字符串用isNaN判断时会认为是数字0
		$("#input-error").css("visibility", "visible");
		$("#skip-page").focus();
		return false;
	}
	get_page(page_url + page);
}

// 更新分页栏
function update_pagination(url, pages_num) {
	var pages_num = parseInt(pages_num);	// 总页码
	var parms = parse_url(url);				// 获取请求页参数，可以直接通过参数传进来，或者用正则提取
	var cur_page = parseInt(parms["page"]);	// 当前页
	var cur_category = parms["c_id"];		// 分类
	var next_page = $("#next-page");
	var prev_page = $("#prev-page");
	var href_parm = cur_category == "" ? "?page=" : "?c_id=" + cur_category + "&page=";
	if(cur_page < pages_num) {				// 当前页码小于总页码说明有下一页
		next_page.removeClass("disabled");
		next_page.attr("href", href_parm + (cur_page + 1));
	}
	else {									// 否则没有，“下一页”按钮禁用
		next_page.addClass("disabled");
	}

	if(cur_page > 1) {						// 当前页码大于1说明有上一页
		prev_page.removeClass("disabled");
		prev_page.attr("href", href_parm + (cur_page - 1));
	}
	else {									// 否则没有，“上一页”按钮禁用
		prev_page.addClass("disabled");
	}
	// 设置页码
	var first_page = cur_page <= 10 ? 1 : parseInt((cur_page-1)/10)*10 + 1;
	var page_list = [];

	for(var i=0; i<10; i++) {
		page_list[i] = first_page + i;		// 页码列表
	}
	
	$(".pagination li:not(.page-turn)").each(function(index, dom_ele) {
		$(dom_ele).removeClass("active");
		$(dom_ele).css("display", "none");	// 让每一个链接先隐藏
	});	// 移除所有链接的活动属性

	// 计算当前的位置
	var active_pos = cur_page<=10 ? cur_page % 11 : cur_page % page_list[0] + 1;
	$(".pagination li").eq(active_pos).addClass("active");	// 给当前链接设置活动属性

	// 更新每个链接的值
	var n = 0;
	$(".pagination a:not(#prev-page,#next-page,#gogo)").each(function(index, dom_ele) {
		$(dom_ele).attr("href", href_parm + page_list[index]);
		$(dom_ele).html(page_list[index]);
		if(page_list[index] <= pages_num) {
			$(dom_ele).parent().css("display", "");		// 在页码不大于总页数时才显示
			n = index;									// 记住分页栏中最后一个索引
		}
	});
	if(page_list[n] < pages_num) {						// 如果分页栏最后一个页码小于总页码
		$("#omit-page").css("display", "");				// 显示的最后一页比总页数小则显示'...'
	}
	$("skip-page").val(pages_num);
	$("#input-error").css("visibility", "hidden");		// 隐藏错误跳转错误
}

// 提取一个链接的所有参数
function parse_url(url) {
	var pattern = /(\w+)=(\w+)/ig;
	var parms = {};
	url.replace(pattern, function(parm1, key, value) {
		parms[key] = value;
	});
	parms.hasOwnProperty("page") ? "" : parms["page"] = "";
	parms.hasOwnProperty("c_id") ? "" : parms["c_id"] = "";
	return parms;
}