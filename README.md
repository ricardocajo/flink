Tables:

    CREATE TABLE alerts (
      alert_id INT,
      host STRING,
      status STRING,
      os_type STRING,
      ts TIMESTAMP(3)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'alerts',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );

    CREATE TABLE alerts_windows (
      alert_id INT,
      host STRING,
      status STRING,
      os_type STRING,
      ts TIMESTAMP(3)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'alerts-windows',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );

    CREATE TABLE alerts_linux (
      alert_id INT,
      host STRING,
      status STRING,
      os_type STRING,
      ts TIMESTAMP(3)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'alerts-linux',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );


Put a diagram in readme with architecture?