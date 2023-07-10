# Data Transformations in the Cloud

_**This is a Makers Bite.** Bites are designed to train specific skills or
tools. They contain an intro, a demonstration video, some exercises with an
example solution video, and a challenge without a solution video for you to test
your learning. [Read more about how to use Makers
Bites.](https://github.com/makersacademy/course/blob/main/labels/bites.md)_


Learn how to run data transformations code in the Cloud using AWS Lambda.

## Introduction

Until now you have only run transformations locally.

Now you will get your code to run in the Cloud so it's not dependent on your
laptop (batch processing wouldn't be very reliable if it had to be done from a
person's laptop all the time!).

More granularly, in this bite you will:
* Learn how to use cloud services such as AWS Lambda and S3 for data processing
  tasks.
* Gain hands-on experience in writing data transformation scripts and deploying
  them to the cloud.


## Demonstration

We are going to demonstrate how to process a CSV file stored in an Amazon S3
bucket using an [AWS Lambda](../pills/aws_lambda.md) function. The Lambda
function will read the file, perform calculations, and save the results back to
an S3 bucket.

In this demonstration, we'll be working with a CSV file containing IMDb movie
data. We will calculate the top 10 most frequent occupations among the movie
principals, such as actors, directors, and writers.


### Setup

We first create an AWS Lambda function with Python 3.9 as the runtime. We'll
give it this role: `LambdaToS3andCloudWatchRole`.

_Note: Choose a descriptive name for it, e.g.
`JosueBatchingBites4Demonstration`. This way, I am able to identify the Lambda
against its owner (Josue) and against the scenario in the curriculum it solves._

This is the code we will need for our Lambda:

<!-- OMITTED -->

```python
import os
import csv
import boto3
from collections import Counter

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    source_bucket = os.environ['SOURCE_BUCKET'] # value => data-eng-makers-public-datasets-404544469985
    dest_bucket = os.environ['DEST_BUCKET'] # value => batching-bite-4 -- this is where your output will be saved.

    student_name = "your-name"  # Change this to your own name!

    # Download the file from S3
    s3.download_file(source_bucket, 'IMDB-dataset-files/ImdbTitlePrincipals.csv', '/tmp/title_principals.csv')
    
    # Read the file using csv module
    occupations = []
    with open('/tmp/title_principals.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            occupations.append(row['category'])

    # Calculate the top 10 most frequent occupations
    top_occupations = Counter(occupations).most_common(10)

    # Save the result as a CSV file
    with open('/tmp/top_occupations.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['occupation', 'count'])
        writer.writerows(top_occupations)
  
    # Upload the result to the destination S3 bucket in the specified folder
    s3_key = f"{student_name}/top_occupations.csv"
    s3.upload_file('/tmp/top_occupations.csv', dest_bucket, s3_key)

    return {
        'statusCode': 200,
        'body': 'Top occupations have been calculated and saved to the destination S3 bucket.'
    }
```

If you read through the code, you will realise we are using environment
variables for the source and destination buckets. This is considered good
practice, so that we do not hardcode these names and have them visible under the
lambda code.

One more thing: Lambdas have a predefined timeout for tasks execution of 3
seconds. This is not enough to be able to download and process csv files,
therefore I increased this parameter of my Lambda under the `General
configuration` tab.

**Can you find where to add the values for these variables?**

<details>
  <summary>Click here for the answer</summary>

  Open your Lambda function, and then `Configuration`. You should be able to see
  a section named `Environment variables`. That's where you need to add these
  two variables from the script. Make sure the key names match and to add the
  right values!
</details>

We then save and deploy our updated code.


### Running our Lambda

Lambdas run as a result of something else that triggers them.

For example, we could set a trigger so that anytime a new file gets added to the
bucket, the Lambda runs to perform any transformations we want.

For this demonstration, however, we will set a simple, empty trigger so that we
can test our Lambda manually and perform the necessary transformation tasks.

**Setting the trigger for our Lambda**

In the AWS Lambda console, scroll down to the "Function overview" section and
click on "Add trigger."

Select "S3" as the trigger type.

Configure the trigger:
1. Select the source S3 bucket from the "Bucket" dropdown list.
2. For "Event type," choose "All object create events".
3. In the "Prefix" field, you can specify a prefix (i.e., a folder) to limit the
   trigger to specific files within the bucket, or leave it blank to trigger on
   all uploaded files. In this case, it makes sense to set it as
   `IMDB-dataset-files/`, because that is where the dataset files for this bite
   live.
4. Leave the "Suffix" field blank unless you want to limit the trigger to
   specific file extensions.
5. Click "Add" to create the trigger.


Finally, it is time to test our Lambda. There is an event that we have created
already named `BatchingBites4`.

If you click on the little arrow next to the blue button "Test", you will be
able to locate this prefilled event. Test your lambda with it.


We then finally verify that the `top_occupations.csv` file has been uploaded to
the destination S3 bucket (within our folder) and contains the correct results.

This example demonstrates the power of AWS Lambda for processing data stored in
S3.

<!-- OMITTED -->


## Exercise

In this exercise, you will create a Lambda function that processes two CSV files
from the source S3 bucket and combines them into a single CSV file. The source
files are:

- `source_bucket/ImdbTitleBasics.csv`
- `source_bucket/ImdbTitleRatings.csv`

The Lambda function should read both files, join them on the `tconst` column,
and store the resulting CSV in the destination S3 bucket.

The output CSV file should have the following columns: `tconst`, `primaryTitle`,
`startYear`, `genres`, and `averageRating`. Save the output file as
`combinedMovies.csv`.

_Note: The purpose of this exercise is not for you to spend ages learning how to
use the `csv` module. So if you're finding yourself too caught up in this,
please refer to the solution, but nonetheless I'd recommend you give it a go as
this will enhance your researching skills!_

<details>
  <summary>Some hints</summary>

  To complete this exercise:

  1. Create a new Lambda function and use the provided IAM role for permissions.
  2. Write a Python script to read the two source CSV files, join them on the
     `tconst` column, and save the resulting file to the destination S3 bucket.
  3. Configure the S3 trigger for your Lambda function.
  4. Test your Lambda function.

  Note: You can use the provided demonstration as a starting point.
</details>

<!-- OMITTED -->

<details>
  <summary>This could be a solution</summary>

  ```python
import boto3
import csv
from io import StringIO
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = os.environ['SOURCE_BUCKET']
    dest_bucket = os.environ['DEST_BUCKET']
    title_basics_file = 'IMDB-dataset-files/ImdbTitleBasics.csv'
    title_ratings_file = 'IMDB-dataset-files/ImdbTitleRatings.csv'

    # Read ImdbTitleBasics.csv
    title_basics_obj = s3_client.get_object(Bucket=source_bucket, Key=title_basics_file)
    title_basics_data = title_basics_obj['Body'].read().decode('utf-8')
    title_basics_reader = csv.DictReader(StringIO(title_basics_data))
    title_basics_dict = {row['tconst']: row for row in title_basics_reader}

    # Read ImdbTitleRatings.csv
    title_ratings_obj = s3_client.get_object(Bucket=source_bucket, Key=title_ratings_file)
    title_ratings_data = title_ratings_obj['Body'].read().decode('utf-8')
    title_ratings_reader = csv.DictReader(StringIO(title_ratings_data))

    # Combine Data
    combined_data = []
    fieldnames = ['tconst', 'primaryTitle', 'startYear', 'genres', 'averageRating']

    for row in title_ratings_reader:
        tconst = row['tconst']
        if tconst in title_basics_dict:
            combined_row = {
                'tconst': tconst,
                'primaryTitle': title_basics_dict[tconst]['primaryTitle'],
                'startYear': title_basics_dict[tconst]['startYear'],
                'genres': title_basics_dict[tconst]['genres'],
                'averageRating': row['averageRating']
            }
            combined_data.append(combined_row)

    # Save resulting CSV to destination S3 bucket, in a folder
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)
    folder_name = 'your_name'  # Replace with the appropriate folder name
    destination_key = f"{folder_name}/combinedMovies.csv"
    s3_client.put_object(Bucket=dest_bucket, Key=destination_key, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'CSV files combined and saved to the destination S3 bucket.'
    }
  ```
</details>


<!-- OMITTED -->



## Challenge

For this challenge, you'll work with the `ImdbTitleCrew.csv` file. The file
contains columns: `tconst`, `directors`, and `writers`. Your task is to create a
new CSV file that only includes rows where there is at least one director and
one writer. 

Additionally, the output CSV should be saved in a folder within the destination
S3 bucket.

You may have to face some additional challenges for this challenge. Make sure
you read the Lambda logs and investigate possible solutions!


<!-- OMITTED -->

## Recap

In this module, we covered how to read and process CSV files stored in S3 using
AWS Lambda. We learned how to create a Lambda function, set up triggers and
permissions, and write Python code to read, transform, and write CSV files back
to S3.

It's important to note that there are other ways to perform data transformations
in the Cloud. Lambdas are fine for small transformations and source datasets.

However, other data processing services are designed to handle larger-scale
tasks.

We will explore some of these alternatives in later modules. The method you
choose depends on your specific use case, the size of the data, and the
complexity of the transformations.

Keep experimenting and honing your skills in working with AWS services and data
transformations!


<!-- BEGIN GENERATED SECTION DO NOT EDIT -->

---

**How was this resource?**  
[😫](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F04_data_transformations_in_the_cloud_bite.md&prefill_Sentiment=😫) [😕](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F04_data_transformations_in_the_cloud_bite.md&prefill_Sentiment=😕) [😐](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F04_data_transformations_in_the_cloud_bite.md&prefill_Sentiment=😐) [🙂](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F04_data_transformations_in_the_cloud_bite.md&prefill_Sentiment=🙂) [😀](https://airtable.com/shrUJ3t7KLMqVRFKR?prefill_Repository=makersacademy%2Fbatch-processing&prefill_File=batching_bites%2F04_data_transformations_in_the_cloud_bite.md&prefill_Sentiment=😀)  
Click an emoji to tell us.

<!-- END GENERATED SECTION DO NOT EDIT -->
