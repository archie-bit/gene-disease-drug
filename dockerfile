# FROM apache/airflow:2.9.0-python3.10

# # Install additional Python packages
# RUN pip install --no-cache-dir \
#     apache-airflow-providers-amazon \
#     pyspark \
#     requests \
#     pandas


FROM apache/airflow:2.9.0-python3.10

USER root

# 1. Install OpenJDK 17 (Required for Spark) and procps (required for Spark checks)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

# 3. Install Python dependencies
RUN pip install --no-cache-dir \
    apache-airflow-providers-amazon \
    pyspark==3.5.0 \
    requests \
    pandas