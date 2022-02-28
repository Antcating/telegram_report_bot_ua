FROM python:3.9
RUN apt update
WORKDIR /app
COPY requirements.txt /tmp/
RUN pip install \
    --no-cache-dir \
    -r /tmp/requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "python3", "main.py" ]

