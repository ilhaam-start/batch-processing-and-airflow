# Warming up

Before we dive into the tasks for the project, we are doing to warm up a bit!

## Running Airflow inside EC2

We learned earlier this week that in order to run our Airflow tasks we need to
run the webserver and also the scheduler, in parallel.

:question: What is your plan to do this inside your EC2 instance?

<details>
  <summary>Find out more!</summary>

  As I see it, you have two options:
  1. You can open different terminal tabs and connect to the EC2 instance in all
     of them; OR
  2. You could use a tool such as
     [TMUX](https://dev.to/dnsinyukov/guide-to-tmux-terminal-that-remembers-everything-39aa)
     - Which will allow you to run multiple terminals within one window.

  I personally prefer the second method, but both are perfectly fine and valid!
</details>


## Your first task in the Cloud

Your first task will be print the following message within Airflow: `Hello from
the test DAG!`

You should be able to find where this gets printed.


<!-- OMITTED -->

## Scheduling your DAGs

A crucial feature of Apache Airflow (and of batching in general) is the ability
to schedule tasks. This is done using the `schedule_interval` argument when
creating a DAG.

:information-source: You have come across this already, however this was not a
central feature of the previous Airflow DAGs earlier this week, hence why we
haven't discussed it until now!

:question: But what if you want the DAG to run every 5 minutes? How would you
set the schedule_interval?

<!-- OMITTED -->

## Monitoring our Data Pipeline

Earlier this week, we got a bit or familiarity already with the Graph view inside
Airflow, which showed different boxes, each representing a task within our DAG
file.

In case you need a refresher, [this is the screenshot](../assets/successful-airflow-flow.png) we used to illustrate it.

Now it is time for us to expand on that knowledge a bit more.

These are a few key components of the Airflow UI:

### DAG Runs

This page gives an overview of the runs of a specific DAG.

Here, you can see the state of each run (e.g., running, success, failed), the
execution date, and the run duration.

### Graph View

This is the one shown in the screenshot above. This view shows the DAG
structure, including tasks and dependencies.

When a DAG is running, you can see the state of each task (running, success,
failed, etc.). By clicking on a task, you can access more detailed information
such as logs and task instance details.

### Task Duration

This page provides a historical graph of the duration of the tasks in the DAG.

This can be useful for identifying tasks that are taking longer to run than
expected.

### Gantt Chart

This chart visualises the execution timeline of the tasks in a DAG run. It can
be useful for identifying bottlenecks in the DAG.

These may come handy when working on more complex processes within Airflow.

The last two form a great combo in maintaining and optimising your data
pipelines.

Bear them in mind!


## What's next?

Great, we have already warmed up and are ready now to tackle the project tasks!

Good luck :star:


[Next Challenge](03_project_tasks.md)

<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F02_warming_up.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F02_warming_up.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F02_warming_up.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F02_warming_up.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F02_warming_up.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
