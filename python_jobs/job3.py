from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col, call

table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
table_env.get_config().set("parallelism.default", "1")

create_table_linux_sink = """
    CREATE TABLE alerts_linux (
      alert_id INT,
      host STRING,
      status STRING,
      os_type STRING,
      ts STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'alerts-linux',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );
"""
table_env.execute_sql(create_table_linux_sink)

# Create the table from a sql query
table = table_env.sql_query("SELECT * FROM alerts_linux")

result_table = table \
    .group_by(col("alert_id"), col("os_type")) \
    .select(col("alert_id"), col("os_type"), call("count", col("alert_id")).alias("_count_"))


result_table.execute().print()
