import random
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from kafka_plugin.pinot_schema_operator import PinotSchemaSubmitOperator


start_date = datetime(2024, 10, 7)
default_args = {
    'owner': 'Saleh',
    'depends_on_past': False,
    'catchup': False,
    'start_date':start_date
}




with DAG('schema_dag',
         default_args=default_args,
         description='A DAG to submit all schema in a folder to Apache Pinot',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['schema']) as dag:

    start = EmptyOperator(
        task_id='start_task'
    )

    submit_schema = PinotSchemaSubmitOperator(
        task_id = 'submit_schema',
        folder_path = '/opt/airflow/dags/schemas',
        pinot_url = 'http://pinot-controller:9000/schemas'
    )

    end = EmptyOperator(
        task_id='end_task'
    )


    start >> submit_schema >> end
