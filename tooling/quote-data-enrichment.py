from pyflink.table.table_environment import StreamTableEnvironment
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types, Row
from pyflink.datastream.connectors.kafka import KafkaSink, KafkaRecordSerializationSchema
from pyflink.datastream.formats.json import JsonRowSerializationSchema

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
# Create a TableEnvironment
t_env = StreamTableEnvironment.create(env)

# Define the schema for Kafka
row_type_info = Types.ROW_NAMED([
    'recordId', 'time', 'arrivalTime',
    'bid0Price', 'bid0Ccy', 'bid0Size', 'bid0DataSource', 'bid0AgeOffsetMsecs',
    'bid1Price', 'bid1Ccy', 'bid1Size', 'bid1DataSource', 'bid1AgeOffsetMsecs',
    'bid2Price', 'bid2Ccy', 'bid2Size', 'bid2DataSource', 'bid2AgeOffsetMsecs',
    'bid3Price', 'bid3Ccy', 'bid3Size', 'bid3DataSource', 'bid3AgeOffsetMsecs',
    'bid4Price', 'bid4Ccy', 'bid4Size', 'bid4DataSource', 'bid4AgeOffsetMsecs',
    'ask0Price', 'ask0Ccy', 'ask0Size', 'ask0DataSource', 'ask0AgeOffsetMsecs',
    'ask1Price', 'ask1Ccy', 'ask1Size', 'ask1DataSource', 'ask1AgeOffsetMsecs',
    'ask2Price', 'ask2Ccy', 'ask2Size', 'ask2DataSource', 'ask2AgeOffsetMsecs',
    'ask3Price', 'ask3Ccy', 'ask3Size', 'ask3DataSource', 'ask3AgeOffsetMsecs',
    'ask4Price', 'ask4Ccy', 'ask4Size', 'ask4DataSource', 'ask4AgeOffsetMsecs'
], [
    Types.INT(), Types.BIG_INT(), Types.BIG_INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT(),
    Types.DOUBLE(), Types.STRING(), Types.INT(), Types.INT(), Types.INT()
])

t_env.execute_sql("""
    CREATE TABLE raw_data_table (
        `recordId` INT,
        `time` BIGINT,
        `arrivalTime` BIGINT,
        `bid0Price` DOUBLE,
        `bid0Ccy` STRING,
        `bid0Size` INT,
        `bid0DataSource` INT,
        `bid0AgeOffsetMsecs` INT,
        `bid1Price` DOUBLE,
        `bid1Ccy` STRING,
        `bid1Size` INT,
        `bid1DataSource` INT,
        `bid1AgeOffsetMsecs` INT,
        `bid2Price` DOUBLE,
        `bid2Ccy` STRING,
        `bid2Size` INT,
        `bid2DataSource` INT,
        `bid2AgeOffsetMsecs` INT,
        `bid3Price` DOUBLE,
        `bid3Ccy` STRING,
        `bid3Size` INT,
        `bid3DataSource` INT,
        `bid3AgeOffsetMsecs` INT,
        `bid4Price` DOUBLE,
        `bid4Ccy` STRING,
        `bid4Size` INT,
        `bid4DataSource` INT,
        `bid4AgeOffsetMsecs` INT,
        `ask0Price` DOUBLE,
        `ask0Ccy` STRING,
        `ask0Size` INT,
        `ask0DataSource` INT,
        `ask0AgeOffsetMsecs` INT,
        `ask1Price` DOUBLE,
        `ask1Ccy` STRING,
        `ask1Size` INT,
        `ask1DataSource` INT,
        `ask1AgeOffsetMsecs` INT,
        `ask2Price` DOUBLE,
        `ask2Ccy` STRING,
        `ask2Size` INT,
        `ask2DataSource` INT,
        `ask2AgeOffsetMsecs` INT,
        `ask3Price` DOUBLE,
        `ask3Ccy` STRING,
        `ask3Size` INT,
        `ask3DataSource` INT,
        `ask3AgeOffsetMsecs` INT,
        `ask4Price` DOUBLE,
        `ask4Ccy` STRING,
        `ask4Size` INT,
        `ask4DataSource` INT,
        `ask4AgeOffsetMsecs` INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'quote-data-raw',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-1:9092,kafka-2:9092,kafka-3:9092',
        'format' = 'avro'
    );
""")

