import threading

from flask import Flask, request, render_template
from flask_cors import *

import Scheduler

app = Flask(__name__)
# 支持跨域
CORS(app, resources=r'/*')

# 收集数据缓存
collected_data = []

# 在校学生数（可调）
num_students = 21
# 每周班数：7*3
num_classes = 21


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
