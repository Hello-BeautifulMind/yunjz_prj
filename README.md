# 网络记账
- 学习Web开发整个流程
- 学习利用Bootstrap前端框架设计UI，使用jQuery和Ajax技术提高用户体验和开发效率
- 掌握利用Django开发Web应用流程以及理解Django的MVC设计理念
- 提高对Python编程和Mysql技能的熟悉度
- 掌握在Linux系统上搭建Web应用开发环境以及提高Git技能的熟练度
- 掌握使用Nginx+uWSGI+Django方法部署Django程序
- 如何为项目书写README.md文档
- 最后一个就是善用搜索引擎解决问题的能力
***
## 内容
* [项目介绍](#项目介绍)
* [环境介绍](#环境介绍)
* [本地运行项目](#本地运行项目)
* [项目演示](#项目演示)

### 项目介绍
-----------
实现基本的日常收入和开销管理，解决基本的记账需求，主要包括几大模块：
* 用户账号管理模块，每个用户只能管理属于自己的账单信息
* 账单分类管理模块，用户为账单进行分类管理，还可以导出进行统计分析
* 账单明细管理模块，用户查看某一分类下的所有账单，可以导出进行分析
* 分页功能：实现分页栏设计

### 环境介绍
-----------
* CentOS7
* Python 3.5.1
* Django1.11.1
  
### 本地运行项目
-----------
1. 克隆项目到本地

   打开命令行，进入到保存项目的文件夹，输入如下命令：

   ```
   git clone https://github.com/Hello-BeautifulWorld/yunjz_prj.git
   ```
 2. 创建并激活虚拟环境

   在命令行进入到保存虚拟环境的文件夹，输入如下命令创建并激活虚拟环境：

   ```
   python -m venv yunjz_venv

   # windows
   yunjz_env\Scripts\activate

   # linux
   source yunjz_env/bin/activate
   ```

   如果不想使用虚拟环境，可以跳过这一步。
   
 3. 安装项目依赖

   如果使用了虚拟环境，确保激活并进入了虚拟环境，在命令行进入项目所在的 yunjz_prj 文件夹，运行如下命令：

   ```
   pip install -r requirements.txt
   ```
 4. 数据库迁移

   在上一步所在的位置运行如下命令迁移数据库：

   ```
   python manage.py migrate
   ```
 5. 创建后台管理员账户

   在上一步所在的位置运行如下命令创建后台管理员账户

   ```
   python manage.py createsuperuser
   ```
 6. 启动应用服务器

   在上一步所在的位置运行如下命令开启开发服务器：

   ```
   python manage.py runserver
   ```
7. 注册用户登录账单管理页面

   在浏览器输入：127.0.0.1:8000/accounts

### 项目演示
-----------
[项目演示](http://www.letmego.me/accounts)



