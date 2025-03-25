import random
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from kafka_plugin.pinot_table_operator import PinotTableSubmitOperator


start_date = datetime(2024, 10, 7)
default_args = {
    'owner': 'Saleh',
    'depends_on_past': False,
    'start_date':start_date,
    'catchup':False,
}




with DAG('table_dag',
         default_args=default_args,
         description='A DAG to submit all table in a folder to Apache Pinot',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['table']) as dag:

    start = EmptyOperator(
        task_id='start_task'
    )

    submit_tables = PinotTableSubmitOperator(
        task_id = 'submit_table',
        folder_path = '/opt/airflow/dags/tables',
        pinot_url = 'http://pinot-controller:9000/tables'
    )

    end = EmptyOperator(
        task_id='end_task'
    )


    start >> submit_tables >> end
