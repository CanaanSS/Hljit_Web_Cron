# Hljit_Web_Cron
监控黑龙江工程学院官网的超链接的变化，并在发生变化时将变动邮件通知到指定邮箱。


### 文件结构及说明

- links
  - config
     网址1 特征码
     网址2 特征码
     . . . . . .

  - 通知公告
     内置了2023-08-27 22:34:27前http://www.hljit.edu.cn/Category_296/Index.aspx的页面信息

  - 文件下载
     内置了2023-08-27 22:35:13前http://www.hljit.edu.cn/Category_298/Index.aspx的页面信息

- main.py
  第11行中的‘my_sender’值修改为发件邮箱\n
  第12行中的‘my_user’值修改为邮箱用户名\n
  第13行中的‘my_pass’值修改为邮箱授权码（密码）
  第21行中的 ‘stmp.126.com’ 改为自己邮箱服务商的SMTP地址
  第21行中的‘465’为SMTP服务器的端口，此脚本默认开启SSL安全连接，接口465尽量保持不变


- no-gui.py
  与main.py使用方法无异
  主程序的无输入版本，将main.py中需输入的数值设置为常量，适合托管到服务器运行
