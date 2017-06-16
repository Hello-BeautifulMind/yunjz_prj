from django import forms
from jizhang.models import Category

class InitializeForm(forms.Form):
	# 选择项取自数据库
	def __init__(self, request, *args, **kwargs):
		forms.Form.__init__(self, *args, **kwargs)
		categoies = Category.objects.filter(user=request.user)		# 为不同用户设置其所拥有的账单分类
		choices_list = []
		for c in categoies:
			value = c.id
			option = c
			choices_list.append((value, option))
		field_name = 'category' if 'category' in self.fields else 'p_category'
		if field_name == 'p_category': choices_list.insert(0, ('0', '无'))
		self.fields[field_name].choices = choices_list

class ItemForm(InitializeForm):
	pub_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(format='%Y-%m-%d',	# 可以直接用DateField
		attrs={'class':'form-control', 'placeholder':'日期(2017-01-01)',}))
	category = forms.ChoiceField(required=True, widget=forms.Select(
		attrs={'class':'form-control',}))
	price = forms.DecimalField(required=True, widget=forms.NumberInput(
		attrs={'class':'form-control', 'placeholder':'金钱',}))
	comment = forms.CharField(required=False, widget=forms.Textarea(
		attrs={'class':'form-control', 'rows':'3', 'cols': '4', 'placeholder':'注释',}))
	
	# 选择项取自数据库
	# def __init__(self, *args, **kwargs):
	# 	forms.Form.__init__(self, *args, **kwargs)
	# 	categoies = Category.objects.all()
	# 	choices_list = []
	# 	for c in categoies:
	# 		value_id = c.id
	# 		value = c
	# 		choices_list.append((value_id, value))

	# 	self.fields['category'].choices = choices_list

class CategoryForm(InitializeForm):
	category_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'类别名称'}))
	p_category = forms.ChoiceField(required=False, widget=forms.Select(
		attrs={'class':'form-control'}))
	isIncome = forms.ChoiceField(required=True, choices=(('1', '收入'), ('0', '支出')), widget=forms.Select(
		attrs={'class':'form-control'}))

	def clean_category_name(self):
		category_name = self.cleaned_data['category_name']

		if len(category_name) < 2:
			raise forms.ValidationError('名称长度不能少于2个字符')
		return category_name

