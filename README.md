# F1-races-ETL-project
ETL to extract latest 2023 F1 championship' result and load into a database, which update driver and team's ranking

# GENERAL INTRODUCTION


# DEV ENVIRONMENT SETUP
The ETL scirpts are written and run on local WSL (Windows System for Linux) with Ubuntu. The 
+ The installation and configuration of PySpark and Airflow on local WSL

AWS services setup : I use a free-tier account for base services like S3 and RDS.    
+ Launch S3 service
+ Create AWS user with full access to S3 service, the secrete key and 
+ RDS services launched
I have tried ro run the spark code on GLUE to build a database on Redshift, but the GLUE service has been very expensive.  Thus I was obliged to run the Spark on local cluster, and build the database on RDS.
