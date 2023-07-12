from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sales_data_dag',
    default_args=default_args,
    description='Extract, transform and load sales data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 10),
    catchup=False,
)

extract_sales_data = """
    CREATE TABLE IF NOT EXISTS raw_sales_data AS
    SELECT t.sales_rep_id, r.name AS region, t.amount
    FROM transactions t
    JOIN sales_reps sr ON t.sales_rep_id = sr.id
    JOIN regions r ON sr.region_id = r.id
"""

t1 = PostgresOperator(
    task_id='extract_sales_data',
    sql=extract_sales_data,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)


transform_sales_data = '''
    CREATE TABLE IF NOT EXISTS sales_summary AS
    SELECT regions.name AS region, sales_reps.name AS sales_representative,
        COUNT(*) AS total_transactions,
        SUM(raw_sales_data.amount) AS total_sales_amount
    FROM raw_sales_data
    JOIN sales_reps ON raw_sales_data.sales_rep_id = sales_reps.id
    JOIN regions ON sales_reps.region_id = regions.id
    GROUP BY regions.name, sales_reps.name;
'''

t2 = PostgresOperator(
    task_id='transform_sales_data',
    sql=transform_sales_data,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

load_sales_summary = """
    INSERT INTO sales_summary (region, sales_representative, total_transactions, total_sales_amount)
    SELECT region, sales_representative, total_transactions, total_sales_amount
    FROM sales_summary;
"""

# updates the orders_summary table with the aggregated data.
t3 = PostgresOperator(
    task_id='load_sales_summary',
    sql=load_sales_summary,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

drop_raw_sales_data = '''
DROP TABLE raw_sales_data;
'''

t4 = PostgresOperator(
    task_id='drop_raw_sales_data',
    sql=drop_raw_sales_data,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

drop_sales_summary = '''
DROP TABLE sales_summary;
'''

t5 = PostgresOperator(
    task_id="drop_sales_summary",
    sql=drop_sales_summary,
    postgres_conn_id="ilhaam-batching-airflow",
    dag=dag,
)

t1 >> t2 >> t3 >> [t4, t5]
