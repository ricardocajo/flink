"""
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema

json_deserialization_schema = JsonRowDeserializationSchema.builder().type_info(row_type_info).build()

# Define the KafkaSource using the builder syntax
source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka-kafka-bootstrap:9092") \
    .set_topics("alerts") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(json_deserialization_schema) \
    .build()

# Add KafkaSource as a source to the environment
ds = env.from_source(data_gen_source, WatermarkStrategy.no_watermarks(), "DataGen Source")
"""
from pyflink.common import Types, WatermarkStrategy