t_env.execute_sql("""
    CREATE TABLE postgres_table (
        key INT,
        symbol STRING,
        name STRING
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/postgres',
        'table-name' = 'quote_data_symbols',
        'username' = 'postgres',
        'password' = 'postgres'
    );
""")

# Conversion between Table and DataStream
#ds = t_env.to_append_stream(t_env.from_path('raw_data_table'), row_type_info)

#ds_transformed = ds#.map(
#    lambda value: Row(
#        value[0],
#        value[1],
#        value[2],
#        "JOB 5 " + value[3].upper() if value[3] is not None else "JOB 5",
#        value[4]
#    ),
#    output_type=row_type_info
#)
#json_serialization_schema = JsonRowSerializationSchema.builder().with_type_info(row_type_info).build()

#sink = KafkaSink.builder() \
#    .set_bootstrap_servers("kafka-1:9092,kafka-2:9092,kafka-3:9092") \
#    .set_record_serializer(
#        KafkaRecordSerializationSchema.builder()
#            .set_topic("quote-data-enriched")
#            .set_value_serialization_schema(json_serialization_schema)
#            .build()
#    ) \
#    .build()

# Add KafkaSink as a sink to the environment
#ds_transformed.sink_to(sink)

# Execute the job
#env.execute()

t_env.execute_sql("""
    CREATE TABLE enriched_table (
        `recordId` INT,
        `time` BIGINT,
        `arrivalTime` BIGINT,
        `bid0Price` DOUBLE,
        `bid0Ccy` STRING,
        `bid0Size` INT,
        `bid0DataSource` INT,
        `bid0AgeOffsetMsecs` INT,
        `bid1Price` DOUBLE,
        `bid1Ccy` STRING,
        `bid1Size` INT,
        `bid1DataSource` INT,
        `bid1AgeOffsetMsecs` INT,
        `bid2Price` DOUBLE,
        `bid2Ccy` STRING,
        `bid2Size` INT,
        `bid2DataSource` INT,
        `bid2AgeOffsetMsecs` INT,
        `bid3Price` DOUBLE,
        `bid3Ccy` STRING,
        `bid3Size` INT,
        `bid3DataSource` INT,
        `bid3AgeOffsetMsecs` INT,
        `bid4Price` DOUBLE,
        `bid4Ccy` STRING,
        `bid4Size` INT,
        `bid4DataSource` INT,
        `bid4AgeOffsetMsecs` INT,
        `ask0Price` DOUBLE,
        `ask0Ccy` STRING,
        `ask0Size` INT,
        `ask0DataSource` INT,
        `ask0AgeOffsetMsecs` INT,
        `ask1Price` DOUBLE,
        `ask1Ccy` STRING,
        `ask1Size` INT,
        `ask1DataSource` INT,
        `ask1AgeOffsetMsecs` INT,
        `ask2Price` DOUBLE,
        `ask2Ccy` STRING,
        `ask2Size` INT,
        `ask2DataSource` INT,
        `ask2AgeOffsetMsecs` INT,
        `ask3Price` DOUBLE,
        `ask3Ccy` STRING,
        `ask3Size` INT,
        `ask3DataSource` INT,
        `ask3AgeOffsetMsecs` INT,
        `ask4Price` DOUBLE,
        `ask4Ccy` STRING,
        `ask4Size` INT,
        `ask4DataSource` INT,
        `ask4AgeOffsetMsecs` INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'quote-data-enriched',
        'scan.startup.mode' = 'earliest-offset',
        'properties.bootstrap.servers' = 'kafka-1:9092,kafka-2:9092,kafka-3:9092',
        'format' = 'avro'
    );
""")

# Define INSERT INTO query
insert_query = """
    INSERT INTO enriched_table
    SELECT * FROM raw_data_table
"""

# Execute the INSERT INTO query
t_env.execute_sql(insert_query).wait()
