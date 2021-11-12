FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "8082"]