from pyflink.table import EnvironmentSettings, TableEnvironment

table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
table_env.get_config().set("parallelism.default", "1")


# Define CREATE TABLE statements
create_table_users_gen = """
    CREATE TABLE users_gen (
        user_id INT,
        user_value DECIMAL(8,2),
        user_name STRING,
        user_time TIMESTAMP(3),
        user_special BOOLEAN
    ) WITH (
        'connector' = 'datagen',
        'fields.user_id.kind' = 'sequence',
        'fields.user_id.start' = '1',
        'fields.user_id.end' = '1000',
        'number-of-rows' = '1000',
        'fields.user_name.length' = '10',
        'rows-per-second' = '10',
        'fields.user_value.min' = '10.0',
        'fields.user_value.max' = '100.0',
        'fields.user_name.kind' = 'random',
        'fields.user_special.kind' = 'random'
    );
"""

create_table_normal_users_sink = """
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

# Execute CREATE TABLE statements
table_env.execute_sql(create_table_users_gen)
table_env.execute_sql(create_table_normal_users_sink)

# Define INSERT INTO query
insert_query = """
    INSERT INTO users
    SELECT user_id, user_value, user_name, user_time, user_special FROM users_gen WHERE user_special = false AND user_value > 45.0
"""

# Execute the INSERT INTO query
table_env.execute_sql(insert_query).wait()
