# ---- 基础镜像，带 Python 和系统工具 ----
FROM python:3.11-slim

# 安装依赖工具和中文OCR语言包
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-tra \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ---- 设置工作目录并复制代码 ----
WORKDIR /app
COPY . .

# ---- 安装 Python 依赖 ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- 暴露端口并运行 ----
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] where to create