from pyspark.sql import SQLContext, SparkSession

sparkS = SparkSession.builder.appName("LearningSparkApp").getOrCreate()
sparkC = sparkS.sparkContext

def main():
	df_cassandra = sparkS.read.json('./data/cassandra_zip').limit(10)
	df_kinesis = sparkS.read.parquet('./data/kinesis').limit(10)
	print(df_cassandra.count())
	print(df_kinesis.count())

if __name__ == "__main__":
	main()