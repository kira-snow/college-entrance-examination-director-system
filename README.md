# gaokaospider
山西招生考试网历年院校投档线爬虫

- python3.7， scrapy爬虫
- 直接从山西招生考试网（http://www.sxkszx.cn） 获取历年高校的投档线，并且保存到excel文件中，默认从2016年起的所有数据，包括院校名称、院校代码、投档最低分数线，包含1A、1A1、2A、2B、2C、专科院校，文理分开两个sheet
- 保存院校分数线到mysql数据库，表schools；保存每年批次分数线到表levelLines；保存每年分数排名到表segments；从阳光高考网站获取院校信息保存到表schoolinfo；
- 提供按照指定线差的查询和名次查询；

## 安装依赖
依赖Scrapy==1.8.0，openpyxl==3.0.3
``` shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

Windows用户可以直接运行install_require.bat

## 安装MySQL
安装包：
https://dev.mysql.com/downloads/windows/installer/
教程：
https://www.runoob.com/w3cnote/windows10-mysql-installer.html

1. 配置用户名，密码
用户：密码：
root:  123456
sa:  123456

默认mysql 服务名：MySQL80

2. 修改默认编码规则
   C:\ProgramData\MySQL\MySQL Server 8.0\data\my.ini
   修改以下内容：
   ```
    [client]

    no-beep

    default-character-set=utf8

    [mysql]

    default-character-set=utf8
   ```

3. 修改默认数据库存储位置
   1) cmd进入控制台

   net stop MySQL80

   1) 复制原来数据库目录到新目录

   　　复制C:\ProgramData\MySQL\MySQL Server 5.5\中的data目录到
   　　D:\Program Files\MySQL\MySQL Server 5.5\目录下（自建的目录）

   2) 修改MySQL配置文件
   　　1、用记事本打开C:\ProgramData\MySQL\MySQL Server 5.5\data\目录下的my.ini
   　　找到datadir="C:\ProgramData\MySQL\MySQL Server 5.5\data"
   　　在前面加#注释掉
   　　在下面添加一行
   　　datadir="D:\Program Files\MySQL\MySQL Server 5.5\data"
   　　修改完成后，保存退出。

   3) 重新启动MySQL
   　　开始-cmd
   　　net start MySQL80

   4) 进入MySQL控制台

   　　show variables like '%datadir%'; #查询MySQL数据库存放目录 
   　　如查询显示为D:\Program Files\MySQL\MySQL Server 5.5\data\即表示修改成功！

4. 执行数据库初始化：.\sql\
``` shell
init.bat
inquire_init.bat
```

## 使用方法
1. 爬取数据
``` shell
scrapy crawl benke
```

Windows用户可以直接运行gaokaospider.bat

2. 查询数据
- 按照指定线差查询：
``` sql
call gaokao.gaokao_qry('1a', '理工', 10, 20, 2016, 2019)
```
直接调用inquire.bat，使用notepad++修改参数。
第一个参数：等级，合法输入：'1a', '1a1', '1b', '2a', '2b', '2c'；(注意必须有英文单引号)
第二个参数：文理科，合法输入：'文史', '理工'；(注意必须有英文单引号)
第三个参数：线差下限，合法输入：必须是正整数
第四个参数：线差上限，合法输入：必须是正整数
第五个参数：年份下限，合法输入：必须是合法年份
第六个参数：年份上限，合法输入：必须是合法年份

- 按照名次查询
``` sql
call gaokao.gaokao_segment_qry('1a', '理工', 2020, 621, 5, 5)
```
直接调用inquire_segment.bat，使用notepad++修改参数。
第一个参数：等级，合法输入：'1a', '1a1', '1b', '2a', '2b'；(注意必须有英文单引号)
第二个参数：文理科，合法输入：'文史', '理工'；(注意必须有英文单引号)
第三个参数：年份，合法输入：必须是高考年份
第四个参数：分数，合法输入：必须是高考总分
第五个参数：分数下限，合法输入：必须是正整数
第六个参数：分数上限，合法输入：必须是正整数