import psycopg2
import logging
import json
import sys
import os

# postgresql config
host  = os.environ.get('RDS_HOST')
user = os.environ.get('RDS_USER')
password = os.environ.get('RDS_PASSWORD')
database = os.environ.get('RDS_DATABASE')
port = os.environ.get('RDS_PORT')


logger = logging.getLogger()
logger.setLevel(logging.INFO)
    
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
    rows = []
    # logger.info("EVENT",event)
    logger.info(context)
    
    # print("EVENT",event)
    print(context)
    
    try:
        connection = create_connection()
        cursor = connection.cursor()

        postgres_read_all_query = "SELECT * FROM public.devices;"  
        cursor.execute(postgres_read_all_query)
        colnames = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        for values in results:
            # rows.append(values)
            res = dict(map(lambda i,j : (i,j) , colnames,values))
            rows.append(res) 
            

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(rows, indent=4, sort_keys=True, default=str)
        }
        
    except (Exception, psycopg2.Error) as error:
        print("Hubo un error: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")