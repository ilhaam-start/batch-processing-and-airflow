# Stretch Exercises

These tasks are by no means part of the module learning objectives. However,
these are helpful to allow you to expand your current knowledge. And also to
allow you to learn things we may have intentionally skipped in this curriculum.

Please, work on these only if you find yourself with extra time this week.

You can do any of them in any order you want.

## AWS Security Groups

You may not have come across this or realised it was a thing for your EC2
instance, and that's because the whole infrastructure was set up for you
already.

However, when you need to set up your own EC2 instance from scratch, you need to
define permissions to decide which connections are allowed to and from your
instance.

This is controlled by a resource named **Security Group** in AWS, where you are
able to define:
1. `Inbound rules`: These define the external sources (IP addresses, ports) that
   are allowed to initiate a connection to your instance. It essentially
   controls who is allowed to send incoming traffic to your EC2 instance.
2. `Outbound rules`: These define the destinations (IP addresses, ports) that
   your instance is allowed to initiate a connection to. It controls where your
   EC2 instance is allowed to send outgoing traffic.

:question: Could you map (based on your understanding now after having completed
the challenge) what inbound and outbound connections were needed throughout the
project?

<details>
  <summary>Hint</summary>

  It would help you to go back to the beginning of the project and trace all the
  actions you performed to get Airflow connected to both RDS instances.
</details>

<!-- OMITTED -->


## Complex Airflow interval schedules

So far, we have seen how to schedule tasks so they run every day (`days = 1`),
or every 15 minutes, (`minutes=15`), using `timedelta` from the `datetime`
library.

:question: But what if you want the DAG to run every 3 hours or every Monday at
9 AM? How would you set the `schedule_interval`?

<details> 
   <summary>Hint</summary>

   For complex schedules, Airflow supports cron-like expressions. 

   Scheduling a task to run every 3 hours could look something like this:
   schedule_interval='0 */3 * * *'
</details>


<!-- OMITTED -->


## Error handling in pipelines

Error handling is also crucial in data pipelines.

This can involve setting up alerts for pipeline failures, using Airflow's
built-in retry functionality, or designing your tasks to be idempotent so they
can be safely retried after a failure.

Imagine you are setting up a data pipeline that extracts data from a web API.
APIs are not always as reliable as we would like. They can go down, be slow or
exceed rate limits.

:question: What would you consider adding to your extraction task to handle
error and make this step more robust against potential failures?

<details>
  <summary>Hints</summary>

  For example, you could retry failing tasks if failure is related to temporary
  network issues. How would you do that in Airflow?
</details>

<!-- OMITTED -->

## Adding a Dashboarding tool

Metabase is an open-source platform that provides an intuitive and user-friendly
interface for querying your database and creating visualisations and dashboards.

It's a great tool for exploring data and sharing insights with your team.

In this project, we are going to set up Metabase locally using
[Docker](../pills/docker.md) and connect it to our RDS analytical database.

This way, we can visualise the data being loaded by our Airflow pipeline and get
insights into the batched data.

This is especially useful when needing to present the data to stakeholders.

Go through the following subsections:


### Install Metabase locally using Docker:

<!-- OMITTED -->

You can use the following Docker command to pull and run the Metabase image:

```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

:question: This command is supposed to run Metabase locally on your machine. How
can you verify it's up and running?

<details>
  <summary>Hint</summary>

   The key to know where you should check to see if Metabase is running is
   understanding this bit: `-p 3000:3000`. Research the Docker documentation as an
   extra task to find out more about the `p` flag.

   If you encounter any issues, check the Docker logs for the Metabase container
   using docker logs metabase. 
</details>

<!-- OMITTED -->

### Connecting Metabase to our RDS analytical database

Once you've set up Metabase, you can add your RDS analytical database as a data source.

You will need the following information about your RDS instance: hostname, port,
database name, username, and password.

:question: How can you connect your RDS analytical database to Metabase and
successfully test the connection?

<details>
   <summary>Hint</summary>

   In Metabase, go to "Admin" -> "Databases" -> "Add database". Select the type
   of your RDS database (e.g., PostgreSQL), and enter the required information.
</details>

<!-- OMITTED -->

### Explore data and create visualisations

Now that Metabase is connected to your database, you can start exploring your
data.

Metabase provides a "question" interface where you can write SQL queries or use
a GUI to interact with your data.

:question: Can you create a simple report using Metabase? Try to create a
visualisation that shows how your data changes over time.

<details>
   <summary>Hint</summary>

   In Metabase, go to "Ask a question" -> "Native query". Here you can write your
   SQL query and then choose how to visualise the results.
</details>

<!-- OMITTED -->

By the end of this exercise, you should be able to monitor the results of your
Airflow pipeline in real-time using Metabase.

This will not only give you a better understanding of your data but also make
your pipeline more transparent and easier to debug.

Happy data exploring!


<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F04_stretch_tasks.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F04_stretch_tasks.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F04_stretch_tasks.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F04_stretch_tasks.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F04_stretch_tasks.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
