# spark docker cluster
To build:

```
sudo make build_base_image
sudo make build_master_image
sudo make build_slave_image
sudo docker-compose up -d --scale slave=<slaves_number>
```
To stop:
```
sudo docker-compose down
```

Dataset: 
Electric Vehicle Population Data
```
https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2/about_data
https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD
```

Configs:
block_size = 512m
driver_mem = 4G

To run: 
```
sudo docker exec -it hadoop-spark-cluster_master_1 /bin/bash
```

In container 
```
cd ~/shared/

# Optimized with partitioning and caching
pyspark  --driver-memory 4G < spark_app_optimized.py

# Not optimized
pyspark  --driver-memory 4G < spark_app.py 
```

Results:
Execution time
| |non_optimized|optimized|
|---|---|-----------|
|1_slave|0:00:33.125732 |0:00:26.564846|
|3_slave|0:00:30.492206 |0:00:24.235050|

Ram consumption
| |non_optimized|optimized|
|---|---|-----------|
|1_slave| 3533MB| 3207MB|
|3_slave| 5865MB |5463MB|



