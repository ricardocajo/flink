FROM europe-west2-docker.pkg.dev/academy-350111/flink/flink-kafka:v2

# install python3 and pip3
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    python -m pip install apache-flink