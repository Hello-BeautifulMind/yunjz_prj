import string
from django import forms
from django.contrib.auth.models import User

# _0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALLOW_CHAR = string.ascii_letters + string.digits + "_"
PWD_ALLOW_CHAR = string.ascii_letters + string.digits + string.punctuation

class RegisterForm(forms.Form):
	# 验证错误时可以保留用户提交的数据，这个适用于重新生成表单，如果使用ajax方式则不需要
	# def __init__(self, *args, **kwargs):
	# 	forms.Form.__init__(self, *args, **kwargs)
	# 	if self.data:	# 如果有提交数据
	# 		self.fields['password'].widget.attrs['value'] = self.data.get('password')
	# 		self.fields['re_password'].widget.attrs['value'] = self.data.get('re_password')
	
	username = forms.CharField(max_length=40, required=True,
		widget=forms.TextInput(attrs={'size': 40, 'class':'form-control', 'placeholder':'昵称长度不能小于4位'}))
	email = forms.EmailField(max_length=40, required=False,
		widget=forms.EmailInput(attrs={'size':40, 'class':'form-control', 'placeholder':'example@163.com'}))
	password = forms.CharField(max_length=20, required=True,
		widget=forms.PasswordInput(attrs={'size':20, 'class':'form-control', 'placeholder':'密码长度不能小于6位'}))
	re_password = forms.CharField(max_length=20, required=True,
		widget=forms.PasswordInput(attrs={'size':20, 'class':'form-control', 'placeholder':'密码长度不能小于6位'}))

	def clean_username(self):
		'''验证昵称, 长度不小于4'''
		username = self.cleaned_data["username"]
		print("clean_username: ", self.cleaned_data)
		if len(username) < 4:
			raise forms.ValidationError("昵称长度不能小于4位")
		else:
			for c in username:
				if c not in ALLOW_CHAR:
					raise forms.ValidationError("昵称仅能用字母、数字或下划线")
		# try:
		# 	uname = User.objects.get(username=username)
		# except User.DoesNotExist:
		# 	pass
		# else:
		# 	raise forms.ValidationError("用户'{}'已经存在".format(username))
		userquery = User.objects.filter(username=username)
		if len(userquery) != 0:
			raise forms.ValidationError("用户'{}'已经存在".format(username))

		return username

	# 密码验证
	def clean_password(self):
		username = self.cleaned_data.get("username", None)
		password = self.cleaned_data["password"]
		print("password:", password)
		print("clean_password: ",self.cleaned_data)
		if len(password) < 6:
			raise forms.ValidationError("密码长度不能小于6位")
		elif password == username:
			raise forms.ValidationError("用户名和密码不能相同")
		
		for c in password:
			if c not in PWD_ALLOW_CHAR:
				raise forms.ValidationError("密码中包含非法字符'{}'".format(c))
		return password

	def clean_re_password(self):
		password = self.cleaned_data.get("password", None)
		if password is None:
			return None
		re_password = self.cleaned_data["re_password"]
		print("re_password:", password)
		print("clean_re_password: ",self.cleaned_data)
		if password != re_password:
			raise forms.ValidationError("两次密码输入不一致")
		return re_password

class ModifyPasswordForm(forms.Form):
	'''
		如果实例化了一个表单类，则该表单实例会有一个cleaned_data属性，这是一个包含干净的提交数据的字典
		类似clean_字段()这样的方法是在字段的默认校验规则执行完之后才被调用，而且已通过默认校验规则的字段
		可以在cleaned_data中找到，如果在自定义的方法中字段又不通过，则该字段会从cleaned_data中除去
	'''
	old_password = forms.CharField(max_length=20, required=True, 
		widget=forms.PasswordInput(attrs={'size':20, 'class':'form-control', 'placeholder':'请输入原密码'}))
	new_password = forms.CharField(max_length = 20, required=True,
		widget=forms.PasswordInput(attrs={'size':20, 'class':'form-control', 'placeholder':'新密码长度不能小于6位'}))
	re_new_password = forms.CharField(max_length=20, required=True,
		widget=forms.PasswordInput(attrs={'size':20, 'class':'form-control', 'placeholder':'新密码长度不能小于6位'}))
    
    # 密码验证
	def clean_new_password(self):
		new_password = self.cleaned_data["new_password"]
		if len(new_password) < 6:
			raise forms.ValidationError("密码长度不能小于6位")
		for c in new_password:
			if c not in PWD_ALLOW_CHAR:
				raise forms.ValidationError("密码中包含非法字符'{}'".format(c))
		return new_password

	def clean_re_new_password(self):
		new_password = self.cleaned_data.get("new_password", None)
		if new_password is None:
			return None
		re_new_password = self.cleaned_data["re_new_password"]
		
		if new_password != re_new_password:
			raise forms.ValidationError("两次密码输入不一致")
		return re_new_password