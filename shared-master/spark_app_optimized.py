import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col,array_contains
import datetime
def get_executor_memory(sc):
    executor_memory_status = sc._jsc.sc().getExecutorMemoryStatus()
    executor_memory_status_dict = sc._jvm.scala.collection.JavaConverters.mapAsJavaMapConverter(executor_memory_status).asJava()
    total_used_memory = 0
    for executor, values in executor_memory_status_dict.items():
        total_memory = values._1() / (1024 * 1024)  # Convert bytes to MB
        free_memory = values._2() / (1024 * 1024)    # Convert bytes to MB
        used_memory = total_memory - free_memory
        total_used_memory += used_memory
    return total_used_memory


conf = (pyspark.SparkConf().setMaster("yarn"))
sc = pyspark.SparkContext(conf = conf)
sc._jsc.hadoopConfiguration().set("dfs.block.size", "512m")

spark = SparkSession.builder.appName('Bench_app').getOrCreate()

# start =  datetime.datetime.now()

# print("1. ", datetime.datetime.now())
# df = spark.read.format('csv') \
#                 .option('header',True) \
#                 .option('multiLine', True) \
#                 .load("hdfs:///input/dataset.csv")


# # enable partitioning
# # df = df.repartition(df["Model"])
# print("2. ", datetime.datetime.now())

# print(df.count())
# df.printSchema()

# for ind in range(0,10):
#     df_models = df.groupBy([df["Model"], df["Make"]]).count()
#     # df_models.show()

#     df_count = df.join(df_models,"Model")
#     df_count.printSchema()
#     df_count.select(df_count["Model"],df_count["count"]).show()
#     df_count = df_count.orderBy(df_count["count"])
#     if ind == 0:
#         df_count.cache()
#     #enable cache
#     df_2 = df_count.filter(df_count["count"] < 100).filter(df["Postal Code"].cast('int').alias('count2') % 2 == 0).groupBy(df_count["Model"], df_count["Vehicle Location"]).count()
                    
#     df_count.join(df_2, "count" ,'inner').show()
#     print(f"Iter {ind} date {datetime.datetime.now()}")

# print ("total_time : ", datetime.datetime.now() - start)


import datetime
import pandas as pd

# Prepare a DataFrame to collect results
results = pd.DataFrame(columns=["Run", "Read Time", "Count Time", "Join and Order Time", "Total Time", "Total RAM"])

for run in range(30):
    start = datetime.datetime.now()

    # Read CSV
    read_start = datetime.datetime.now()
    df = spark.read.format('csv') \
                .option('header',True) \
                .option('multiLine', True) \
                .load("hdfs:///input/dataset.csv")
    read_time = datetime.datetime.now() - read_start

    # Count operation
    count_start = datetime.datetime.now()
    print(df.count())
    df.printSchema()
    count_time = datetime.datetime.now() - count_start

    # Join, Order, and Cache
    join_order_start = datetime.datetime.now()
    # for ind in range(2):
    #     df_models = df.groupBy([df["Model"], df["Make"]]).count()
    #     df_count = df.join(df_models,"Model")
    #     df_count = df_count.orderBy(df_count["count"])
    #     df_2 = df_count.filter(df_count["count"] < 100).filter(df["Postal Code"].cast('int') % 2 == 0).groupBy(df_count["Model"], df_count["Vehicle Location"]).count()
    #     df_count.join(df_2, "count" ,'inner')
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
    
    join_order_time = datetime.datetime.now() - join_order_start

    # Calculate total time
    total_time = datetime.datetime.now() - start
    total_RAM = get_executor_memory(sc)
    # Store the results
    new_row = pd.DataFrame({
        "Run": [run + 1],
        "Read Time": [read_time.total_seconds()],
        "Count Time": [count_time.total_seconds()],
        "Join and Order Time": [join_order_time.total_seconds()],
        "Total Time": [total_time.total_seconds()],
        "Total RAM": [total_RAM],
    })

    # Append the new row to the results DataFrame
    results = pd.concat([results, new_row], ignore_index=True)

# Print the results
print(results)

# Optional: Save results to a file or plot them
results.to_csv("timing_results_optimized.csv", index=False)
