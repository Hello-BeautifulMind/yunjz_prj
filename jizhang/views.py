import json, math
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core import serializers
from jizhang.models import Category, Item
from jizhang.forms import ItemForm, CategoryForm
from jizhang.download.FileHandle import write_excel
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from jizhang.data_format_func import get_sorted_categories
#from jizhang.forms import ItemForm, CategoryForm, NewCategoryForm, FindItemForm

PER_PAGE = 10



@login_required
def items(request):
	'''
	账单明细处理模块，包括删除和查询处理，使用ajax处理
	如果是删除，则提交的删除字段是"del[]:['1','2']"
	'''
	if request.method not in ['GET', 'POST']:
		return HttpResponse('')

	# 账单删除操作
	if request.method == 'POST' and request.is_ajax():			# ajax请求，无刷新删除(在前端使用隐藏达到"删除"效果)
		del_list = list(map(int, request.POST.getlist('del_id[]')))			# 提交的账单列表
		del_results = Item.objects.filter(id__in=del_list).delete()			# 批量删除指定的账单
		print(del_results, type(del_results))
		
		in_json = json.dumps(del_list)			# 删除没有异常，返回删除的列表
		return HttpResponse(in_json, content_type="application/json")
	
	# ajax请求某一页内容: 只查看某一类型时有c_id参数，说明查看的是某一类型下的某一页
	if request.method == 'GET' and request.is_ajax():
		c_id = request.GET.get('c_id', None)	
		page = request.GET.get('page', '')
		page = int(page) - 1 if page.isdigit() and int(page) > 0 else 0
		filter_list = {'category__user':request.user,}			# 设置过滤条件
		if c_id and c_id.isdigit():			# 如果有c_id则设置其为查询条件之一
			filter_list['category__id'] =  int(c_id)
		item_set = Item.objects.filter(**filter_list)[(page*PER_PAGE):(page*PER_PAGE+PER_PAGE)]			# 查询结果
		items_num = Item.objects.filter(**filter_list).count()			# 符合该查询条件的账单数，用于前端构建页码栏
		pages_num = int(math.ceil(items_num/PER_PAGE*1.0))			# 转成页数
		all_objects = item2dict(item_set)			# 将对象转成字典数据以转化为字符串形式的json数据。
		all_objects.append({"pages_num":pages_num})
		#in_json = serializers.serialize('json', item_list, ensure_ascii=False, use_natural_foreign_keys=True) # 也可以用该方法
		in_json = json.dumps(all_objects)			# 字典数据转化为字符串形式的json数据。
		return HttpResponse(in_json, content_type='application/json')
		
	item_list = Item.objects.filter(category__user=request.user)[0:PER_PAGE]			# 不属于查询和删除操作，只返回第一页
	category_list = Category.objects.filter(user=request.user)
	items_num = Item.objects.filter(category__user=request.user).count()			# 用户账单数目		
	pages_num = int(math.ceil(items_num/PER_PAGE*1.0))		
	t = {"categories": category_list, 'items': item_list, 'pages_num':pages_num}
	return render(request, "jizhang/items.html", t)

