# Project tasks

These tasks will require you to not only write some code, but also to think
about design considerations and trade-offs!

Remember that we are working with the Stackoverflow source RDS database.

These may feel hard at times, but you will learn a ton as a result. And your
coaches will be here to guide you.

Good luck, you've got this! :star:

## Tasks

### Task 1

Your company wants to ensure that all posts loaded into the target database have
a body field that is not empty. This is to ensure data quality and consistency
in the target database. Additionally, the company wants to avoid reprocessing
the same data every time the ETL process runs.

To achieve this, you have been tasked with setting up an ETL pipeline in Airflow
that extracts all (old and then new) posts from the source database, filters out
any posts with empty bodies, and loads them into the target database, while also
keeping track of the last processed posts.

They are interested in these fields: `id`, `title`, `body`, `owner_user_id`, and
`creation_date`.

:information-source: You will also want to filter out NULL values within the
`owner_user_id` field. Trust us on this one.

This pipeline should be scheduled to run every 15 minutes.

<!-- OMITTED -->

:question: If a task in your DAG fails, how can you find out what went wrong?

<details>
    <summary>Hint</summary>
    You can use the logs accessible from the Graph View to troubleshoot task failures.
</details>

:question: What should you keep in mind when writing your Python functions for
ETL to ensure they're idempotent?

:question: What additional consideration might you need to take into account
when dealing with a large amount of data?

<!-- OMITTED -->


<details>
  <summary>Hint!</summary>

    As we have already seen, an operation is idempotent if performing it multiple
    times has the same effect as performing it once.

    For example, deleting a row with a certain ID from a database is idempotent,
    because once the row is deleted, further delete operations with the same ID will
    not change the database.

    When writing your extraction, transformation, and loading functions, consider
    what would happen if the DAG was interrupted and had to restart from the
    beginning.

    Would your functions produce the same result, or could there be duplicate or
    missing data?

    To ensure idempotence, you might need to add checks for existing data or use
    database operations that are inherently idempotent.
</details>

:question: What do you notice in your current approach?

<details>
  <summary>Hints</summary>

  Remember to think about how you might be able to batch your operations to
  improve efficiency.

  Batching operations not only can help with memory usage but also can improve
  overall performance by reducing the number of database operations.

  **Can your EC2 instance handle the whole extraction in one go?** If not, what
  else can be done?
</details>


<!-- OMITTED -->




### Task 2

Your company has found that the body field in some of the posts contains HTML
tags which are causing issues in downstream applications.

Your task is to clean up the `body` field by removing any HTML tags before loading
the data into the target database.

<details>
  <summary>Hint</summary>

You can use a regular expression to identify and remove HTML tags from the body
field. You can use an existing library or any tools you want really!

</details>

:question: How will you store the transformed data in the target database? Will
you append it to the existing data, overwrite the existing data, create a new
table, or update only the transformed records?

:question: What are the pros and cons of each approach?

<details>
    <summary>Hint</summary> 

    Consider factors such as consistency, processing time, storage space, and the
    ability to compare or audit the data.

    There's no one-size-fits-all solution -- the best approach depends on the
    specific needs and constraints of your project.
</details>

<!-- OMITTED -->





### Task 3

Now, your company would like you to schedule your DAG to run every 7 minutes.

Additionally, the pagination limit should increase to 10,000 (previously it was
1000).

Remember to use the Airflow UI to monitor your DAG's execution and troubleshoot
any issues that arise.

:question: Can you identify which tasks in your DAG take the longest time to
run? How might you use this information to optimize your DAG?

<details>
    <summary>Hint</summary>

  You can use the Task Duration and Gantt Chart views to identify long-running
  tasks.

  Optimising your data pipeline does not focus solely on performance. In fact, you
  may not have a great opportunity to improve it greatly on this project.

  However, you could optimise your pipeline in terms of code organisation,
  readability and maintainability.
</details>


### Task 4

For a stretch task, consider how you might improve your ETL DAG, use the
following questions as guidance:

* :question: Could you parallelise any of the tasks to improve performance? 
* :question: Could you add any additional transformations to make the data more
  useful?

Remember, there's no one right answer to these questions -- they're about
thinking critically and making trade-offs based on your specific needs and
constraints.

Take your time to experiment and play with your data pipeline!

In fact, given the current state of the pipeline and what it does, it may feel a
bit forced to introduce such advanced concepts. That is alright, but it's a
great idea nonetheless that you start exploring these concepts.


## What's next?

First, congratulations for reaching this far on the project! :star:

The next section contains some stretch tasks, which you can attempt if you wish.

You could also consolidate some of the learning objectives for the week or for a
previous week if you find yourself with some extra time.


[Next Challenge](04_stretch_tasks.md)

<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F03_project_tasks.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F03_project_tasks.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F03_project_tasks.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F03_project_tasks.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F03_project_tasks.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
