FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

# 给脚本添加执行权限
RUN chmod +x ./startasdfasdf.sh

# 直接运行脚本
CMD ["./start.sh"]
