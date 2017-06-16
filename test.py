from django.contrib.auth.models import User
from jizhang.models import Category, Item

def test_data():
	pwd = '123456'
	name1 = 'xiaoming'
	name2 = 'xiaohong'
	u1 = User.objects.filter(username=name1)
	u2 = User.objects.filter(username=name2)
	u1 = u1 if u1.exists() else User.objects.create_user(username=name1, password=pwd)
	u2 = u2 if u2.exists() else User.objects.create_user(username=name2, password=pwd)
	
	u_list = User.objects.filter(username__contains='xiao')
	print(u_list)
	for u in u_list:
		c1 = Category(name='salary', isIncome=True, p_category=None, user=u)
		c1.save()
		c2 = Category(name='salary_lp', isIncome=True, p_category=c1, user=u)
		c2.save()
		base_salary = 1000 if u.username == 'xiaoming' else 2000

		for i in range(10):
			price = base_salary * (1.0 + i/10.0)
			i = Item(price=price, category=c2, pub_date='2017-%d-01' % (i+1), comment='工资')
			i.save()

	print("测试数据创建成功")


def create_items():
	pwd = '123456'
	name = 'xiaoming'
	try:
		user = User.objects.get(username=name)
	except User.DoesNotExist:
		user = User.objects.create_user(username=name, password=pwd)
	#
	c = Category.objects.get(user=user, name='salary')
	base_salary = 1000
	for i in range(100):
		price = base_salary * (1 + i/10.0)
		i = Item(price=price, category=c, pub_date='2{:03}-01-01'.format(i), comment='工资%d' % i)
		i.save()
	print("测试数据创建成功")


if __name__ == "__main__":
	test_data()
