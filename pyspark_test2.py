from pyspark.sql import SparkSession
import pyspark.sql.functions as f

def main():
    spark = SparkSession.builder        \
        .appName('Visitas Diarias')     \
        .getOrCreate()

    df = spark.read.json('./data/cassandra_zip').limit(10)

    json_count = df.count()

    df = df                                                                         \
        .withColumn('associated', f.lit(False))                                     \
        .withColumnRenamed('changedOn', 'timestamp')                                \
        .withColumnRenamed('mapHierarchy', 'locationMapHierarchy')                  \
        .withColumnRenamed('macAddress', 'deviceId')                                \
        .select('deviceId', 'associated', 'timestamp', 'locationMapHierarchy')

    df2 = spark.read.parquet('./data/kinesis').limit(10)

    kinesis_count = df2.count()

    df2 = df2.select(f.explode('notifications').alias('x')).select('x.*') \
        .select('deviceId', 'associated', 'timestamp', 'locationMapHierarchy')

    df_final = df2.union(df)

    final_count = df_final.count()

    print(json_count)
    print(kinesis_count)
    print(final_count)


if __name__ == '__main__':
    main()