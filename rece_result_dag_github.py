from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import requests
import boto3
import pandas as pd
import os

from datetime import datetime, timedelta

# Define python function to perform rapid API data extraction and loading to s3
def extractFunc(grand_prix, gp_index):

    aws_access_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_KEY')
    rapid_api_key = os.environ.get('RAPID_API_KEY')

    # make request to Rapid API endpoint with parameter corresponding to the name of latest race (grand-prix)
    url = f"https://fia-formula-1-championship-statistics.p.rapidapi.com/api/races/race-results/2023/{grand_prix}"

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "fia-formula-1-championship-statistics.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    result_json = response.json()

    # convert data into pandas dataframe and save to csv
    df = pd.DataFrame.from_dict(result_json["raceResultsFiltered"])
    print(df.head(5))
    df.to_csv(f"./result_{gp_index}_{grand_prix}.csv", index = False)

    # save the csv file to S3 using boto3 library
    s3 = boto3.resource(
        service_name='s3',
        region_name='eu-west-3',
        aws_access_key_id= aws_access_id,
        aws_secret_access_key= aws_secret_key)

    s3.Bucket('gng-bucket-01').upload_file(Filename = f"./result_{gp_index}_{grand_prix}.csv", Key = f"result-2023/result_{gp_index}_{grand_prix}.csv" )


with DAG(
    dag_id="F1_ETL_dag",
    description="2013 F1 championship result ETL",
    start_date=datetime(2023, 9, 19),
    schedule_interval="@weekly"
) as dag:

    task1= PythonOperator(
        task_id="rapidAPI_extraction_to_s3",
        python_callable=extractFunc,
        op_kwargs={'grand_prix':'japan', 'gp_index':17}
    )

    task2= BashOperator(
        task_id="spark_transform_load_rds",
        bash_command='./spark-submit-script.sh japan 17 ',
    )

    task1>>task2


