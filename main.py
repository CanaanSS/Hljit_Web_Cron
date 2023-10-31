import requests
from bs4 import BeautifulSoup
import os
import schedule
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# 初始化web_list
web_list = [
    {"name": "教务科", "url": "http://www.hljit.edu.cn/Category_581/Index.aspx"},
    {"name": "考务科", "url": "http://www.hljit.edu.cn/Category_582/Index.aspx"},
    {"name": "信息管理科", "url": "http://www.hljit.edu.cn/Category_586/Index.aspx"},
    # 添加更多网站
]
# 存储被通知的邮箱
notice_list = ["12345@qq.com","12345s@qq.com"]  # 添加通知邮箱地址

# 检测log.txt文件是否存在，如不存在则创建
if not os.path.isfile("log.txt"):
    with open("log.txt", "w", encoding="utf-8") as log_file:
        log_file.write("Log Created|{}\n".format(datetime.datetime.now()))

# 辅助函数：发送邮件通知
def send_email(subject, message, to_email):
    from_email = ""  # 发件人邮箱
    from_name = "Stsbot"
    password = ""  # 发件人邮箱密码

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email

    text = MIMEText(message, "html")
    msg.attach(text)

    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.126.com", 465, context=context)#将smtp.126.com更改为发件邮箱的SMTP服务器
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

# 构建HTML格式的邮件内容
def build_email_content(website_name, new_links):
    email_content = f"<h1>{website_name}通知页面有内容更新</h1>\n"
    email_content += "<h3>新增通知：</h3>\n"

    for link in new_links:
        link_url, link_text = link.split("|", 1)
        email_content += f"{link_text}<a href='http://www.hljit.edu.cn/{link_url}' target='_blank'>http://www.hljit.edu.cn/{link_url}</a><br>\n"

    return email_content

# 访问网页、抓取链接并记录到文件
def scrape_website(url, name):
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            links_info = [f"{link.get('href')}|{link.text.strip()}" for link in links]

            # 检查是否存在对应的文件
            filename = f"{name}.txt"
            temp_filename = f"{name}_temp.txt"

            if not os.path.isfile(filename):
                with open(filename, "w", encoding="utf-8") as file:
                    pass

            with open(temp_filename, "w", encoding="utf-8") as temp_file:
                temp_file.write("\n".join(links_info))

            with open(filename, "r", encoding="utf-8") as file:
                existing_links = set(file.read().splitlines())

            with open(temp_filename, "r", encoding="utf-8") as temp_file:
                new_links = set(temp_file.read().splitlines())

            diff = new_links.difference(existing_links)

            if diff:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write("\n" + "\n".join(diff))

                # 发送邮件通知
                subject = f"{name}通知页面有内容更新"
                email_content = build_email_content(name, diff)
                for recipient in notice_list:
                    if send_email(subject, email_content, recipient):
                        print("New links notification sent.")
                # 记录删除记录至log.txt文件中
                with open("log.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"{name} Updated|{datetime.datetime.now}\n")

                print("New links recorded.")

            os.remove(temp_filename)

        else:
            current_time = datetime.datetime.now()
            if 8 <= current_time.hour < 21 and status_code != 200:
                print(f"Status code is not 200. Sleeping for 10 minutes...")
                time.sleep(600)  # 10 minutes sleep
            elif current_time.hour >= 21:
                sleep_duration = (datetime.datetime(current_time.year, current_time.month, current_time.day, 21, 30) - current_time).seconds
                print(f"Sleeping until 8:00 AM...")
                time.sleep(sleep_duration + 3600)  # Sleep until 8:00 AM

    except Exception as e:
        print(f"Error while scraping {name}: {str(e)}")

# 定时任务
for website in web_list:
    schedule.every(30).seconds.do(scrape_website, website["url"], website["name"])

# 开始执行定时任务
while True:
    schedule.run_pending()
    time.sleep(1)
