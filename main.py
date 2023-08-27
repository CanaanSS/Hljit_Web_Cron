import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import re

# 发件邮箱配置
my_sender = ''
my_user = ''
my_pass = ''


def send_mail(to_list, sub, content):
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = Header(sub, 'utf-8')

    try:
        s = smtplib.SMTP_SSL("smtp.126.com", 465)
        s.login(my_sender, my_pass)
        s.sendmail(my_sender, to_list, msg.as_string())
        print("邮件发送成功")
    except s.SMTPException:
        print("Error: 无法发送邮件")


# 获取输入的邮箱和秒数
emails = input("请输入邮箱(多个用+++隔开):")
seconds = int(input("请输入秒数:"))
email_list = emails.split('+++')

with open('./links/config', encoding='utf-8') as f:
  lines = f.readlines()

urls = []
codes = []

for line in lines:
  url, code = line.split()
  urls.append(url)
  codes.append(code)

# 更新链接文件函数
def update_links_file(filename, new_links):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.readlines()

    old_links = [i.strip() for i in content[1:]]

    add_links = []
    for x in new_links:
        if "/Category_" not in x and x not in old_links:
            add_links.append(x)

    if add_links:

        with open(filename, 'a', encoding='utf-8') as f:

            f.write('\n')

            for x in add_links:
                link_str = x.strip()

                link_name = link_str.split(' ')[0]
                link_url = ' '.join(link_str.split(' ')[1:])

                f.write(f'{link_name} {link_url}\n')

    return add_links


# 检查是否存在links目录,不存在则创建

if not os.path.exists('./links'):
    os.makedirs('./links')

# 向邮箱发送配置成功提示
send_mail(email_list, '教务通知监控', '监控系统启动成功，若有新通知则通知至此邮箱，收到此邮件暨系统运行正常。\n From 636.')

while True:
    for i in range(len(urls)):
        url = urls[i]
        code = codes[i]

        # 判断状态码
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.ConnectionError:
        now = time.localtime()
        if now.tm_hour >= 8 and now.tm_hour <= 23:
            print('连接异常,暂停15分钟')
            time.sleep(15 * 60)
        else:
            print('连接异常,暂停到8点')
            while now.tm_hour < 8:
                time.sleep(600)
                now = time.localtime()

        if res.status_code == 200:
            print(f'{url} 状态码正常,继续运行')
        else:
            now = time.localtime()
            if now.tm_hour >= 8 and now.tm_hour <= 23:
                print(f'{url}状态码异常,暂停15分钟后继续')
                time.sleep(900)
            else:
                print(f'{url}状态码异常,暂停到8:00后继续')
                while True:
                    if time.localtime().tm_hour >= 8:
                        break
                    time.sleep(300)

        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a')

            filename = './links/' + code + '.txt'

            if not os.path.exists(filename):
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n')

            with open(filename, 'r', encoding='utf-8') as f:
                content = f.readlines()

            old_links = [i.strip() for i in content[1:]]

            new_links = []
            for link in links:
                new_links.append(link.text + ' ' + link.get('href'))

            add_links = update_links_file(filename, new_links)

            if add_links:
                content = f'检测到{code}Page更新了内容:</br>'

                for x in add_links:
                    link_name, link_url = x.split(' ')
                    content += f'{link_name}</br>'
                    content += f'<a href="http://www.hljit.edu.cn{link_url}">http://www.hljit.edu.cn{link_url}</a></br>'
                    content += '请及时关注!</br>'
                    content += 'From Fraic Tool.</br>'
                msg = MIMEText(content, _subtype='html', _charset='utf-8')
                msg['Subject'] = 'Page内容·更新通知'  # 标题为纯文本
                print('检测到新链接,发送邮件通知...')
                send_mail(email_list, 'Page内容·更新通知', content)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n')
                for x in new_links:
                    f.write(x + '\n')

        except Exception as e:
            print('Error:', e)

        finally:
            time.sleep(seconds)