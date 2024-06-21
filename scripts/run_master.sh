#!/bin/bash 
echo "Initializing SSH"
sudo service ssh start
eval `ssh-agent -s`
exec ssh-add &

# Below 3 lines will hide the prompt about fingerprinting during ssh connection 
# to HDFS
ssh -oStrictHostKeyChecking=no spark-master uptime
ssh -oStrictHostKeyChecking=no localhost uptime
ssh -oStrictHostKeyChecking=no 0.0.0.0 uptime

 
echo "Starting HDFS"
~/hadoop-$HADOOP_VERSION/sbin/start-dfs.sh > ./start-dfs.log   

# Now, start YARN resource manager and redirect output to the logs
echo "Starting YARN resource manager"
yarn resourcemanager > ~/resourcemanager.log 2>&1 &

# Next, start Spark master
echo "Starting Spark master..."
exec start-master.sh -h spark-master -p 7077 &

echo "Starting history server..."
hdfs dfs -mkdir /shared
hdfs dfs -mkdir /shared/spark-logs 

hdfs dfs -mkdir /input
hdfs dfs -put /home/sparker/shared/dataset.csv /input/dataset.csv

exec start-history-server.sh &
# Start bash to prevent Docker image from exit
# exec bash
while true; do sleep 1000; done
