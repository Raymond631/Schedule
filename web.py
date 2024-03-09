import threading
import json

from flask import Flask, request, render_template

import Scheduler

app = Flask(__name__)

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

# 收集数据缓存
collected_data = []

# 在校学生数（可调）
num_students = config["num_students"]
# 每周班数：7*3
num_classes = config["num_classes"]


@app.route('/', methods=['get'])
def entrypoint():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(f"Received data: {data}")
    collected_data.append(data)

    if len(collected_data) == num_students:
        print("收集完毕")
        thread = threading.Thread(target=Scheduler.start, args=(collected_data, num_students, num_classes))
        thread.start()
    return 'OK'


@app.route('/look', methods=['get'])
def look():
    # 按照'id'键对字典列表进行排序
    sorted_data = sorted(collected_data, key=lambda x: x['userId'])
    return render_template("look.html", data=sorted_data)


@app.route('/delete', methods=['get'])
def delete():
    collected_data.clear()
    print("缓存已手动清空")
    return "缓存已手动清空"


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
