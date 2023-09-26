# Introduction
This text explain steps to install and setup pyspark on local machine

## Install JDK and Pyspark
Create installation folder where both Java and Pyspark will be installed 
```bash
mkdir spark
cd spark
```

Inside the spark/ folder, download and unzip both JDK (version 11) and PYSPARK. The download link can be found on the pyspark and open jdk websites. 

```bash
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
tar xzvf openjdk-11.0.2_linux-x64_bin.tar.gz
wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar xzvf spark-3.5.0-bin-hadoop3.tgz
```

set Environement Variable. These commands can be copied into the .bashrc file, which will exectue them automatically at each terminal launch.

```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export SPARK_HOME="${HOME}/spark/spark-3.2.4-bin-hadoop3.2"
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

## Install Connector libraries
For connection to AWS S3 and RDS, addtional connector libraries need to be downloaded and copied in Spark's jars folder:
 - JDBC Posgres library (=> conenction to Posgres on AWS RDS)
 - Hadoop AWS => for connection to S3  (link for jar file to be found on Maven Repository)

```bash
cd /root/spark/spark-3.2.4-bin-hadoop3.2/jars
wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
wget https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws

```


## Lau
