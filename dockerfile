FROM nvcr.io/nvidia/pytorch:23.07-py3
WORKDIR /app
COPY requirements-docker.txt /app
RUN pip install -r requirements-docker.txt
COPY . /app