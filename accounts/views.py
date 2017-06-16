from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from accounts.forms import RegisterForm, ModifyPasswordForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
import json

# Create your views here.
@login_required
def index(request):
	return HttpResponseRedirect('/jizhang')

def login(request):
	'''
		登录视图
		request.POST是一个字典对象，包含提交的数据
	'''
	template_var = {}
	if request.method == "POST" and request.is_ajax():
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")
		# print(request.user, type(request.user)) AnonymousUser <class 'django.utils.functional.SimpleLazyObject'>
		user = auth.authenticate(username=username, password=password)			# 不通过认证则返回None（只是账号认证，还没登录）
		if user is not None and user.is_active:	
			# print(request.user, type(request.user)) AnonymousUser 'django.utils.functional.SimpleLazyObject'
			auth.login(request, user)			# 认证通过后进行登录，生成session
			# print(request.user, type(request.user)) xiaoming <class 'django.contrib.auth.models.User'>
			return HttpResponse(json.dumps(True), content_type='application/json')			# 登录成功
		else:
			return HttpResponse(json.dumps(False), content_type='application/json')			# 登录失败
	return render(request, "accounts/login.html", template_var)
	

def register(request):
	'''
		注册视图
	    注意加"/"和不加"/"的区别
	'''
	template_var = {}
	if request.method == "POST":
		form = RegisterForm(data=request.POST.copy())			# 使用提交的数据构建表单
		if form.is_valid():			# 表单字段验证正常
			post_data = form.cleaned_data
			username = post_data["username"]
			password = post_data["password"]
			email = post_data["email"]
			user = User.objects.create_user(username, email, password)			# 创建用户
			in_json = json.dumps([True,])			# 创建成功，向前端返回True
			return HttpResponse(in_json, content_type='application/json')
		else:
			in_json = json.dumps([False, form.errors])			# 创建失败
			print(in_json)
			return HttpResponse(in_json, content_type='application/json')
		# 注册完毕 重定向到登录页面
		#return HttpResponseRedirect("/accounts/index")
	else:
		form = RegisterForm()
	template_var["form"] = form
	return render(request, "accounts/register.html", template_var)

# 用户注销
@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/accounts/login")

# 修改密码
@login_required
def modify_password(request):
	if request.method == 'POST' and request.is_ajax():			# 通过提交的数据进行构建表单对象
		print(request.POST)
		form = ModifyPasswordForm(data=request.POST.copy())
		if form.is_valid():			# 表单字段验证
			cleaned_data = form.cleaned_data
			old_pwd = cleaned_data['old_password']
			new_pwd = cleaned_data['new_password']
			user = auth.authenticate(username=request.user.username, password=old_pwd)			# 原密码验证
			if user is not None:			# 原密码正确
				if new_pwd == request.user.username:			# 密码不能和用户名相同
					form.add_error('new_password', '密码不能和用户名相同')
				else:
					print('密码修改成功')
					# print(request.user is user)
					# print(type(user))
					user.set_password(new_pwd)
					user.save()
					in_json = json.dumps([True, {}])			# 向前端返回True
					return HttpResponse(in_json, content_type='application/json')			# 修改成功
			else:			# 原密码不正确
				form.add_error('old_password', '密码输入不正确')
		in_json = json.dumps([False, form.errors])
		return HttpResponse(in_json, content_type='application/json')	
	else:
		form = ModifyPasswordForm()
	return render(request, 'accounts/modify_password.html', {'form': form})
