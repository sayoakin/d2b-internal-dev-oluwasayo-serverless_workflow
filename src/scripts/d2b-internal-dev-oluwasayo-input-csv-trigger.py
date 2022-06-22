import io
import boto3
import pandas as pd
import urllib.parse
from pathlib import Path
from datetime import date
from schema import SCHEMA

s3 = boto3.client('s3')


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],
                                    encoding='utf-8')
    print(f"Key: {key} \n Bucket: {bucket}")
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = io.StringIO(response['Body'].read().decode('utf-8'))
        df = pd.read_csv(data,
                         dtype=dict(first_name=str,
                                    last_name=str,
                                    email_address=str),
                         parse_dates=['date_of_visits'])

        df.rename(columns={'number_of_vists': 'number_of_visits'},
                  inplace=True)

        print(df.info())
        today = date.today().strftime('%Y/%m/%d')
        path = Path(f'/tmp/{today}')
        path.mkdir(parents=True, exist_ok=True)
        output_bucket = 'd2b-internal-dev-oluwasayo-serverless-parquet-output'
        output_filename = 'business_data.parquet'
        df.to_parquet(path / output_filename, schema=SCHEMA, index=False)
        s3.upload_file(str(path / output_filename),
                       Bucket=output_bucket,
                       Key="YEAR=<{}>/MONTH=<{}>/DAY=<{}>/{}".format(
                           *today.split('/'), output_filename))
        print("File converted to parquet and loaded to output")
        return "ok"
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'
            .format(key, bucket))
        raise e
