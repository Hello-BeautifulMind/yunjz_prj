from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	INCOM_CHOICES = (			# 下拉选项
			(True, "收入"),
			(False, "支出"),
		)
	p_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类名称",			# 外键指向自身，因为父类名称也属于Category模型
			related_name="childs"
		)
	name = models.CharField(max_length=20, verbose_name="类别名称")
	isIncome = models.BooleanField(choices=INCOM_CHOICES, verbose_name="是否收入")
	user = models.ForeignKey(User, verbose_name="所属用户")

	class Meta:
		unique_together = (('user', 'name'),)			# 每个用户自身的分类是唯一的

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.id, self.name)

class Item(models.Model):
	price = models.DecimalField(max_digits=20, decimal_places=2, null=True, verbose_name="金额")
	pub_date = models.DateField(verbose_name="日期")
	comment = models.CharField(max_length=200, blank=True, verbose_name="注释")
	category = models.ForeignKey(Category, blank=True, null=False, verbose_name="分类", related_name="items")

	class Meta:
		ordering = ['-pub_date']			# 每次返回数据是都是返回pub_date最近的数据