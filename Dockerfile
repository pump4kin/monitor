# 使用官方Python基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器中
COPY ../../PyProject/monitor /app

# 安装依赖
RUN pip install --index-url=https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt

# 安装supervisor
RUN pip install --index-url=https://mirrors.aliyun.com/pypi/simple/ supervisor==4.2.5

# 复制supervisor配置文件
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露端口
EXPOSE 5000

# 运行Flask应用
#CMD ["flask", "run"]

# 运行supervisord
CMD ["/usr/local/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
