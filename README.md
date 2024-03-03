# Schedule

### 前端
主程序：ScheduleForm/index.html
技术栈：html+JQuery
#### 部署：
用nginx部署即可

### 后端
主程序：web.py
技术栈：Python Flask
排班算法：回溯
结果展示方式：邮件通知
#### 部署：
1. 创建并进入虚拟环境
2. 安装依赖：pandas、flask、flask_cors
3. 启动：nohup ./venv/bin/python ./web.py >> ./log 2>&1 &
