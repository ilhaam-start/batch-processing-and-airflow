from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import mysql.connector as mariadb
import csv

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'financial_dag',
    default_args=default_args,
    description='A financial data extraction and loading DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 4, 28),
    catchup=False,
)

create_account_summary = """
    CREATE TABLE IF NOT EXISTS account_summary (
        account_id INT PRIMARY KEY,
        total_transactions INT,
        total_amount NUMERIC
    );
"""

t1 = PostgresOperator(
    task_id='create_account_summary',
    sql=create_account_summary,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

def fetch_data_from_mariadb():
    try:
        mariadb_conn = mariadb.connect(
                host="relational.fit.cvut.cz",
                user="guest",
                password="relational",
                database="financial"
        )
        cursor = mariadb_conn.cursor()
        query = """
            SELECT account_id, COUNT(*) AS total_transactions, SUM(amount) AS total_amount
            FROM trans
            GROUP BY account_id
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    finally:
        if cursor:
            cursor.close()
        if mariadb_conn:
            mariadb_conn.close()


def export_to_csv(**context):
    result = fetch_data_from_mariadb()
    csv_file_path = '/tmp/account_summary.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

export_to_csv_task = PythonOperator(
        task_id= 'export_to_csv',
        python_callable= export_to_csv,
        provide_context= True,
        dag=dag
    )

load_account_summary = """
    CREATE TEMPORARY TABLE temp_account_summary (LIKE account_summary);

    COPY temp_account_summary (account_id, total_transactions, total_amount)
    FROM '/tmp/account_summary.csv' WITH CSV;

    INSERT INTO account_summary (account_id, total_transactions, total_amount)
    SELECT account_id, total_transactions, total_amount
    FROM temp_account_summary
    ON CONFLICT (account_id) DO NOTHING;
"""

t2 = PostgresOperator(
    task_id='load_account_summary',
    sql=load_account_summary,
    postgres_conn_id='ilhaam-batching-airflow',
    dag=dag,
)

t1 >> export_to_csv_task >> t2