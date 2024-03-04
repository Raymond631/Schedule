# Schedule

### 前端
* 主程序：ScheduleForm/index.html
* 技术栈：html+JQuery
#### 部署：
1. 用nginx部署前端页面
2. 通过nginx反向代理后端，将前端发送的/api请求转发到后端

### 后端
* 主程序：web.py
* 技术栈：Python Flask
* 排班算法：回溯
* 结果展示方式：邮件通知（需配置授权码）
#### 部署：
1. 创建并进入虚拟环境
2. 安装依赖：pandas、flask、flask_cors
3. 启动：nohup ./venv/bin/python -u ./web.py >> ./log 2>&1 &

### 部署注意事项
1. 放开防火墙对应的端口
2. 修改云服务器安全组
