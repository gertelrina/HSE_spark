# Get base image
FROM ubuntu:20.04

# Install Java
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    add-apt-repository ppa:openjdk-r/ppa -y && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get clean

# Install needed packages
RUN apt-get install less -y
RUN apt-get -y install vim
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install openssh-client
RUN apt-get -y install rsync
RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -ms /bin/bash sparker
USER sparker
WORKDIR /home/sparker

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre/
# Download Spark binary distribution with Hadoop
ENV HADOOP_VERSION 3.3.2
ENV HADOOP_HOME /home/sparker/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz  -q -O ./hadoop-$HADOOP_VERSION.tar.gz
RUN tar -xvzf ./hadoop-$HADOOP_VERSION.tar.gz
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# SPARK
ENV SPARK_VERSION 3.3.2
ENV SPARK_HOME /home/sparker/spark-$SPARK_VERSION-bin-hadoop3
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV PATH $PATH:${SPARK_HOME}/bin:${SPARK_HOME}/sbin
RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz -q -O ./spark-$SPARK_VERSION-bin-hadoop3.tgz
RUN tar -xvzf ./spark-$SPARK_VERSION-bin-hadoop3.tgz

# node manager ports
EXPOSE 8040
EXPOSE 8042
EXPOSE 22
EXPOSE 8030
EXPOSE 8031
EXPOSE 8032
EXPOSE 8033
EXPOSE 8088
EXPOSE 10020
EXPOSE 19888
