# EC2 Setup

So now we are familiar with the project we are working on for the rest of the
module, great!

Now we need to jump on the main Cloud resource within our infrastructure, the
one we fully control and where magic happens: **our EC2 instance.**

For a complete setup, we need to:
1. Make sure we can access our EC2 instance as if we were in our own machine!
2. Set up Apache Airflow in our EC2 instance


## Accessing our instance

The first step in this project is to access the EC2 instance that has been set
up for you. To do this, you'll need to use a secure shell (SSH) connection.

**And what is SSH?**

SSH is a cryptographic network protocol that allows secure remote login from one
computer to another. SSH is commonly used to log into remote servers and execute
commands.

:question: What do you think you need to establish an SSH connection to your EC2
instance?

[This resource](https://asf.alaska.edu/how-to/data-recipes/connect-to-ec2-with-ssh-mac-os-x/) should help with this.

<details>
  <summary>Please give me another hint!</summary>

  You will need the public IP address of your EC2 instance and the private key
  from the key-value pair that was created for the instance.
</details>

Once you think you have everything you need to access the EC2 instance via SSH
from your terminal, let your coach know!

<!-- OMITTED -->



## Setting up Apache Airflow

At this point, you should be able to access your instance (please do not proceed
if that is not the case!).

Now we would like to set up our instance to start working with Apache Airflow to
create our data pipeline.

:question: What would be your approach to install Apache Airflow in the
instance?

We have two options:
1. We install it globally in the EC2 instance
2. We install it within a virtual environment (`venv`) in the EC2 instance

:question: Which one do you prefer?

<details>
  <summary>Find out more!</summary>

  You know this already, but when working on a Python project it's considered
  good practice to keep our project's dependencies isolated from other projects.

  And this is the main reason why we should use a `venv` here as well.

  If you think about it, running the project inside an EC2 instance is not much
  different from running it locally, when you have 1+ projects.

</details>

Having reflected on the above questions, go ahead and install Apache Airflow.


### Airflow credentials

So now we have installed Airflow, then we access it on the corresponding port
(same as we did locally).

However, we need to log in. We then try and use the same credentials we used
when we worked on the previous Airflow project. It does not work.

:question: What is going on?

<details>
  <summary>Find out more!</summary>

  Well, the key here is to understand that we cannot use the same credentials we
  created before because the previous Airflow instance on our local machine is
  separate from the one we have created on the EC2 instance.

  Therefore, the user we created locally won't be available inside our EC2.

  If you want to use the same credentials on the EC2 instance, you will need to
  create a new user on the EC2 instance with the same username and password as
  you used locally
</details>

<!-- OMITTED -->



### Connections to DBs

We could create our first DAG file for our Data Pipeline. And then add the DB
connection details within the DAG so that we can perform the ETL process.

:question: What do you think of this approach?

<details>
  <summary>Find out more!</summary>
  Well, it's an option, but not one that follows best practices.

  If you remember from the examples running Airflow locally, we saw a much
  better way of handling connections.

  That was using the Connection IDs approach within Airflow, so that we could
  establish two connections (one against the source DB and the other one against
  the destination DB).
</details>


So, now that you have reflected on this important question, you will need some
details to connect to both databases.

:information-source: Your coach should have provided you already with the
details you need for both databases. If you don't have these details yet, please
ask your coach.

<!-- OMITTED -->

## What's next?

Now that we have Apache Airflow fully set up in our EC2 instance, it's time for
us to tackle the guided exercises to set up our first Data Pipeline in the
Cloud!


## Resources

- [AWS Docs: Connecting to EC2 via SSH](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)


[Next Challenge](02_warming_up.md)

<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F01_ec2_setup.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F01_ec2_setup.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F01_ec2_setup.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F01_ec2_setup.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=data_pipelines_with_airflow%2F01_ec2_setup.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
