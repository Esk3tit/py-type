FROM python:3.10.10-slim-bullseye

WORKDIR /usr/src/app

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "bash" ]