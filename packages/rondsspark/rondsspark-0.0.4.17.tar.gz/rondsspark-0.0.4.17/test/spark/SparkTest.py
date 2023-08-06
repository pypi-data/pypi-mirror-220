from datetime import datetime, date

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import Row
import logging

from pyspark.sql.functions import explode, split
from pyspark.streaming import StreamingContext
from pyspark.sql import functions as F

from ronds_sdk import logger_config

logger = logging.getLogger(__name__)


def spark_df1(spark: SparkSession):
    # spark run
    df = spark.createDataFrame([
        Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
        Row(a=2, b=2., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
        Row(a=3, b=2., c='string2', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0)),
    ])
    print(df.schema)


def spark_df2(spark: SparkSession):
    # spark df 指定元数据
    df = spark.createDataFrame([
        (1, 2., "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
        (2, 2., "string1", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
        (3, 2., "string1", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0)),
    ], schema="a long, b double, c string, d date, e timestamp")
    logger.info(df.schema)


def structured_streaming1(spark: SparkSession):
    """
    :param spark: spark 入口
    :return:  None
    """
    lines = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()
    words = lines.select(explode(split(lines.value, " ")).alias("word"))
    word_counts = words.groupBy(words.word).agg(F.count(words.word))
    query = word_counts \
        .writeStream \
        .outputMode("update") \
        .format("console") \
        .start()
    query.awaitTermination()


def structured_streaming2(spark: SparkSession):
    lines = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()
    lines.createOrReplaceTempView("my_table")
    words_2 = spark.sql('select explode(split(value, " ")) as word2 from my_table')

    query2 = words_2 \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    query2.awaitTermination()


def spark_streaming1():
    sc = SparkContext("local[2]", "NetworkWordCount")
    ssc = StreamingContext(sc, 1)
    lines = ssc.socketTextStream("127.0.0.1", 9999)
    words = lines.flatMap(lambda line: line.split(" "))
    words.count()
    words.pprint(10)
    ssc.start()  # Start the computation
    ssc.awaitTermination()


def main():
    logger_config.config()
    spark = SparkSession.builder.getOrCreate()
    # spark_df1(spark)
    # spark_df2(spark)
    structured_streaming2(spark)


if __name__ == '__main__':
    main()
