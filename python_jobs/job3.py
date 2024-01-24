from pyflink.table import EnvironmentSettings, TableEnvironment

table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
table_env.get_config().set("parallelism.default", "1")

# Define CREATE TABLE statements
create_table_users = """
    CREATE TABLE users (
        user_id INT,
        user_value DECIMAL(8,2),
        user_name STRING,
        user_time TIMESTAMP(3),
        user_special BOOLEAN
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'users',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );
"""

create_table_messages = """
    CREATE TABLE messages (
        message_id INT,
        message_body STRING,
        message_time STRING,
        message_level INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'messages',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );
"""

create_table_results_sink = """
    CREATE TABLE results (
        user_id INT,
        user_value DECIMAL(8,2),
        message_id INT,
        message_body STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'results',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
        'format' = 'json'
    );
"""

# Execute CREATE TABLE statements
table_env.execute_sql(create_table_users)
table_env.execute_sql(create_table_messages)
table_env.execute_sql(create_table_results_sink)

# Define INSERT INTO query
insert_query = """
    INSERT INTO results
    SELECT u.user_id, u.user_value, m.message_id, m.message_body
        FROM users AS u
          JOIN messages AS m
            ON u.user_id = m.message_id;
"""

# Execute the INSERT INTO query
table_env.execute_sql(insert_query).wait()
