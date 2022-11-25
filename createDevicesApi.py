import psycopg2
import logging
import json
import sys
import os
import traceback

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
    logger.info("EVENT",event)
    logger.info(context)
    
    print("EVENT",event)
    print(context)
    
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        
        body = json.dumps(event)
        dictionary = json.loads(body)
        
        userId = dictionary['userId'] 
        ipAddress = dictionary['ipAddress']
        device = dictionary['device']
        platform = dictionary['platform']
        platformVersion = dictionary['platformVersion']
        browser = dictionary['browser']
        browserVersion = dictionary['browserVersion']
        isMobile = dictionary['isMobile']
        createdAt = dictionary['createdAt']
        updatedAt = dictionary['updatedAt']
        
        record_to_insert = (userId,ipAddress,device,platform,platformVersion,browser,browserVersion, isMobile,createdAt,updatedAt)
        postgres_insert_query = """ INSERT INTO public.devices( user_id, ip_address, device, platform, platform_version, 
                            browser, browser_version, is_mobile, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
                            
        cursor.execute(postgres_insert_query, record_to_insert)
        user = cursor.fetchone()[0]
        connection.commit()
        
        return {
            'statusCode': 200, 
            'headers': {
                'headers': { 'Content-Type': 'application/json' },
            },
            'body': json.dumps({
                "message": "Record inserted successfully",
                "UserId": user
            })
        }
                
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into public.devices  table", error)
        return log_err ("ERROR: Cannot execute cursor.\n{}".format(
            traceback.format_exc()) ) 

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")