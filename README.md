# F1-races-ETL-project

# 1. GENERAL INTRODUCTION
The 2023 F1 championship consists of 23 races (grand-prix) organised in multiple cities over 9 months, from March to November, with rythm of one race every 2-3 weeks. There are 10 teams with 2 drivers each. For each race, points are attributed according to driver's position (max 20 points for race winner). /

Our database compiles data on race results, driver and team. 

After each race event, the ETL scripts will extract the race result from rapidAPI endpoint, transform and load into a database on AWS RDS, which update driver and team's ranking.   

![image](https://github.com/giangNguyen2007/F1-races-ETL-project/assets/146067036/5dd268aa-91fa-4184-a151-cd80c852a16b)


## 1.1 Database model
The database consists of 4 tables, linked in star schema:
+ dim_race (list of all races of season) race_id, race_title, place, event_date, race_winner
+ dim_driver: driver_id, driver_name, team_id, total_points, current_ranking
+ dim_team : team_id, team_name, total_points, current_ranking
+ fact table (compile results of all drivers for past races): race_id, driver_id, driver_name, team_id, postions, points, race_time

Currently, the database have recorded the results of the first 10 races of the season.

## 1.2 ETL DAG Overview
The ETL is orchestrated by Airflow in a single DAG, which consists of two tasks:
- task 1 (PythonOperator) : a Python function to make request to RapiAPI endpoint to retrieve the lastet F1 race result,  in form of csv table, then save it into S3 folder
    + connection Python-AWS S3 : boto3
- task 2 (BashOperator): bash script to submit PySpark .py file to local Spark cluster. The PySpark script will retrieve the latest csv table from S3, make transformation and update the RDS database accordingly
    + connector Pyspark-AWS S3: AWS SDK library
    + connection Pyspark-AWS RDS : Postgres JDBC

## 1.3 Files in project folder
The folder contains 3 code files, to be copied into the /dags folder of Airlfow
- F1_ETL_dag.py : dag and task definition
- pySpark_transform_load_rds.py : PySpark code for the task #2 of the ETL process. 
- spark-submit.sh : bash script to submit the pySpark_transform_load_rds.py to local Spark cluster

## 1.4 Project Launch Steps Overview 
Environment setup (ref section "2. DEV ENVIRONMENT SETUP" for more details)
- Setup AWS S3 and RDS services  
- Install and pre-configure Airflow and PySpark on local WSL 

Steps to launch project (ref section "3. ETL Launch" for more details):
- Start local PySpark cluster
- Start Airflow server and copy 3 files into the Airflow's /dags folder
- Run Airflow DAG



# 2. DEV ENVIRONMENT SETUP
## 2.1. AWS services setup : 
I use a free-tier account for base services like S3 and RDS.  Initially, I worked on GLUE spark notebook and a Redshift database, but the GLUE service has been too expensive.  Thus I was obliged to run the Spark on local cluster, and build the database on RDS.
  
+ Create bucket in S3 to store the raw data extracted from rapidAPI : s3/gng-bucket-01/ 
+ Create AWS user with full access to S3, create user access keys  (AWS_ACCESS_KEY_ID and AWS_SECRET_KEY) to be saved on local machine
+ Launch RDS service with Postgres, save connection credentials (host url, port, database, user and passwrod)

## 2.2 Local environement setup
The ETL scripts are written and run on local WSL-Ubuntu (Windows System for Linux), which requires the installation below:
+ install Airflow using pip.
+ install and configure PySpark for connection to AWS => see details in install-PySpark.md
+ install pgAdmin then make connection to RDS Postgres. This allow us to monitor the evolution of the database after each Airflow DAG run
  
# 3. STEPS TO LAUNCH THE ETL
## 3.1 Start local Spark cluster

Launch local Spark master 
```bash
{$SPARK_HOME}/sbin/start-master.sh
```
By going on `localhost:8081`, we can get the URL of the master in the form  ```spark://<computer-name>.:7077``` 

Launch one worker associated with the master

```bash
MASTER_URL="spark://<computer-name>.:7077"
{$SPARK_HOME}/sbin/start-worker.sh ${MASTER_URL}
```
We now have a local Spark cluster running with one worker, which is enough for our project, whose goal is to gain practise on building ETL pipeline with Spark.

![image](https://github.com/giangNguyen2007/F1-races-ETL-project/assets/146067036/489fe49c-a9e9-4a85-87bd-1c2ea23921c4)

## 3.2 Launch Airflow and run the ETL DAG

Start the Airflow server
```bash
airflow standalone
```
The Airflow UI server can be accessed on localhost:8080, where all DAG status can be checked.
Copy the 3 code files into the /dags folder. The DAG status and task graph can be checked on the Airflow UI.

![image](https://github.com/giangNguyen2007/F1-races-ETL-project/assets/146067036/4ba7fa71-2655-436d-915b-b5697cd425e3)

The DAG now is ready to be run as scheduled.

