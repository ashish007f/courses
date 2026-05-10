from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit, expr
from config import settings
import os

def create_spark_session(app_name="UnifiedBronzeIngestion"):
    """
    Create a SparkSession using Spark Connect.
    Standard PySpark 4 SparkSession is now Connect-aware.
    """
    # Use environment variable for remote URL if available, fallback to localhost
    spark_remote = os.getenv("SPARK_REMOTE", "sc://localhost")

    return SparkSession.builder \
        .remote(spark_remote) \
        .appName(app_name) \
        .getOrCreate()


def process_kafka_streams(spark):
    # Subscribe to all relevant topics
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.kafka_bootstrap_servers) \
        .option("subscribe", ",".join(settings.kafka_topics)) \
        .option("startingOffsets", "earliest") \
        .load()

    # Add metadata
    processed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "topic", "partition", "offset", "timestamp") \
        .withColumn("ingestion_timestamp", current_timestamp()) \
        .withColumn("source", lit("kafka"))
    

    return processed_df

def process_batch_files(spark):
    # Ensure directory exists
    os.makedirs(settings.batch_landing_zone, exist_ok=True)
    
    # Read files as a stream (simulating bounded batch normalized into stream)
    try:
        df = spark.readStream \
            .format("json") \
            .option("cleanSource", "archive") \
            .option("sourceArchiveDir", f"{settings.batch_landing_zone}/archive") \
            .load(settings.batch_landing_zone)
        
        processed_df = df.selectExpr("CAST(NULL AS STRING) as key", "to_json(struct(*)) as value") \
            .withColumn("topic", lit("batch_import")) \
            .withColumn("partition", lit(0)) \
            .withColumn("offset", lit(0)) \
            .withColumn("timestamp", current_timestamp()) \
            .withColumn("ingestion_timestamp", current_timestamp()) \
            .withColumn("source", lit("batch"))
        

        return processed_df
    except Exception as e:
        print(f"Batch landing zone error or empty: {e}")
        return None

def write_to_bronze(df, query_name):
    if df is None:
        return
        
    return df.writeStream \
        .format("parquet") \
        .outputMode("append") \
        .queryName(query_name) \
        .option("checkpointLocation", f"{settings.checkpoint_base_path}/{query_name}") \
        .start(f"{settings.bronze_base_path}/raw_events")

if __name__ == "__main__":
    spark = create_spark_session()
    
    kafka_df = process_kafka_streams(spark)
    kafka_query = write_to_bronze(kafka_df, "kafka_to_bronze")
    
    # Batch processing (uncomment if batch files are expected)
    # batch_df = process_batch_files(spark)
    # if batch_df:
    #     batch_query = write_to_bronze(batch_df, "batch_to_bronze")
    
    spark.streams.awaitAnyTermination()
