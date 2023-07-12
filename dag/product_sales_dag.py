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
    'product_sales_dag',
    default_args=default_args,
    description='Extract, transform and load product sales data into a summary table',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 10),
    catchup=False,
)

extract_product_sales_data = """
    CREATE TABLE IF NOT EXISTS raw_product_sales_data AS
    SELECT product_id, quantity
    FROM product_sales;
"""

t1 = PostgresOperator(
    task_id='extract_product_sales_data',
    sql=extract_product_sales_data,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)


transform_product_sales_data = '''
    CREATE TABLE IF NOT EXISTS product_sales_summary AS
    SELECT product_id, SUM(quantity) AS total_quantity
    FROM raw_product_sales_data
    GROUP BY product_id;
'''

t2 = PostgresOperator(
    task_id='transform_product_sales_data',
    sql=transform_product_sales_data,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

load_product_sales_summary = """
    INSERT INTO product_sales_summary (product_id, total_quantity)
    SELECT product_id, total_quantity
    FROM product_sales_summary;
"""

# updates the orders_summary table with the aggregated data.
t3 = PostgresOperator(
    task_id='load_product_sales_summary',
    sql=load_product_sales_summary,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

drop_raw_product_sales_data = '''
DROP TABLE raw_product_sales_data;
'''

t4 = PostgresOperator(
    task_id='drop_raw_product_sales_data',
    sql=drop_raw_product_sales_data,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

drop_product_sales_summary = '''
DROP TABLE product_sales_summary;
'''

t5 = PostgresOperator(
    task_id="drop_product_sales_summary",
    sql=drop_product_sales_summary,
    postgres_conn_id="ilhaam-batching-airflow",
    dag=dag,
)

t1 >> t2 >> t3 >> [t4, t5]