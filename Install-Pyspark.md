#Pyspark Installation

Create installation folder where both Java and Pyspark will be installed 
```bash
mkdir spark
cd spark
```

Inside the spark/ folder, download and unzip both JDK and PYSPARK

```bash
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
tar xzvf openjdk-11.0.2_linux-x64_bin.tar.gz
```

set Environement Variable

```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export SPARK_HOME="${HOME}/spark/spark-3.2.4-bin-hadoop3.2"
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

# Connector Installation
