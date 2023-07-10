# Implementing strategies to achieve idempotence and reproducibility

_**This is a Makers Bite.** Bites are designed to train specific skills or
tools. They contain an intro, a demonstration video, some exercises with an
example solution video, and a challenge without a solution video for you to test
your learning. [Read more about how to use Makers
Bites.](https://github.com/makersacademy/course/blob/main/labels/bites.md)_


Apply common strategies for making data transformations idempotent.

## Introduction

In the previous section, we learned about the important of making our data
transformations idempotent, along with some of the benefits it has on data
pipelines.

Now, we are going to see some examples of non-idempotent approaches and your
task would be to think about potential strategies to come up with an idempotent
and reproducible solution.



## Exercise

Imagine you are working for a retail company that processes daily sales data.
The company uses a data pipeline to aggregate the sales data by product category
and store it in a summary table. The pipeline is scheduled to run daily and
update the summary table with the latest sales data.

However, the team responsible for creating the pipeline didn't follow the
delete-write approach, leading to the following issue:

After a few days of running the pipeline, the company noticed that the summary
table had duplicate data. The duplicated data was causing incorrect calculations
in the company's sales reports, resulting in overestimation of sales and
affecting the company's inventory management decisions.

The company's management has asked you to investigate the issue and refactor the
data pipeline to ensure that it doesn't produce any duplicates.

Take a look at the original data transformation:

```sql
INSERT INTO sales_summary (category, total_sales, total_amount)
SELECT category, COUNT(*) AS total_sales, SUM(amount) AS total_amount
FROM daily_sales
GROUP BY category;
```

Now, think about the following questions to guide you in identifying the issue
and refactoring the transformation:

1. :question: How does the original data transformation handle existing data in the
sales_summary table when updating it with new sales data?


2. :question: Can you identify any potential issues with this data
   transformation that might lead to duplicated data?


3. :question: How can you modify the data transformation to ensure idempotence
   and reproducibility?


<details>
  <summary>Hints!</summary>

  Consider the delete-write approach for updating the summary table.

  Think about how you can delete the existing summary data for the specific date
  or category before inserting the new aggregated data.

  <details>
    <summary>Possible solution</summary>

    Delete existing summary data for the date or category:

    ```sql
    DELETE FROM sales_summary
    WHERE summary_date = '{{ ds }}';
    ```

    Insert new aggregated data:

    ```sql
    INSERT INTO sales_summary (summary_date, category, total_sales, total_amount)
    SELECT '{{ ds }}' AS summary_date, category, COUNT(*) AS total_sales, SUM(amount) AS total_amount
    FROM daily_sales
    WHERE sale_date = '{{ ds }}'
    GROUP BY category;
    ```

    This refactored data transformation follows the delete-write principle, ensuring
    that the sales_summary table doesn't contain any stale or duplicate data.
  </details>
</details>




## Challenge

:satellite: This is a submission point, please work on it solo and submit your
work using [this form](https://airtable.com/shrvo9ePjlwnaiLv5?prefill_Item=batch_processing_idempotence_and_reproducibility02) when you are done.

In this challenge, you will work with the following dataset and your task will
be to apply one principle to create an idempotent data transformation.

Submit your code explaining what it does.

Here's the dataset:

**daily_visits dataset**

```lua
| visit_id | store_id | visit_date | visitor_count |
| -------- | -------- | ---------- | ------------- |
| 1        | 1        | 2023-05-01 | 50            |
| 2        | 1        | 2023-05-02 | 55            |
| 3        | 2        | 2023-05-01 | 60            |
| 4        | 2        | 2023-05-02 | 45            |
```

**Summary Table: store_visits_summary**
```lua
| store_id | total_visits | total_visitor_count |
| -------- | ------------ | ------------------- |
| 1        | 0            | 0                   |
| 2        | 0            | 0                   |
```

The goal is to create a data pipeline that calculates the total visits and total
visitor count for each store and updates the store_visits_summary table daily.

To help you identify a suitable idempotent solution, consider the following
questions:

1. How can you calculate the total visits and total visitor count for each store
   in the daily_visits dataset?

2. How can you update the store_visits_summary table while ensuring that the
   transformation is idempotent and reproducible?

3. Can you think of a principle or technique that would help you achieve
   idempotence in this scenario?


Feel free to play and experiment with the datasets in any way you want locally!


<!-- OMITTED -->


<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F02_implementing_strategies_to_achieve_idempotence_and_reproducibility_bite.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F02_implementing_strategies_to_achieve_idempotence_and_reproducibility_bite.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F02_implementing_strategies_to_achieve_idempotence_and_reproducibility_bite.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F02_implementing_strategies_to_achieve_idempotence_and_reproducibility_bite.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=idempotence_and_reproducibility%2F02_implementing_strategies_to_achieve_idempotence_and_reproducibility_bite.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