@login_required
def categories(request):
	'''
	账单分类处理模块，包括删除和查询处理
    注：如果分类下含有子类或者该分类已被其他账单绑定则不能删除
	'''
	del_list, warning_list = list(), list()			# 记录不能删除的分类和可以删除的分类
	all_categories = Category.objects.filter(user=request.user)
	categories = Category.objects.filter(user=request.user)[0:PER_PAGE]			# 只返回一页
	if request.method == 'POST' and request.is_ajax():
		post_list = list(map(int, request.POST.getlist('del_id[]')))			# 提交的分类，不存在返回空列表
		for del_id in post_list:
			print("将删除{}".format(del_id))
			c_childs = set()
			c_childs = get_category_childs(c_childs, all_categories, del_id)			# 获取所有子类
			items = Item.objects.filter(category=del_id)			# 获取绑定该分类的item
			try:
				del_category = Category.objects.get(id=del_id)
				if len(c_childs) != 0 or items.exists():			# 如果该分类有子类或者有item绑定
					print(len(c_childs), items.exists())
					warning_list.append(del_id)			# 记录该分类，然后在页面中高亮提示
				else:
					del_category.delete()
					del_list.append(del_id)
					print('已删除{}, {}, {}'.format(del_id, del_category, 'abc'))
			except Category.DoesNotExist:
				pass		
		# categories = Category.objects.filter(user=request.user)			# 更新页面
		in_json = json.dumps([del_list, warning_list])			# 字典数据转化为字符串形式的json数据
		return HttpResponse(in_json, content_type='application/json')

	# ajax请求某一页内容
	if request.method == 'GET' and request.is_ajax():
		c_id = request.GET.get('c_id', None)	
		page = request.GET.get('page', '')
		page = int(page) - 1 if page.isdigit() and int(page) > 0 else 0
		filter_list = {'user':request.user,}			# 设置过滤条件
		if c_id and c_id.isdigit():
			filter_list['id'] =  int(c_id)
		category_set = Category.objects.filter(**filter_list)[(page*PER_PAGE):(page*PER_PAGE+PER_PAGE)]
		categories_num = Category.objects.filter(**filter_list).count()
		pages_num = int(math.ceil(categories_num/PER_PAGE*1.0))
		all_objects = category2dict(category_set)			# 字典列表
		all_objects.append({"pages_num":pages_num})
		#in_json = serializers.serialize('json', item_list, ensure_ascii=False, use_natural_foreign_keys=True)
		in_json = json.dumps(all_objects)										
		return HttpResponse(in_json, content_type='application/json')

	categories_num = Category.objects.filter(user=request.user).count()			# 用户账单分类数目		
	pages_num = int(math.ceil(categories_num/PER_PAGE*1.0))
	t = {"all_categories": all_categories, "categories": categories, "pages_num": pages_num}
	return render(request, "jizhang/categories.html", t)


# 新建账单操作，使用ajax方式
@login_required
def new_item(request):
	other_error = ''
	if request.method == 'POST' and request.is_ajax():
		print(request.POST)
		form = ItemForm(request, data=request.POST.copy())			# 提交的数据构建该用户的表单对象
		if form.is_valid():			# 数据经过基本验证
			clean_data = form.cleaned_data			# 验证过的数据
			try:
				category = Category.objects.get(id=int(clean_data['category']))			# 从数据库中获取该分类
			except Category.DoesNotExist:
				form.add_error('category', '该分类已经不存在')			# 某些异常
			else:
				pub_date = clean_data['pub_date']
				price = clean_data['price']
				comment = clean_data['comment']
				new_item = Item(pub_date=pub_date, category=category, price=price, comment=comment)			# 通过Item模型将数据保存到数据库
				new_item.save()
				print('Item创建成功')
				in_json = json.dumps([True,{}])			# 返回操作状态，成功
				return HttpResponse(in_json, content_type='application/json')
		in_json = json.dumps([False, form.errors])			# 错误
		return HttpResponse(in_json, content_type='application/json')			# 表单验证不通过，返回错误信息
	else:
		form = ItemForm(request)
	return render(request, "jizhang/new_item.html", {'form':form, 'other_error':other_error})

# 新建账单分类操作，使用ajax方式
@login_required
def new_category(request):
	if request.method == 'POST' and request.is_ajax():
		form = CategoryForm(request, data=request.POST.copy())
		if form.is_valid():
			# 将数据保存到数据库
			clean_data = form.cleaned_data
			# print("clean_data: ", clean_data)
			# form.add_error('category_name', '该分类已经存在')
			# form.add_error('category_name', '第二个错误')
			# print("clean_data: ", clean_data)
			# print("clean_data: ", form.cleaned_data)
			# print("form.errors: ", form['category_name'].errors, type(form['category_name'].errors))
			# print("退出...")
			category_name =	clean_data['category_name']			# 名称
			p_category = None if clean_data['p_category'] == '0' else None 			# 从数据库获取	# 父类名称	value即为id
			isIncome = 	bool(int(clean_data['isIncome']))			# 收入/支出
			u = request.user 			# 用户
			c = Category(p_category=p_category, name=category_name, isIncome=isIncome, user=u)
			try:
				c.save()			# 保存到数据库
			except IntegrityError:
				form.add_error('category_name', '该分类已经存在!')
			else:
				print("category保存成功")
				in_json = json.dumps([True, {}])			# 返回操作状态
				return HttpResponse(in_json, content_type='application/json')
		in_json = json.dumps([False, form.errors])
		return HttpResponse(in_json, content_type='application/json')			# 表单验证不通过，返回错误信息
	else:
		form = CategoryForm(request)
	return render(request, "jizhang/new_category.html", {'form':form,})

