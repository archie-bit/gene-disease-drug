from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession

def run_spark_job():
    # Connect to the remote Spark master
    spark = SparkSession.builder \
        .appName("AirflowSparkTest") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    print("Spark Session Created Successfully!")
    
    # Create a dummy dataframe
    df = spark.createDataFrame(
        [("Airflow", "Orchestrator"), ("Spark", "Engine")],
        ["Component", "Role"]
    )
    
    df.show()
    print(f"Row count: {df.count()}")
    
    spark.stop()

with DAG(
    dag_id="01_spark_test",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task_run_spark = PythonOperator(
        task_id="run_spark_task",
        python_callable=run_spark_job
    )