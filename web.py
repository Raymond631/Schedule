import csv
import json
import threading

from flask import Flask, request, render_template

import Scheduler
import utils

app = Flask(__name__)

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)
# 在校学生数（可调）
num_students = config["num_students"]
# 每周班数：7*3
num_classes = config["num_classes"]

people = {}
with open('resource/people.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        people[row['name']] = row['level']


@app.route('/', methods=['get'])
def entrypoint():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(f"收到数据: {data}")
    # 插入redis（重复提交可以覆盖）
    length = utils.put_into_redis(data)

    if length >= num_students:
        print("收集完毕")
        # 从redis取出所有数据
        collected_data = utils.get_from_redis()
        thread = threading.Thread(target=Scheduler.start, args=(collected_data, num_students, num_classes))
        thread.start()
    return 'OK'


@app.route('/look', methods=['get'])
def look():
    collected_data = utils.get_from_redis()
    # 未提交人员名单
    missing_names = [name for name in people.keys() if name not in set(item['name'] for item in collected_data)]
    return render_template("look.html", collected_data=collected_data, missing_names=missing_names)


# 特殊情况下，可用于删除某个提交（如name输错）
@app.route('/delete', methods=['get'])
def delete():
    name = request.args.get('name')
    utils.delete_from_redis(name)
    s = f"已删除name={name}的提交"
    print(s)
    return s


@app.route('/preview', methods=['get'])
def preview():
    # 获取参数列表并转换为list
    name = request.args.get('name')
    user_id = request.args.get('userId')
    time_list = eval(request.args.get('data'))
    data = {"name": name, "userId": user_id, "timeList": time_list}
    return render_template("preview.html", data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
