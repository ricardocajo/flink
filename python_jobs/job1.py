from pyflink.table import EnvironmentSettings, TableEnvironment

table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
table_env.get_config().set("parallelism.default", "1")

# Define your CREATE TABLE statements
create_table_alerts = """
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
"""

create_table_windows_sink = """
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
"""

# Execute CREATE TABLE statements
table_env.execute_sql(create_table_alerts)
table_env.execute_sql(create_table_windows_sink)

# Define your INSERT INTO query
insert_query = """
    INSERT INTO alerts_windows
    SELECT alert_id, host, status, os_type, ts FROM alerts WHERE os_type = 'windows'
"""

# Execute the INSERT INTO query
table_env.execute_sql(insert_query).wait()
