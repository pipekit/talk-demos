import os
from datetime import datetime
from pyspark.sql import SparkSession


FILE_LOCATION = os.environ.get("FILE_LOCATION")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

def loadData(fields):
    bikeType = fields["rideable_type"]
    startAt = datetime.strptime(fields["started_at"], "%Y-%m-%d %H:%M:%S")
    endAt = datetime.strptime(fields["ended_at"], "%Y-%m-%d %H:%M:%S")
    rideLength = endAt - startAt

    return (bikeType, rideLength)

spark = SparkSession.builder.appName("bike-ride-length-job").getOrCreate()
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_KEY)

rdd = spark.read.csv(FILE_LOCATION, header=True).rdd


rdd = rdd\
    .map(lambda line: loadData(line)) \
    .reduceByKey(lambda x, y: x + y) \
    .sortBy(lambda x: x[1], ascending=False)

for element in rdd.collect():
    print("BikeType %s, count %s" %(element[0], element[1]))


spark.stop()
