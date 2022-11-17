import boto3
import awswrangler as wr
from urllib.parse import unquote_plus


def lambda_handler(event, context):
    
    # Get the staging bucket and object name passed to lambda
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        
        # Gather important info: databse name, table name etc
        key_list = key.split("/")
        print(f'key_list: {key_list}')
        db_name = key_list[len(key_list) - 3]
        table_name = key_list[len(key_list) - 2]
        file_name = key_list[len(key_list) - 1]
        file_prefix = file_name.split(".")[0]
        
        print(f'Bucket: {bucket}')
        print(f'Key: {key}')
        print(f'DB Name: {db_name}')
        print(f'Table Name: {table_name}')
        print(f"File prefix: {file_prefix}")
        
        input_path = f"s3://{bucket}/{key}"
        print(f'Input path: {input_path}')
        output_path = f"s3://etl1-transformed/{db_name}/{table_name}"
        print(f'Output path: {output_path}')
        
        
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
            
        print("RESULT: ")
        print(f"result")
        
        return result
