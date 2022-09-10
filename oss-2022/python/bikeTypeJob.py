import os
from pyspark.sql import SparkSession


FILE_LOCATION = os.environ.get("FILE_LOCATION")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

spark = SparkSession.builder.appName("bike-type-job").getOrCreate()
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_KEY)

rdd = spark.read.csv(FILE_LOCATION, header=True).rdd

result = rdd \
    .map(lambda fields: (fields["rideable_type"], 1)) \
    .reduceByKey(lambda x, y: x + y) \
    .sortBy(lambda x: x[1], ascending=False) \
    .collect()

for element in result:
    print("BikeType %s, count %d" %(element[0], element[1]))


spark.stop()
