import json
from secret_manager import get_secret
import psycopg2
import boto3
import urllib.parse


def lambda_handler(event, context):

    try:

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        secret = json.loads(get_secret()["SecretString"])
        user = secret.pop("username")

        secret.pop("dbClusterIdentifier")
        secret.pop("engine")

        iam = boto3.resource("iam")
        role = iam.Role("d2b-internal-dev-oluwasayo-redshift-role")

        conn = psycopg2.connect(user=user, dbname="dev", **secret)
        cursor = conn.cursor()

        query = f"""
        COPY business_data
        FROM 's3://{bucket}/{key}'
        iam_role '{role.arn}'
        FORMAT AS PARQUET;
        """
        cursor.execute(query)
        conn.commit()

        print({'statusCode': 200, 'body': 'loaded data successfully.'})

    except Exception as e:
        print("Error Occured: ", str(e))

    finally:
        cursor.close()
        conn.close()