# 使用ajax方式修改账单分类
# 并且父类不能设置为自身和其子类
@login_required
def edit_category(request, c_id=None):
	'''
	0、修改的记录是c_id
	1、获取编辑的是哪一条记录
	2、使用提交的数据更新该条记录
	'''
	other_error = {}
	print(request.POST)
	try:
		c = Category.objects.get(id=c_id)			# 将要修改的记录
	except Category.DoesNotExist:
		print('不存在该记录')
	else:
		if request.method == 'POST' and request.is_ajax():
			form = CategoryForm(request, data=request.POST.copy())
			if form.is_valid():
				clean_data = form.cleaned_data
				c.name = clean_data['category_name']			# 修改为新的分类名称
				p_id = int(clean_data['p_category'])			# 获取提交的父类id
				try:
					u_categories = Category.objects.filter(user=request.user)			# 该用户的所有分类
					u_p_id = c_id if c.p_category is None else c.p_category.id
					childs_set = set()
					childs_set = get_category_childs(childs_set, u_categories, u_p_id)			# 获取该用户当前父类下所有子类
					
					c.p_category = None if p_id == 0 else Category.objects.get(id=p_id)			# 新的父类
					if p_id == int(c_id) or c.p_category in childs_set:
						form.add_error('p_category', '父类不能设置为自身和其子类')
						in_json = json.dumps([False, form.errors])
						return HttpResponse(in_json, content_type='application/json')
				except Category.DoesNotExist:
					pass
				else:
					c.isIncome = bool(int(clean_data['isIncome']))			# 新的收支情况
					try:
						c.save()
					except IntegrityError:
						form.add_error('category_name', '该分类已经存在!')
					else:
						print('category修改成功')
						in_json = json.dumps([True, {}])
						return HttpResponse(in_json, content_type='application/json')
			in_json = json.dumps([False, form.errors])
			return HttpResponse(in_json, content_type='application/json')

		else:
			category_name = c.name
			p_category = '0' if c.p_category is None else c.p_category.id
			isIncome = int(c.isIncome)
			form = CategoryForm(request, data={'category_name': category_name,
												'p_category': p_category, 
												'isIncome': isIncome})
		return render(request, 'jizhang/new_category.html', {'form':form, 'other_error':other_error})

# 使用ajax方式修改账单
@login_required
def edit_item(request, item_id):
	'''
	1、修改的记录id是item_id
	2、获取该记录
	3、使用提交的数据更新该记录
	'''
	other_error = ""
	try:
		modify_item = Item.objects.get(id=item_id)
	except Item.DoesNotExist:
		pass
	else:
		if request.method == 'POST' and request.is_ajax():
			form = ItemForm(request, data=request.POST.copy())			# 使用提交的数据构建表单
			if form.is_valid():			# 如果数据格式正确
				clean_data = form.cleaned_data			# 验证过的数据
				c_id = int(clean_data['category'])
				try:
					category = Category.objects.get(id=c_id)			# 分类不存在将抛出异常
				except Category.DoesNotExist:
					form.add_error('category', '该分类已经不存在')
				else:
					modify_item.pub_date = clean_data['pub_date']
					modify_item.category = category
					modify_item.price = clean_data['price']
					modify_item.comment = clean_data['comment']
					try:
						modify_item.save()
					except Exception:
						other_error = "修改保存时发生异常"
					else:
						print('Item修改成功')
						in_json = json.dumps([True, {}])			# 返回成功操作的结果
						return HttpResponse(in_json, content_type='application/json')
			else:
				in_json = json.dumps([False, form.errors])			# 返回错误操作的结果
				return HttpResponse(in_json, content_type='application/json')			# 表单验证不通过，返回错误信息

		else:			# 构建待修改账单的表单
			pub_date = modify_item.pub_date
			category = modify_item.category.id
			price = modify_item.price
			comment = modify_item.comment
			form = ItemForm(request, data={'pub_date': pub_date,
											'category': category,
											'price': price,
											'comment': comment})
		return render(request, 'jizhang/new_item.html', {'form': form, 'other_error':other_error})

