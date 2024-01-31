from pyflink.table.table_environment import StreamTableEnvironment
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream.serialization import SimpleDeserializationSchema
import json

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
# Create a TableEnvironment
t_env = StreamTableEnvironment.create(env)


# Define the schema for Kafka
row_type_info = Types.ROW_NAMED(['user_id', 'item_id', 'category_id', 'behavior', 'ts', 'original_json'],
                                [Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()])
#json_deserialization_schema = JsonRowDeserializationSchema.builder().type_info(row_type_info).ignore_parse_errors().build()

class CustomJsonDeserializationSchema(SimpleDeserializationSchema):
    def __init__(self, row_type_info):
        self.row_type_info = row_type_info

    def deserialize(self, message):
        try:
            json_object = json.loads(message)
            user_id = json_object.get('user_id', None)
            item_id = json_object.get('item_id', None)
            category_id = json_object.get('category_id', None)
            behavior = json_object.get('behavior', None)
            ts = json_object.get('ts', None)

            return user_id, item_id, category_id, behavior, ts
        except json.JSONDecodeError:
            # Return None for malformed JSON
            return None

# Create a custom deserialization schema
custom_json_deserialization_schema = CustomJsonDeserializationSchema(row_type_info)

# Define the KafkaSource using the builder syntax
source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9095") \
    .set_topics("source") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(custom_json_deserialization_schema) \
    .build()

ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Source")

# interpret the insert-only DataStream as a Table
source_table = t_env.from_data_stream(ds, custom_json_deserialization_schema)

t_env.create_temporary_view("source", source_table)

create_table_valid_records = """
    CREATE TABLE sink (
        user_id STRING,
        item_id STRING,
        category_id STRING,
        behavior STRING,
        ts STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'sink',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9095',
        'format' = 'json'
    );
"""

create_table_error_records = """
    CREATE TABLE sink_error (
        original_json STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'sink_error',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9095',
        'format' = 'json'
    );
"""

# Execute CREATE TABLE statements
t_env.execute_sql(create_table_valid_records)
t_env.execute_sql(create_table_error_records)

stmt_set = t_env.create_statement_set()

stmt_set \
    .add_insert_sql("INSERT INTO sink SELECT user_id, item_id, category_id, behavior, ts FROM source")
stmt_set \
    .add_insert_sql("INSERT INTO sink_error SELECT original_json FROM source")

stmt_set.execute()