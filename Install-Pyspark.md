# Introduction
This text explain all steps to install and setup pyspark on local WSL, including AWS connection libraries.

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
export PATH="${JAVA_HOME}/bin:${PATH}"
export SPARK_HOME="${HOME}/spark/spark-3.2.4-bin-hadoop3.2"
export PATH="${SPARK_HOME}/bin:${PATH}"
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

To test if Pyspark is properly installed, we can run the following command to launch the spark shell:
```bash
spark-shell
```
This commands should launch a spark CLI session in scalalocal and spark context UI  accessible at localhost:4040
For development, I use Jupyter notebook, which is pre-installed on WSL, which can be launched by ```jupyter notebook```


## Install Connector libraries
For connection to AWS S3 and RDS, addtional libraries need to be downloaded and copied in Spark's jars folder:
 - JDBC Posgres library (=> connection to Posgres on AWS RDS)
 - Hadoop AWS and AWS JDK (=> for connection to S3 ) (link for jar file to be found on Maven Repository)

```bash
cd /root/spark/spark-3.2.4-bin-hadoop3.2/jars
wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
wget https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws
wget  https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.1023/aws-java-sdk-1.11.1023.jar
```
To access S3, Pyspark also needs AWS credentials associted with a AWS user. This credentials can be created in the AWS user account. Here we record the credentials as environment varialbe, which will be used by AWS SDK libraries during script run.
```bash
export AWS_ACCESS_KEY_ID= <access key provided by AWS>
export AWS_SECRET_ACCESS_KEY= <secret key provided by AWS>
```
With all this set up, the pyspark script can be launched on local WSL, with access to both S3 and  RDS services.
