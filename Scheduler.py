from utils import to_table, send_email, clear_collected_data


class Scheduler:
    def __init__(self, num_students, num_classes, students_availability):
        self.num_students = num_students
        self.num_classes = num_classes
        self.students_availability = students_availability
        self.class_schedule = [0] * num_classes  # 存储每个班次的学生编号
        self.result = False

    def schedule_classes(self, current_class):
        if current_class == self.num_classes:
            self.result = True
            return
        for student in range(self.num_students):
            # 如果学生在当前班次有空，且还没有被排班
            if self.students_availability[student][current_class] == 0 and (student + 1) not in self.class_schedule:
                self.class_schedule[current_class] = (student + 1)  # 将学生安排到当前班次
                self.schedule_classes(current_class + 1)  # 递归调用安排下一个班次的学生
                if self.result:  # 如果找到了有效排班方案，直接结束递归
                    return
                self.class_schedule[current_class] = 0  # 回溯，将当前班次的学生清空


def process(num_students, num_classes, students_availability, name_list):
    result = []
    scheduler = Scheduler(num_students, num_classes, students_availability)
    # 从第一个班次开始安排
    scheduler.schedule_classes(0)
    if scheduler.result:
        print("成功找到排班方案")
        for v in scheduler.class_schedule:
            result.append(name_list[v - 1])
    else:
        print("未找到有效排班方案")
    return result


def start(collected_data, num_students, num_classes):
    name_list = [item["name"] for item in collected_data]
    time_list = [item["timeList"] for item in collected_data]  # 每一行代表一个学生，0表示空闲，1表示忙碌
    print("收集数据如下：")
    print(name_list)
    for row in time_list:
        print(row)

    result = process(num_students, num_classes, time_list, name_list)
    if len(result) > 0:
        table = to_table(result)
        send_email("成功找到排班方案", table, True)
    else:
        send_email("未找到有效排班方案，请根据下面的数据手动调整（0表示空闲，1表示忙碌）：", collected_data, False)

    # 清空缓存，以待下次收集
    clear_collected_data()

# def mock(num_students):
#     collected_data = []
#     for _ in range(num_students):
#         collected_data.append({
#             "name": ''.join(random.choice(string.ascii_letters) for i in range(6)),
#             "userId": random.randint(100, 1000),
#             "timeList": [random.choice([0, 1]) for _ in range(21)]
#         })
#     return collected_data
#
#
# if __name__ == '__main__':
#     start(mock(21), 21, 21)
