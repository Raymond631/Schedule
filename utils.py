import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import redis

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

# 邮件配置
account = config["account"]
receiver = config["receiver"]
smtp_host = config["smtp_host"]
password = config["password"]
# redis配置
host = config["redis"]["host"]
port = config["redis"]["port"]
pwd = config["redis"]["password"]
db = config["redis"]["db"]
redis_db = redis.StrictRedis(host=host, port=port, password=pwd, db=db)


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
    for row in table:
        print(row)
    return table


def send_email(msg, data, success):
    custom_css = """
    <style>
        table {
            border-collapse: collapse;
            text-align: center;
            border: 2px;
        }
        td {
            text-align: center;
            border: 1px solid black;
            padding: 10px;
            font-size: 20px;
        }
        th {
            text-align: center;
            border: 1px solid black;
            padding: 10px;
            font-size: 20px;
        }
    </style>
    """

    # 文本消息
    text_message = MIMEText(msg, 'html', 'utf-8')
    # 表格消息
    if success:
        html_table = pd.DataFrame(data).to_html(index=False, header=False)  # index为行号，header为列名
        full_html = custom_css + html_table
        table_message = MIMEText(full_html, 'html')
    else:
        html_table = pd.DataFrame(data).to_html(index=False)
        full_html = custom_css + html_table
        table_message = MIMEText(full_html, 'html')

    message = MIMEMultipart()
    message['From'] = account
    message['Subject'] = '网服排班结果'
    message.attach(text_message)
    message.attach(table_message)
    try:
        s = smtplib.SMTP_SSL(smtp_host, 465)
        s.login(account, password)
        s.sendmail(account, receiver, message.as_string())
        s.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


# 存入redis
def put_into_redis(data):
    # 如果name已存在，会更新数据
    redis_db.hset("collected_data", data.get("name"), json.dumps(data))
    # 返回数据长度
    return redis_db.hlen("collected_data")


# 从redis取出
def get_from_redis():
    collected_data = redis_db.hgetall("collected_data")
    decoded_data = [json.loads(value) for value in collected_data.values()]
    return decoded_data


# 从redis删除
def delete_from_redis(name):
    redis_db.hdel("collected_data", name)


# 清空redis
def clear_collected_data():
    redis_db.delete("collected_data")
    print("缓存已清空")
