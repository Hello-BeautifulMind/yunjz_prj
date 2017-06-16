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
* [演示地址](#演示地址)

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
   git clone https://github.com/Hello-BeautifulWorld/MyProject.git
   ```
 2. 创建并激活虚拟环境

   在命令行进入到保存虚拟环境的文件夹，输入如下命令创建并激活虚拟环境：

   ```
   virtualenv blogproject_env

   # windows
   blogproject_env\Scripts\activate

   # linux
   source blogproject_env/bin/activate
   ```

   关于如何使用虚拟环境，参阅：[搭建开发环境](http://zmrenwu.com/post/3/) 的 Virtualenv 部分。如果不想使用虚拟环境，可以跳过这一步。
   
### 示例
-----------
1. 下载文件<br>
命令：get example.avi<br> 
[客户端下载](/images/client.png)<br>
[服务端信息](/images/server.png)



