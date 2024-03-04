# Schedule

### 前端
* 主程序：templates/index.html
* 技术栈：html+JQuery


### 后端
* 主程序：web.py
* 技术栈：Python Flask
* 排班算法：回溯
* 结果展示方式：邮件通知（需配置smtp用户名和密码）

### 直接部署：
1. 创建并进入虚拟环境
2. 安装依赖：pip install -r requirements.txt
3. 启动：nohup ./venv/bin/python -u ./web.py >> ./log 2>&1 &

### docker部署:
1. 编辑 `config.json` 和 `compose.yaml`
2. docker compose up -d

### 部署注意事项
1. 放开防火墙对应的端口
2. 修改云服务器安全组
