import random

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime, timedelta

start_date = datetime(2024, 9, 15)
default_args = {
    'owner': 'Saleh',
    'depends_on_past': False,
    'catchup': False,
}

num_rows = 50
output_file = './account_dim_large_data.csv'

account_ids = []
account_types = []
statueses = []
customer_ids = []
blanaces = []
opening_dates = []


def gen_random_data(row_num):
    account_id = f'A{row_num:05d}'
    account_type = random.choice(['SAVINGS', "CHECKING"])
    status = random.choice(['ACTIVE', 'UNACTIVE'])
    customer_ids = f'C{random.randint(1, 1000):05d}'
    balance = round(random.uniform(100.00, 10000.00), 2)

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 365))
    opening_dates_millis = int(random_date.timestamp() * 1000)

    return account_id, account_type, status, customer_ids, balance, opening_dates_millis


def gen_account_dim_data():
    row_num = 1
    while row_num <= num_rows:
        account_id, account_type, status, customer_id, balance, opening_dates_millis = gen_random_data(row_num)
        account_ids.append(account_id)
        account_types.append(account_type)
        statueses.append(status)
        customer_ids.append(customer_id)
        opening_dates.append(opening_dates_millis)
        blanaces.append(balance)

        row_num += 1

    df = pd.DataFrame({
        'account_id': account_ids,
        'account_type': account_ids,
        'status': statueses,
        'customer_id': customer_ids,
        'opening_dates': opening_dates_millis,
        'blanace': blanaces
    })
    df.to_csv(output_file, index=False)

    print(f'CSV file {output_file} with {num_rows} row has been generated successfully!')


with DAG('account_dim_gen',
         default_args=default_args,
         description='Generate large account dimension data in CSV file',
         schedule_interval=timedelta(seconds=10),
         start_date=start_date,
         tags=['schema']
         ) as dag:
    start = EmptyOperator(
        task_id='start_task'
    )
    generate_account_dimension_data = PythonOperator(
        task_id='generate_account_dim_data',
        python_callable=gen_account_dim_data
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_account_dimension_data >> end
