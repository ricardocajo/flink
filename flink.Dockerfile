FROM flink:1.18.1-scala_2.12-java11

RUN wget -P /opt/flink/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar && \
    wget -P /opt/flink/lib https://jdbc.postgresql.org/download/postgresql-42.7.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.1-1.17/flink-connector-jdbc-3.1.1-1.17.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/seatunnel/flink-sql-connector-jdbc/2.1.3/flink-sql-connector-jdbc-2.1.3.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/flink/flink-sql-avro/1.18.1/flink-sql-avro-1.18.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/flink/flink-avro/1.18.1/flink-avro-1.18.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/flink/flink-avro-confluent-registry/1.18.1/flink-avro-confluent-registry-1.18.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.18.1/flink-sql-avro-confluent-registry-1.18.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/org/apache/avro/avro/1.11.3/avro-1.11.3.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.16.1/jackson-databind-2.16.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.16.1/jackson-core-2.16.1.jar && \
    wget -P /opt/flink/lib https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.16.1/jackson-annotations-2.16.1.jar
