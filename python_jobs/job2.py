from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaOffsetsInitializer, KafkaRecordSerializationSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema, JsonRowSerializationSchema
from pyflink.table.table_environment import StreamTableEnvironment

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
# Create a TableEnvironment
t_env = StreamTableEnvironment.create(env)


# Define the deserialization schema for Kafka consumer
row_type_info = Types.ROW_NAMED(['alert_id', 'host', 'status', 'os_type', 'ts'],
                                [Types.INT(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()])
json_deserialization_schema = JsonRowDeserializationSchema.builder().type_info(row_type_info).build()

# Define the KafkaSource using the builder syntax
source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_topics("alerts") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(json_deserialization_schema) \
    .build()  

# Add KafkaSource as a source to the environment
ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")


# Filter records where "behavior" is equal to "pv1"
filtered_ds = ds.filter(lambda value: value['os_type'] == 'linux')

# Register the DataStream as a temporary table
#t_env.create_temporary_view("my_table", ds)
# Use SQL-like expressions to filter records
#filtered_table = t_env.sql_query("SELECT * FROM my_table WHERE os_type = 'linux'")
# Convert the result back to a DataStream
#filtered_ds = t_env.to_data_stream(filtered_table)

# Define the serialization schema for Kafka producer
json_serialization_schema = JsonRowSerializationSchema.builder().with_type_info(row_type_info).build()

sink = KafkaSink.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
            .set_topic("alerts-linux")
            .set_value_serialization_schema(json_serialization_schema)
            .build()
    ) \
    .build()

# Add KafkaSink as a sink to the environment
filtered_ds.sink_to(sink)


# Execute the job
env.execute()
