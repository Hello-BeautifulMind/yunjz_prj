from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from accounts.forms import RegisterForm, ModifyPasswordForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
import json
import os
import time
import string
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Create your views here.
ascii_letters = 'abcdefghjkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'		# 去掉‘i o l O’
digits = '123456789'		# 去掉0
ALLOW_CHARS = ''.join([ascii_letters, digits])
font_type = 'simkai.ttf'

class VerificationCode(object):
	'''
	验证码类
	'''
	def __init__(self):
		pass

	# 创建验证码
	def create_validate_code(self, size=(100, 34),
                             chars=ALLOW_CHARS,
                             img_type="GIF",
                             mode="RGB",
                             bg_color=(255, 255, 255),
                             fg_color=(0, 0, 255),
                             font_size=20,
                             font_type=font_type,
                             length=4,
                             draw_lines=True,
                             n_line=(1, 3),
                             draw_points=True,
                             point_chance = 2):
		'''
		@todo: 生成验证码图片
		@param size: 图片的大小，格式（宽，高），默认为(120, 30)
		@param chars: 允许的字符集合，格式字符串
		@param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
		@param mode: 图片模式，默认为RGB
		@param bg_color: 背景颜色，默认为白色
		@param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
		@param font_size: 验证码字体大小
		@param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
		@param length: 验证码字符个数
		@param draw_lines: 是否划干扰线
		@param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
		@param draw_points: 是否画干扰点
		@param point_chance: 干扰点出现的概率，大小范围[0, 100]
		@return: [0]: PIL Image实例
		@return: [1]: 验证码图片中的字符串
		'''
		width, height = size # 宽， 高
		img = Image.new(mode, size, bg_color) # 创建图形
		draw = ImageDraw.Draw(img) # 创建画笔
		if draw_lines:
			self.create_lines(draw,n_line,width,height)
		if draw_points:
			self.create_points(draw,point_chance,width,height)
		strs = self.create_strs(draw,chars,length,font_type, font_size,width,height,fg_color)

		# 图形扭曲参数
		params = [1 - float(random.randint(1, 2)) / 100,
		        0,
		        0,
		        0,
		        1 - float(random.randint(1, 10)) / 100,
		        float(random.randint(1, 2)) / 500,
		        0.001,
		        float(random.randint(1, 2)) / 500
		        ]
		img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
		img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）
		return img, strs

	def create_lines(self, draw,n_line,width,height):
		'''绘制干扰线'''
		line_num = random.randint(n_line[0],n_line[1]) # 干扰线条数
		for i in range(line_num):
			# 起始点
			begin = (random.randint(0, width), random.randint(0, height))
			#结束点
			end = (random.randint(0, width), random.randint(0, height))
			draw.line([begin, end], fill=(0, 0, 0))
	  
	def create_points(self, draw,point_chance,width,height):
		'''绘制干扰点'''
		chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]
		for w in range(width):
			for h in range(height):
				tmp = random.randint(0, 100)
				if tmp > 100 - chance:
					draw.point((w, h), fill=(0, 0, 0))
	  
	def create_strs(self, draw,chars,length,font_type, font_size,width,height,fg_color):
		'''绘制验证码字符'''
		'''生成给定长度的字符串，返回列表格式'''
		c_chars = random.sample(chars, length)
		strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开

		font = ImageFont.truetype(font_type, font_size)
		font_width, font_height = font.getsize(strs)
		draw.text(((width - font_width) / 3, (height - font_height) / 3),strs, font=font, fill=fg_color)
		return ''.join(c_chars)

# 获取验证码
def get_verification_code(request):
	vc = VerificationCode()
	code_img = vc.create_validate_code()		# 创建验证码
	img_name = time.strftime('%Y%m%d%H%M%S', time.gmtime())
	code_img[0].save(img_name + ".png", "PNG")	# 保存到本地
	request.session['auth_code'] = code_img[1].lower()		# 将当前验证码保存到session中
	f = open(img_name + ".png", "rb")		# 图片格式，二进制形式打开
	buffer = f.read()
	f.close()
	try:
		os.remove(img_name + ".png")		# 移除本地的验证码图片
		print("验证码图片'{}.png'已被移除".format(img_name))
	except FileNotFoundError:
		pass
	return HttpResponse(buffer, content_type='image/png')

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
		captcha = request.POST.get("captcha", "")

		if captcha != request.session['auth_code']:		# 验证码核对
			return HttpResponse(json.dumps([False, 'auth_code_failed']))
		# print(request.user, type(request.user)) AnonymousUser <class 'django.utils.functional.SimpleLazyObject'>
		user = auth.authenticate(username=username, password=password)			# 不通过认证则返回None（只是账号认证，还没登录）
		if user is not None and user.is_active:	
			# print(request.user, type(request.user)) AnonymousUser 'django.utils.functional.SimpleLazyObject'
			auth.login(request, user)			# 认证通过后进行登录
			# print(request.user, type(request.user)) xiaoming <class 'django.contrib.auth.models.User'>
			return HttpResponse(json.dumps([True, ""]), content_type='application/json')			# 登录成功
		else:
			return HttpResponse(json.dumps([False, 'user_auth_failed']), content_type='application/json')			# 登录失败
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
