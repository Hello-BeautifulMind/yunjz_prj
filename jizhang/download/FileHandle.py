import xlwt
from io import BytesIO
from django.http import HttpResponse

def set_style(name='Times New Roman', height=260, bold=False, num_format_str=None):
	style = xlwt.XFStyle()	# 初始化样式

	if num_format_str: style.num_format_str = num_format_str

	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font

	# 设置居中
	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER		# 水平居中
	alignment.vert = xlwt.Alignment.VERT_CENTER		# 再垂直居中
	style.alignment = alignment
	return style

def write_excel(data):
	wb = xlwt.Workbook()		# 创建工作簿

	sheet1 = wb.add_sheet("收支", cell_overwrite_ok=True)

	# 表头
	title = '账单明细'
	sheet1.write_merge(0, 0, 0, 3, title, set_style(height=270, bold=True))

	# 字段称呼
	row2 = ['时间', '金额', '分类', '备注']
	for col, value in enumerate(row2):
		sheet1.col(col).width = 256 * 20
		sheet1.write(1, col, value, set_style(bold=True))

	# 写入数据
	for row, obj in enumerate(data):
		row += 2
		sheet1.write(row, 0, obj.pub_date, set_style(num_format_str='M/D/YY'))
		sheet1.write(row, 1, obj.price, set_style(num_format_str='$#,##0.00'))	
		sheet1.write(row, 2, obj.category.name, set_style())
		sheet1.write(row, 3, obj.comment, set_style())

	#wb.save('bill.xls')
	bio = BytesIO()
	wb.save(bio)
	bio.seek(0)
	print('数据.....')
	
	response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=bill.xls'.encode()
	return response


if __name__ == '__main__':
	write_excel([])
	print('创建成功')