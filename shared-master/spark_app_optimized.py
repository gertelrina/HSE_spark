import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col,array_contains
import datetime


conf = (pyspark.SparkConf().setMaster("yarn"))
sc = pyspark.SparkContext(conf = conf)
sc._jsc.hadoopConfiguration().set("dfs.block.size", "512m")

spark = SparkSession.builder.appName('Bench_app').getOrCreate()

start =  datetime.datetime.now()

print("1. ", datetime.datetime.now())
df = spark.read.format('csv') \
                .option('header',True) \
                .option('multiLine', True) \
                .load("hdfs:///input/dataset.csv")


# enable partitioning
# df = df.repartition(df["Model"])
print("2. ", datetime.datetime.now())

print(df.count())
df.printSchema()

for ind in range(0,10):
    df_models = df.groupBy([df["Model"], df["Make"]]).count()
    # df_models.show()

    df_count = df.join(df_models,"Model")
    df_count.printSchema()
    df_count.select(df_count["Model"],df_count["count"]).show()
    df_count = df_count.orderBy(df_count["count"])
    if ind == 0:
        df_count.cache()
    #enable cache
    df_2 = df_count.filter(df_count["count"] < 100).filter(df["Postal Code"].cast('int').alias('count2') % 2 == 0).groupBy(df_count["Model"], df_count["Vehicle Location"]).count()
                    
    df_count.join(df_2, "count" ,'inner').show()
    print(f"Iter {ind} date {datetime.datetime.now()}")

print ("total_time : ", datetime.datetime.now() - start)