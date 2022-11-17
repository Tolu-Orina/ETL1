# ETL 1: Automate File Format Conversion with AWS Lambda

In this Project, we configure an s3 bucket to atomatically trigger a lambda function
whenever a new ".csv" file is written to it. This Lambda converts the csv file to parquet format

## Architecture
![ETL1](https://user-images.githubusercontent.com/78595009/202572265-3035bae4-72c0-44bf-b297-0bede7ae5685.png)


## Services Used
- **Amazon S3**
- **AWS Lambda**
- **AWS Data Wrangler**
- **AWS Glue Data Catalog**

**Amazon S3** is a reliable, highly available and scalable data lake storage solution. It is easy to use and integrates with many AWS services and third-party tools used for data curation, analysis, engineering and Machine Learning. In this project Amazon S3 is used as a data lake store for both staging and load phase of the ETL (Extract, Transform, Load) process.

**AWS Lambda** is an event-driven, serverless compute platform that lets you run light weight code without worrying about provisioning servers. Here AWS lambda serves as compute platform for data transformation and conversion to parquet format (an open source, column-oriented data file format designed for efficient data storage and retrieval).

**AWS Data Wrangler**, now AWS SDK for pandas, is an open source package for reading data in the AWS ecosystem. It was created by AWS Professional Services Team at Amazon and is built on top of pandas (python's popular data wrangling tool). AWS Data Wrangler does the work of converting the csv file to parquet format.

**AWS Glue Data Catalog** is an index to the location, schema, and runtime metrics of your data. You use the information in the Data Catalog to create and monitor your ETL jobs. Information in the Data Catalog is stored as metadata tables, where each table specifies a single data store. Here It serves as the metadata reference for the destination bucket in this project

***Code Snippets***
```
# Read in the Data
input_df = wr.s3.read_csv([input_path])
        
current_databases = wr.catalog.databases()
if db_name not in current_databases.values:
    print(f"Creating Database {db_name} .....")
    wr.catalog.create_database(db_name)
else:
    print(f'Database {db_name} already exists')

print(f'Converting to {file_prefix}.parquet')
# Write to parquet in output s3 bucket
result = wr.s3.to_parquet(
    df = input_df,
    path=output_path,
    dataset = True,
    filename_prefix = file_prefix,
    database = db_name,
    table = table_name,
    mode ="append"
    )
```




https://user-images.githubusercontent.com/78595009/202561890-6e0132bd-874a-4899-8cc5-31783b6b589f.mp4