@login_required
def del_category(request):
	'''
	如果分类下有子类或者是item中还绑定该分类则不能删除
	'''
	pass

# 父类不能设置为自身和其子类
def get_category_childs(childs_set, categories, p_id):
	childs = categories.filter(p_category=p_id)
	if not childs.exists():
		return childs_set
	for c in childs:
		get_category_childs(childs_set, categories, c.id)
	childs_set.update(childs)
	return childs_set

# 账单分类查询
@login_required
def find_categories(request):
	print(request.POST)
	if request.method == "POST" and request.is_ajax():
		c_id = request.POST.get('c_id', '')
		filter_list = {'user': request.user,}
		if c_id.isdigit():
			filter_list["id"] = c_id 			# 查询条件
		category_set = Category.objects.filter(**filter_list)[0:PER_PAGE]	# 
		categories_num = Category.objects.filter(**filter_list).count()			# 匹配数量
		pages_num = int(math.ceil(categories_num/PER_PAGE*1.0))

		all_objects = category2dict(category_set)
		all_objects.append({"pages_num": pages_num})			# 将页码总数也序列化
		in_json = json.dumps(all_objects)
		return HttpResponse(in_json, content_type='application/json')

# 账单查询
@login_required
def find_items(request):
	print(request.POST)
	if request.method == "POST" and request.is_ajax():
		c_id = request.POST.get('c_id', '')
		filter_list = {'category__user': request.user,}
		if c_id.isdigit():
			filter_list["category__id"] = c_id 			# 查询条件
		item_set = Item.objects.filter(**filter_list)[0:PER_PAGE]			# 返回pub_date最新的5条数据
		items_num = Item.objects.filter(**filter_list).count()				# 匹配数量
		pages_num = int(math.ceil(items_num/PER_PAGE*1.0))

		all_objects = item2dict(item_set)
		all_objects.append({"pages_num": pages_num})			# 将页码总数也序列化
		in_json = json.dumps(all_objects)
		return HttpResponse(in_json, content_type='application/json')

# json转换时将Decimal类型先编码，不然正常情况不能将Decimal序列化	
class DecimalEncoder(json.JSONEncoder):
	pass

# 将模型对象转为可序列化成json对象的格式
def item2dict(item_set):
	item_list = []
	for item in item_set:
		item_list.append({
				'pk': item.id,
				'fields': {
					'price': format(item.price, '.2f'),			# '{:.2f}'.format(item.price) [限于python3.x]
					'pub_date': str(item.pub_date),			# '2017-01-01'
					'comment': item.comment,
					'category': [item.category.id, item.category.name],
				}
			})
	return item_list

def category2dict(category_set):
	category_list = []
	for c in category_set:
		category_list.append({
				'pk': c.id,
				'fields': {
					'c_name': c.name, 
					'p_name': [c.p_category.id, c.p_category.name] if c.p_category else [None, 'None'],		
					'income': c.get_isIncome_display(),
				}
			})
	return category_list


# 导出excel
@login_required
def export_excel(request):
	if request.method == 'GET':
		page = request.GET.get('page', '')
		c_id = request.GET.get('c_id', '')
		filter_list = {'category__user': request.user}
		if c_id.isdigit():
			filter_list['category__id'] = int(c_id)

		if page.isdigit() and page.isdigit() > 0:
			page = int(page) - 1
			data = Item.objects.filter(**filter_list)[page*PER_PAGE:page*PER_PAGE+PER_PAGE]
		else:
			data = []

		return write_excel(data)