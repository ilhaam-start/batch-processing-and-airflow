# Understanding Idempotence and Reproducibility in Data Pipelines

_**This is a Makers Bite.** Bites are designed to train specific skills or
tools. They contain an intro, a demonstration video, some exercises with an
example solution video, and a challenge without a solution video for you to test
your learning. [Read more about how to use Makers
Bites.](https://github.com/makersacademy/course/blob/main/labels/bites.md)_


Explain what we mean by reproducibility/idempotence in the context of data
pipelines and why they matter.


## Introduction

You have already used some of these principles without realising!

Do you remember when we altered the table in our database when we were setting
up our environment for the batching bites we have just finished?

We run this query:

```sql
ALTER TABLE orders_summary
ADD CONSTRAINT unique_summary_date UNIQUE (summary_date);
```

_At the time, it did not make a lot of sense to go much in depth about it, but it
aligns quite well with our lessons now._

Let's have a look at [our first DAG](../batching_bites//02_your_first_dag_in_airflow_bite.md).

:rotating-light: Reflect through the following questions before checking the answers!

- :question: If you were to run the DAGs multiple times, would they produce the
  same result each time?

<details>
  <summary>Answer</summary>

  Yes, running the DAG multiple times should produce the same result each time.

  The unique constraint on the summary_date column ensures that there won't be
  duplicate entries for the same date in the orders_summary table. The ON
  CONFLICT clause in the update_orders_summary task takes care of updating the
  existing summary records instead of inserting new ones, which makes the DAG
  idempotent.
</details>

- :question: Would the data in the target tables be free of duplicates or stale
  data?

<details>
  <summary>Answer</summary>

  Yes, the data in the target table orders_summary should be free of duplicates
  and stale data.
  
  The unique constraint on the summary_date column prevents duplicate entries,
  and the ON CONFLICT clause in the update_orders_summary task updates the
  existing summary records with the new aggregated data, ensuring that the data
  remains fresh and up-to-date.
</details>

- :question: How would the DAGs handle changes in business logic or failure
  scenarios?

<details>
  <summary>Answer</summary>

  The DAG handles failure scenarios by retrying the tasks with a 5-minute delay
  between retries, as specified in the retry_delay parameter in `default_args`.
  
  If the business logic changes, the SQL queries within the DAG would need to be
  updated accordingly.
  
  If the DAG is designed to be idempotent and reproducible, it should be able to
  handle these changes and still produce consistent results upon rerunning the
  updated DAG.
</details>


Let's now see what these two concepts really mean:


**What do we mean with Idempotence?**
An operation is idempotent when calling it multiple times does not have a
different result compared to calling the operation once.


**And what about Reproducibility?**
A data transformation is reproducible if it can be executed multiple times and
still produce the same result.


## Exercise

The following DAG could have been a possible solution for the third batching bite:

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'financial_dag_correct',
    default_args=default_args,
    description='A financial data extraction and loading DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 4, 28),
    catchup=False,
)

def extract_financial_data(ti):
    mysql_hook = MySqlHook(mysql_conn_id='financial-mariadb')
    query = """
        SELECT account_id, COUNT(*) AS total_transactions, SUM(amount) AS total_amount
        FROM trans
        GROUP BY account_id;
    """
    financial_data = mysql_hook.get_pandas_df(sql=query)
    
    financial_data_dict = financial_data.to_dict(orient='records')
    ti.xcom_push(key='financial_data', value=financial_data_dict)

def load_account_summary(ti):
    financial_data_dict = ti.xcom_pull(key='financial_data', task_ids='extract_financial_data')
    financial_data = pd.DataFrame(financial_data_dict)
    
    postgres_hook = PostgresHook(postgres_conn_id='batching-airflow')
    
    create_account_summary = """
        CREATE TABLE IF NOT EXISTS account_summary (
            account_id INT PRIMARY KEY,
            total_transactions INT,
            total_amount NUMERIC
        );
    """
    postgres_hook.run(create_account_summary)

    for _, row in financial_data.iterrows():
        insert_query = """
            INSERT INTO account_summary (account_id, total_transactions, total_amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (account_id) DO UPDATE
            SET total_transactions = EXCLUDED.total_transactions,
                total_amount = EXCLUDED.total_amount;
        """
        postgres_hook.run(insert_query, parameters=(row['account_id'], row['total_transactions'], row['total_amount']))

t1 = PythonOperator(
    task_id='extract_financial_data',
    python_callable=extract_financial_data,
    provide_context=True,
    dag=dag,
)

t2 = PythonOperator(
    task_id='load_account_summary',
    python_callable=load_account_summary,
    provide_context=True,
    dag=dag,
)

t1 >> t2
```

Your task is to answer the following questions:


- :question: How does the DAG ensure that it produces the same result each time,
  even when executed multiple times?

<details>
  <summary>Answer</summary>

  The DAG ensures that it produces the same result each time by using an INSERT
  operation with an ON CONFLICT clause when inserting data into the
  account_summary table.
  
  This ensures that when there's a conflict with the account_id primary key, the
  existing records will be updated instead of inserting duplicates. This
  approach makes the data pipeline idempotent.
</details>

- :question: How does the DAG handle duplicate records or conflicts in the
  account_summary table?

<details>
  <summary>Answer</summary>

  The DAG handles duplicate records or conflicts in the account_summary table
  using the ON CONFLICT clause in the INSERT operation.

  When a conflict occurs with the primary key account_id, the existing record is
  updated with new values for total_transactions and total_amount, ensuring that
  duplicate records are not inserted.
</details>


## Recap

Hopefully these two concepts with really difficult names make a bit more sense
now!

I would like us to finish this brief bite going through some of the reasons why
these are important in data pipelines:

**Why do these matter across data pipelines?**

* To avoid duplicated data
* To preserve data consistency
* To ensure pipelines can handle changes in business logic or failure scenarios
* Easier retries: Ensuring your data transformations are idempotent and
  reproducible makes it easy to retry failed operations without creating
  duplicates or leaving stale data behind.
* Consistent results: By making your data transformations idempotent and
  reproducible, you can ensure consistent results across multiple runs,
  regardless of changes in business logic or timing.


[Next Challenge](02_implementing_strategies_to_achieve_idempotence_and_reproducibility_bite.md)

<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F01_understanding_idempotence_and_reproducibility_in_data_pipelines_bite.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F01_understanding_idempotence_and_reproducibility_in_data_pipelines_bite.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F01_understanding_idempotence_and_reproducibility_in_data_pipelines_bite.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F01_understanding_idempotence_and_reproducibility_in_data_pipelines_bite.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F01_understanding_idempotence_and_reproducibility_in_data_pipelines_bite.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
