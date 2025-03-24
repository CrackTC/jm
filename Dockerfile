FROM python:3.13-slim
RUN apt update && apt install -y git imagemagick
COPY ./policy.xml /etc/ImageMagick-6/policy.xml
RUN pip install --no-cache-dir git+https://github.com/hect0x7/JMComic-Crawler-Python flask
COPY . /app
WORKDIR /app
ENV PORT=5000
CMD ["python", "main.py"]
