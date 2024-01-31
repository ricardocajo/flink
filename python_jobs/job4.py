from pyflink.table.table_environment import StreamTableEnvironment
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.table.schema import Schema

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
# Create a TableEnvironment
t_env = StreamTableEnvironment.create(env)


# Define the schema for Kafka
row_type_info = Types.ROW_NAMED(['user_id', 'item_id', 'category_id', 'behavior', 'ts', 'original_json'],
                                [Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()])
json_deserialization_schema = JsonRowDeserializationSchema.builder().type_info(row_type_info).ignore_parse_errors().build()

# Custom JsonRowDeserializationSchema to handle parsing errors
"""class CustomJsonRowDeserializationSchema(JsonRowDeserializationSchema):
    def deserialize(self, message):
        try:
            deserialized_data = super().deserialize(message)
            
             # Explicitly cast 'user_id' to string
            deserialized_data['user_id'] = str(deserialized_data['user_id'])
            deserialized_data['item_id'] = str(deserialized_data['item_id'])
            deserialized_data['category_id'] = str(deserialized_data['category_id'])
            # Add the 'original_json' field to the deserialized data
            deserialized_data['original_json'] = None
            
            return deserialized_data
        except Exception as e:
            # Handle parsing errors (e.g., log the error or process the error differently)
            print(f"Error deserializing record: {e}")
            # Return the 'original_json' field along with other fields set to None
            return {
                'user_id': None,
                'item_id': None,
                'category_id': None,
                'behavior': None,
                'ts': None,
                'original_json': message.decode('utf-8')
            }


json_deserialization_schema = CustomJsonRowDeserializationSchema.builder().type_info(row_type_info).build()
"""
# Define the KafkaSource using the builder syntax
source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_topics("source") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(json_deserialization_schema) \
    .build()

ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Source")

"""schema = Schema.new_builder() \
    .column("user_id", "BIGINT") \
    .column("item_id", "BIGINT") \
    .column("category_id", "BIGINT") \
    .column("behavior", "STRING") \
    .column("ts", "TIMESTAMP(3)") \
    .column("original_json", "STRING") \
    .build()"""

# interpret the insert-only DataStream as a Table
source_table = t_env.from_data_stream(ds)

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
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
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
        'properties.bootstrap.servers' = 'kafka-kafka-bootstrap:9092',
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