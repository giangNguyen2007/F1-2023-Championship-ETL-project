

import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.sql.window import Window
from pyspark.sql.functions import desc
from pyspark.sql.functions import row_number, dense_rank, rank
from pyspark.sql.functions import lit
import os
import argparse

def main(params):

       gp_index = params.gp_index
       grand_prix = params.grand_prix

       # get postgres access credentials for later connection
       postGres_user = os.environ.get('RDS_POSTGRES_USER')
       postGres_password = os.environ.get('RDS_POSTGRES_PASSWORD')

       conf = SparkConf()
       conf.set('spark.hadoop.fs.s3.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
       conf.set('spark.jars', 'postgresql-42.6.0.jar')

       spark = SparkSession.builder \
              .config(conf = conf) \
              .appName('test') \
              .getOrCreate()
       
       result_schema = StructType([ \
              StructField("pos",IntegerType(),True), \
              StructField("driver_id",IntegerType(),False), \
              StructField("driver_name",StringType(),False), \
              StructField("constructor", StringType(), False), \
              StructField("laps", IntegerType(), True), \
              StructField("completion_time", IntegerType(), True), \
              StructField("points", IntegerType(), True) \
              ])


       # Extract the result of new race from s3 bucket
       df = spark.read.option('header', 'true').schema(result_schema).csv(f"s3a://gng-bucket-01/result-2023/result_{gp_index}_{grand_prix}.csv")
       
       # add columns for race name and index  
       df = df.withColumn("grand_prix", lit(grand_prix)).withColumn("gp_id", lit(gp_index))
       # rearrange the columns to match the column order of existing table in database
       df = df.selectExpr("gp_id", "grand_prix", "driver_id", "driver_name", "constructor","pos", "points", "laps")
       df.printSchema()
       df.show()


       # insert latest result to existing fact table (by appending) 
       if df.count()==20:
              df.write.mode("append") \
                     .format("jdbc") \
                     .options(
                            url='jdbc:postgresql://dbgng.cjoc6hd0q4wg.eu-west-3.rds.amazonaws.com:5432/postgres', # jdbc:postgresql://<host>:<port>/<database>
                            dbtable="factTB_result_2023",
                            user= postGres_user,
                            password= postGres_password,
                            driver='org.postgresql.Driver')\
                     .save()
              print(f"Grand prix No{gp_index} {grand_prix}'s result inserted sucessfully into fact table")
       else:
              print(f"Grand prix No{gp_index} {grand_prix}'s insertion failed") 


       # ===============================UPDATE THE DRIVER DIMENSION TABLE ================================================

       # Load the current table from database
       df_driver = spark.read \
                     .format("jdbc") \
                     .options(
                            url='jdbc:postgresql://dbgng.cjoc6hd0q4wg.eu-west-3.rds.amazonaws.com:5432/postgres', # jdbc:postgresql://<host>:<port>/<database>
                            dbtable=f"dim_drivers",
                            user= postGres_user,
                            password=postGres_password,
                            driver='org.postgresql.Driver')\
                     .load()
       print("="*60)
       print(f"Driver ranking before Grand prix No{gp_index} {grand_prix}'s result:")
       df_driver.show()


       # update driver table with latest result
       df_driver = df_driver.alias("df_driver").join(df.alias("df") ,df_driver.driver_id == df.driver_id,"inner").select("df_driver.*", "df.points")

       # update the "total_points" and "total_races" columns
       df_driver = df_driver.withColumn('total_points', df_driver['total_points']+df_driver['points']).drop("points")
       df_driver = df_driver.withColumn('total_races', df_driver['total_races']+ 1)
       # update the ranking column following total points update
       df_driver = df_driver.withColumn("current_rank", rank().over(Window.orderBy(desc("total_points"))))
       print(f"Driver ranking before Grand prix No{gp_index} {grand_prix}'s result:")
       df_driver.show()

       # Load the updated table back to database in overwrite mode
       if df_driver.count()==20:
              try:
                     df_driver.write \
                            .mode("overwrite") \
                            .format("jdbc") \
                            .options(
                                   url='jdbc:postgresql://dbgng.cjoc6hd0q4wg.eu-west-3.rds.amazonaws.com:5432/postgres', # jdbc:postgresql://<host>:<port>/<database>
                                   dbtable=f"dim_drivers",
                                   user= postGres_user,
                                   password=postGres_password,
                                   driver='org.postgresql.Driver')\
                            .save()
              except Exception as e:
                     print("error loading to RDS: ", e)
              else:                   
                     print("="*60)
                     print(f"Successfully create driver table after Grand Prix No{gp_index} {grand_prix}:")
       else:
              print("error in transformation of driver dataframe")

       
       # ===============================UPDATE THE TEAM DIMENSION TABLE ===================================
       
       # Recalculate the total points per team
       df_team_updated = df_driver.groupby(['team_id', 'team_name']).sum("total_points")
       # Add the ranking column
       df_team_updated = df_team_updated.withColumn("current_rank", rank().over(Window.orderBy(desc("sum(total_points)"))))
       # the df_team_updated dataframe now has the same 4 column as the team dimension table in the database:
       # "team_id", "team_name", "sum(total_points)" and "current_ranking" 

       # Overwrite the current team dim table with the df_team_updated 
       
       if df_team_updated.count()==10:
              try:
                     df_team_updated.write.mode("overwrite") \
                            .format("jdbc") \
                            .options(
                                   url='jdbc:postgresql://dbgng.cjoc6hd0q4wg.eu-west-3.rds.amazonaws.com:5432/postgres', # jdbc:postgresql://<host>:<port>/<database>
                                   dbtable="dim_team",
                                   user= postGres_user,
                                   password=postGres_password,
                                   driver='org.postgresql.Driver')\
                            .save()
              except Exception as e:
                     print("error loading to RDS: ", e)
              else:                   
                     print("="*60)
                     print(f"Successfully update team dimension table after Grand Prix No{gp_index} {grand_prix}:")
       else:
              print("error in transformation of team dataframe, database not updated")
       
       




if __name__ == '__main__':
       parser = argparse.ArgumentParser()
       parser.add_argument('--grand_prix')
       parser.add_argument('--gp_index', type=int)
       args = parser.parse_args()
       main(args)








