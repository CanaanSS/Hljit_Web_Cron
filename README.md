# Hljit_Web_Cron
监控黑龙江工程学院官网的超链接的变化，并在发生变化时将变动邮件通知到指定邮箱。

本来想简称HGC_Wc来着，后来想了想不太文明，就Wec吧

#### 问题声明

目前已知仍存在部分问题

1. 在官网夜间关闭期间，可能存在不稳定问题，目前尚在调试中。

#### 项目说明

起因是我所在的二级学院教务处老师转达消息太慢，以至于班级同学已经从别的学院听说了某个通知而我这个班长还毫不知情。。。。。。

正好各种通知教务处都会在官网发布公告而这学期的专业课又是Python。。。干脆写个脚本自动抓通知吧

初学者代码比较烂而且也没啥稀奇功能，大佬们手下留情。。。

### 文件结构及说明

- links
   - config
    
    网址1 特征码
  
    网址2 特征码
    
     . . . . . .

   - 通知公告.txt
    
     内置了2023-08-29 21:51:31前 http://www.hljit.edu.cn/Category_296/Index.aspx 的页面信息

   - 文件下载.txt
    
     内置了2023-08-29 21:51:21前 http://www.hljit.edu.cn/Category_298/Index.aspx 的页面信息

- main.py
  
  第11行中的‘my_sender’值修改为发件邮箱
  
  第12行中的‘my_user’值修改为邮箱用户名
  
  第13行中的‘my_pass’值修改为邮箱授权码（密码）
  
  第20行中的 ‘stmp.126.com’ 改为自己邮箱服务商的SMTP地址
  
  第20行中的‘465’为SMTP服务器的端口，此脚本默认开启SSL安全连接，接口465尽量保持不变


- no-gui.py
  
  与main.py使用方法无异
  
  主程序的无输入版本，将main.py中需输入的数值设置为常量，适合托管到服务器运行
