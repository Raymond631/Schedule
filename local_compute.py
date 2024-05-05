import csv
import random

import utils
from Scheduler import process

people = {}
with open('resource/people.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        people[row['name']] = row['level']

# 在校学生数（可调）
num_students = len(people)
# 每周班数：7*3
num_classes = 21


# 模拟数据，仅用于测试
def mock():
    collected_data = []
    b = random.randint(0, num_students - 1)  # 偏移量
    for i in range(num_students):
        collected_data.append({
            "name": list(people.keys())[(i + b) % len(people.keys())],
            "userId": random.randint(100, 1000),
            "timeList": [random.choice([0, 1]) for _ in range(21)]
        })

    # 模拟输出
    name_list = [item["name"] for item in collected_data]
    time_list = [item["timeList"] for item in collected_data]  # 每一行代表一个学生，0表示空闲，1表示忙碌
    print("收集数据如下：")
    print(name_list)
    for row in time_list:
        print(row)
    return collected_data


# 读取收集数据
def read_data():
    file_path = 'resource/收集结果.csv'
    collected_data = []

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 跳过行头
        for row in csv_reader:
            data = {'name': row[0], 'userId': row[1]}
            timeList = []
            for entry in row[2:23]:
                if entry == '':
                    timeList.append(1)
                elif entry == '空闲':
                    timeList.append(0)
            data['timeList'] = timeList
            collected_data.append(data)
    # 模拟输出
    name_list = [item["name"] for item in collected_data]
    time_list = [item["timeList"] for item in collected_data]  # 每一行代表一个学生，0表示空闲，1表示忙碌
    print("收集数据如下：")
    print(name_list)
    for row in time_list:
        print(row)

    return collected_data


def compute(collected_data):
    # 将新队员排到前面（优先排班）
    collected_data.sort(key=lambda x: people[x['name']])
    name_list = [item["name"] for item in collected_data]
    time_list = [item["timeList"] for item in collected_data]  # 每一行代表一个学生，0表示空闲，1表示忙碌
    result = process(num_students, num_classes, time_list, name_list)
    return result


def print_result(result):
    if len(result) > 0:
        utils.to_table(result)
    else:
        print('结果为空')


if __name__ == '__main__':
    # collected_data = mock()

    collected_data = read_data()
    result = compute(collected_data)
    print_result(result)
