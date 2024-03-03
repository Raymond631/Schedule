import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd

# 邮件设置
account = 'raymondli631@163.com'
receiver = ['raymondli631@qq.com', '1526960441@qq.com']
# TODO 配置授权码
password = ''


def to_table(data):
    # 在第一行前面插入一行作为行头
    header_row = ['时间', '周一', '周二', '周三', '周四', '周五', '周六', '周日']
    table = [header_row]

    # 将行头和数据填入7列3行的表格中
    days = ['10:00-11:40', '14:10-15:50', '15:50-17:30']
    for i in range(3):
        row = [days[i]]
        for j in range(7):
            index = j * 3 + i  # 按列顺序获取元素的索引
            if index < len(data):
                row.append(data[index])
            else:
                row.append('')
        table.append(row)
    print("排班结果：")
    print(table)
    return table

    # # 将表格输出到CSV文件
    # with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(table)
    # print("排班文件已生成：output.csv")


def send_email(data, msg_type):
    message = MIMEMultipart()
    message['From'] = account
    message['Subject'] = '网服排班结果'

    if msg_type == "table":
        html_table = pd.DataFrame(data).to_html(index=False, header=False)
        body = MIMEText(html_table, 'html', 'utf-8')
        message.attach(body)
    else:
        message.attach(MIMEText(data, 'plain', 'utf-8'))

    try:
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        s.login(account, password)
        s.sendmail(account, receiver, message.as_string())
        s.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
