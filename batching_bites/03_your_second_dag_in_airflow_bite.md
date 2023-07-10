# Your second DAG in Airflow

_**This is a Makers Bite.** Bites are designed to train specific skills or
tools. They contain an intro, a demonstration video, some exercises with an
example solution video, and a challenge without a solution video for you to test
your learning. [Read more about how to use Makers
Bites.](https://github.com/makersacademy/course/blob/main/labels/bites.md)_

Learn to orchestrate the execution of batch data processing tasks that depend on
each other using Apache Airflow.


## Introduction

In the previous bite, we worked with our own data source really. From there, we
learned how to create our first data pipeline using a batch processing approach
with Airflow.

In this one, we are going to do the same. However, we will not be using our own
data source. Instead, we will use a third-party, cloud-based data source.

We used [this one](https://relational.fit.cvut.cz/dataset/Financial) already in
the previous module.

Please note that as part of this bite we will not use a demonstration as most of
the learning objectives were demonstrated in the previous one.

There will be some additional challenges in this one though!


## Exercise

You are given an Airflow DAG that extracts data from the Financial dataset
available at https://relational.fit.cvut.cz/dataset/Financial (hosted on a
MariaDB database) and loads it into a local PostgreSQL database.

The goal is to create a table containing the account ID, the total number of
transactions, and the total amount of transactions for each account.

E.g.
* `account_id` => 1
* `total_transactions` => 239
* `total_amount` => 375192.0

A data engineer in your team has put this DAG together and has asked you to test
it.

This is the DAG:

  <!-- OMITTED -->

```python
    from datetime import datetime, timedelta
    from airflow import DAG
    from airflow.providers.mysql.operators.mysql import MySqlOperator
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
        postgres_conn_id='local_postgres',
        dag=dag,
    )

    extract_financial_data = """
        SELECT account_id, COUNT(*) AS total_transactions, SUM(amount) AS total_amount
        FROM trans
        GROUP BY account_id
        INTO OUTFILE '/tmp/account_summary.csv'
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"'
        LINES TERMINATED BY '\n';
    """

    t2 = MySqlOperator(
        task_id='extract_financial_data',
        sql=extract_financial_data,
        mysql_conn_id='financial_mariadb',
        dag=dag,
    )

    load_account_summary = """
        COPY account_summary(account_id, total_transactions, total_amount)
        FROM '/tmp/account_summary.csv' WITH CSV;
    """

    t3 = PostgresOperator(
        task_id='load_account_summary',
        sql=load_account_summary,
        postgres_conn_id='local_postgres',
        dag=dag,
    )

    t1 >> t2 >> t3
```

<!-- OMITTED -->

<details>
  <summary>DAG hints</summary>

  Ask yourself the following questions:
  * How many connections do I need now in Airflow?

    <!-- OMITTED -->

  * How can I transfer data between different database systems, such as
    MariaDB and PostgreSQL?
</details>


:rotating_light: :rotating_light: **What did you notice?**

<details>
  <summary>Click here to find out more!</summary>

  There seems to be an issue on one of the tasks for the given DAG.

  It seems we are trying to do something we are not allowed to do. What could it
  be?

  As a hint, analyse the implementation Python script for the second etl bite
  from the previous module.
  _Note: This is the one where we used the Financial dataset previously!_

  When you are ready, proceed to the next section of this bite...
</details>

<!-- OMITTED -->

## Challenge

:satellite: This is a submission point, please work on it solo and submit your
work using [this form](https://airtable.com/shrvo9ePjlwnaiLv5?prefill_Item=batch_processing_batching_bites03) when you are done.

Find a way to modify the given DAG for this bite so that the process can work.

Put together a document where you show your thinking process, explain the nature
of the problem and your documented solution.

Feel free to use screenshots or any materials you have used!


[Next Challenge](04_data_transformations_in_the_cloud_bite.md)

<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F03_your_second_dag_in_airflow_bite.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F03_your_second_dag_in_airflow_bite.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F03_your_second_dag_in_airflow_bite.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F03_your_second_dag_in_airflow_bite.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F03_your_second_dag_in_airflow_bite.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
