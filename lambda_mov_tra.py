import io
import os
import csv
import sys
import json
import boto3
import logging
import psycopg2
import traceback
import psycopg2.extras
from zipfile import ZipFile
from datetime import datetime, timezone

# Database config
host  = os.environ.get('RDS_HOST')
user = os.environ.get('RDS_USER')
password = os.environ.get('RDS_PASSWORD')
database = os.environ.get('RDS_DATABASE')
port = os.environ.get('RDS_PORT')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Database connection
def create_connection():
    try:
        return psycopg2.connect(
                    database=database,
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                )
    except:
        logger.error("ERROR: Could not connect to Postgres instance.")
        sys.exit()

def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg , "headers": {}, "statusCode": 400,
        "isBase64Encoded":"false"}

def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    file_name = key[0:-4]
    path = f"vec/prod/internet/fuentes/vector/info/b_techrules/data/{file_name}.txt"
    
    logger.info(event)
    logger.info(context)

    if "val" in key or "VAL" in key:
        # Get zip file from s3
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name,key)
        table = 'account_positions'

        csv.register_dialect('pipe', delimiter='|')

        # Get UTC time
        utc_dt = datetime.now(timezone.utc)
        new_utc = utc_dt.strftime('%Y-%m-%d  %H:%M:%S')

        # Dummy values
        typepos = "posiciones"
        account_id = 1

        account_positions = []

        # Read zip, get txt and create an array of the objects in the txt file
        with io.BytesIO(obj.get()["Body"].read()) as tf:
            # rewind the file
            tf.seek(0)

            with ZipFile(tf, mode='r') as zf:
                with zf.open(path, 'r') as infile:
                    reader = csv.DictReader(io.TextIOWrapper(infile, 'utf-8'), dialect='pipe')
                    
                    for row in reader:
                        # process the CSV here
                        # Orden de valores Posiciones 
                        # accountid, assetcode, valuationdate, valuation, numberassests, costvalue, assetprice, assetpricedate, typepos
                        
                        data_txt = (account_id, row['ASSET_CODE'], row['VALUATION_DATE'], row['VALUATION'], row['NUMBER ASSETS'], row['COST VALUE'], float(row['ASSET_PRICE'].replace(',','')) , row['ASSET_PRICE_DATE'], typepos, new_utc)
                        account_positions.append(data_txt)

        try:
            # Database connection
            connection = create_connection()
            cursor = connection.cursor()

            # Insert values into contract
            insert_query = f"INSERT INTO public.{table} (account_id, asset_code, valuation_date, valuation, number_assests, cost_value, asset_price, asset_price_date, type, created_at) VALUES %s RETURNING id;"
            ids = psycopg2.extras.execute_values (
                cursor, insert_query, account_positions, template='(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', fetch=True
            )

            connection.commit()

            return {
                'statusCode': 200,
                'body': {
                    'message': 'Contracts inserted successfully',
                    'ids': json.dumps(ids)
                }
            }
        
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into public.contracts table", error)
            return log_err ("ERROR: Cannot execute cursor.\n{}".format(
                    traceback.format_exc()) )

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                
    if "tra" in key or "TRA" in key:
        # Get zip file from s3
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name,key)
        table = 'account_movements'

        csv.register_dialect('pipe', delimiter='|')

        # Get UTC time
        utc_dt = datetime.now(timezone.utc)
        new_utc = utc_dt.strftime('%Y-%m-%d  %H:%M:%S')

        # Dummy values
        account_id = 1
        movement_type = 'movements'
        currency = 'MXN'

        account_movements = []

        # Read zip, get txt and create an array of the objects in the txt file
        with io.BytesIO(obj.get()["Body"].read()) as tf:
            # rewind the file
            tf.seek(0)

            with ZipFile(tf, mode='r') as zf:
                with zf.open(path, 'r') as infile:
                    reader = csv.DictReader(io.TextIOWrapper(infile, 'utf-8'), dialect='pipe')
                    
                    for row in reader:
                        # process the CSV here
                        # Orden de valores Posiciones 
                        # accountid, movementtype, assetcode, valuationdate, tradedate, tradevaluation, numberassests, tradecode, currecy, tradeassetprice, description
                        
                        data_txt = (account_id, movement_type, row['ASSET_CODE'], row['VALUATION_DATE'], row['TRADE_DATE'], row['TRADE_VALUATION'], row['NUMBER_ASSETS'], row['TRADE_TYPE CODE'], currency, row['TRADE_ASSET_PRICE'], new_utc)
                        account_movements.append(data_txt)

        try:
            # Database connection
            connection = create_connection()
            cursor = connection.cursor()

            # Insert values into contract
            insert_query = f"INSERT INTO public.{ table } (account_id, movement_type, asset_code, valuation_date, trade_date, trade_valuation, number_assests, trade_code, currency, trade_asset_price, created_at) VALUES %s RETURNING id;"
            ids = psycopg2.extras.execute_values (
                cursor, insert_query, account_movements, template='(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', fetch=True
            )

            connection.commit()

            return {
                'statusCode': 200,
                'body': {
                    'message': 'Movements inserted successfully',
                    'ids': json.dumps(ids)
                }
            }
        
        except (Exception, psycopg2.Error) as error:
            print(f"Failed to insert record into public.{ table } table", error)
            return log_err ("ERROR: Cannot execute cursor.\n{}".format(
                    traceback.format_exc()) )

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        pass
    
