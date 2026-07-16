from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

DBT_DIR = "/opt/airflow/retail_transforms"
DBT_PROFILES_DIR = "/home/airflow/.dbt"
DBT_TARGET = "prod"

with DAG(
    dag_id='retail_pipeline',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['retail']
) as dag:

    # Task 1: ingestion --> skip for now
    # Task 2: staging models
    task_2 = BashOperator(
        task_id='stg_models',
        bash_command=f'dbt run --select staging --project-dir {DBT_DIR} --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}'
    )
    task_3 = BashOperator(
        task_id='int_models',
        bash_command=f'dbt run --select int_orders_enriched --project-dir {DBT_DIR} --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}'
    )
    task_4 = BashOperator(
        task_id='mart_models',
        bash_command=f'dbt run --select mart_customer_orders mart_seller_performance mart_order_fulfillment --project-dir {DBT_DIR} --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}'
    )
    task_5 = BashOperator(
        task_id='dbt_tests',
        bash_command=f'dbt test --project-dir {DBT_DIR} --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}'
    )
    # dependencies
    task_2 >> task_3 >> task_4 >> task_5