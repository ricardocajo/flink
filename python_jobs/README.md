from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer, KafkaSink, KafkaRecordSerializationSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema, JsonRowSerializationSchema

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()


# Define the schema for Kafka
row_type_info = Types.ROW_NAMED(['user_id', 'item_id', 'category_id', 'behavior', 'ts'],
                                [Types.BIG_INT(), Types.BIG_INT(), Types.BIG_INT(), Types.STRING(), Types.STRING()])
#json_deserialization_schema = JsonRowDeserializationSchema.builder().type_info(row_type_info).ignore_parse_errors().build()

# Custom JsonRowDeserializationSchema to handle parsing errors
class CustomJsonRowDeserializationSchema(JsonRowDeserializationSchema):
    def deserialize(self, message):
        try:
            return super().deserialize(message)
        except Exception as e:
            # Handle parsing errors (e.g., log the error or process the error differently)
            print(f"Error deserializing record: {e}")
            return {'original_json': message.decode('utf-8')}

json_deserialization_schema = CustomJsonRowDeserializationSchema.builder().type_info(row_type_info).build()

# Define the KafkaSource using the builder syntax
source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_topics("source") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(json_deserialization_schema) \
    .build()

ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Source")



# Filter out records with parsing errors
error_records = ds.filter(lambda value: 'original_json' in value)
valid_records = ds.filter(lambda value: 'original_json' not in value)



json_serialization_schema = JsonRowSerializationSchema.builder().with_type_info(row_type_info).build()

valid_records_sink = KafkaSink.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
            .set_topic("sink")
            .set_value_serialization_schema(json_serialization_schema)
            .build()
    ) \
    .build()

error_row_type_info = Types.ROW_NAMED(['original_json'],
                                [Types.STRING()])
json_error_serialization_schema = JsonRowSerializationSchema.builder().with_type_info(error_row_type_info).build()

error_records_sink = KafkaSink.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
            .set_topic("sink_error")
            .set_value_serialization_schema(json_error_serialization_schema)
            .build()
    ) \
    .build()

# Add KafkaSink as a sink to the environment
error_records.sink_to(error_records_sink)
valid_records.sink_to(valid_records_sink)


# Execute the job
env.execute()