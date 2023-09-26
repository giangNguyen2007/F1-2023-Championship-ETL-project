# F1-races-ETL-project
ETL to extract latest 2023 F1 championship' result and load into a database, which update driver and team's ranking

# 1. GENERAL INTRODUCTION
The 2023 F1 championship consists of 23 races (grand-prix) organised in multiple cities over 9 months, from March to November, with rythme of one race every 2-3 weeks. There are 10 teams with 2 driver each. For each race, points are attributed according to driver's position (max 20 points for race winner)

## 1.1 Database model
The database consists of 4 tables, linked in star schema:
+ dim_race (list of all races of season) race_id, race_title, place, event_date, race_winner
+ dim_driver: driver_id, driver_name, team_id, total_points, current_ranking
+ dim_team : team_id, team_name, total_points, current_ranking
+ fact table (compile results of all drivers for past races): race_id, driver_id, driver_name, team_id, postions, points, race_time

Currently, the database have recorded the results of the first 10 races of the season. After each new race, the ETL scripts be launched to extract the result from RapidAPI, and update the database accordingly. 

## 1.2 ETL scripts
The ETL consist of two scripts:
- Python Script: make request to RapiAPI endpoint to retrieve the lastet F1 race result,  in form of csv table, then save it into S3 folder
    + connection Python-AWS S3 : boto3
- Pyspark script: retrieve the latest csv table from S3, make transformation and update the RDS database accordingly
    + connector Pyspark-AWS S3: AWS SDK library
    + connection Python- AWS RDS : Postgres JDBC



# DEV ENVIRONMENT SETUP
## AWS services setup : 
I use a free-tier account for base services like S3 and RDS.  Initially, I worked on GLUE spark notebook and a Redshift database, but the GLUE service has been too expensive.  Thus I was obliged to run the Spark on local cluster, and build the database on RDS.
  
+ Create bucket in S3 to store the raw data extracted from rapidAPI : s3/gng-bucket-01/ 
+ Create AWS user with full access to S3, create user access keys  (AWS_ACCESS_KEY_ID and AWS_SECRET_KEY) to be saved on local machine
+ Launch RDS service with Postgres, save connection credentials (host url, port, database, user and passwrod)

## Local environement setup
The ETL scirpts are written and run on local WSL-Ubuntu. (Windows System for Linux). The 
+ install and configure Airflow
+ install and configure PySpark for connection to AWS => see details in install-PySpark.md
+ install pgAdmin then make connection to RDS Postgres. This allow us to monitor the evolution of the database after each Airflow DAG run
  
## 
