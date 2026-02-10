FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
WORKDIR /app/src
CMD ["python", "run.py", "--dry-run"]
