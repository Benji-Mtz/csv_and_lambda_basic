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

def lambda_handler(event, context):
    rows = []
    logger.info(event)
    logger.info(context)
    
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        if event['httpMethod'] =="GET":
            postgres_read_all_query = "SELECT * FROM public.users;"  
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
        
        if event['httpMethod']=="POST":
            postgres_insert_query = """ INSERT INTO public.devices( user_id, ip_address, device, platform, platform_version, 
                                    browser, browser_version, is_mobile) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        
            body = json.dumps(event["body"])
            dictionary = json.loads(body)
           
            userId = dictionary['user_id']
            ipAddress = dictionary['ip_address']
            device = dictionary['device']
            platform = dictionary['platform']
            platformVersion = dictionary['platform_version']
            browser = dictionary['browser']
            browserVersion = dictionary['browser_version']
            isMobile = dictionary['is_mobile']
    
            record_to_insert = (userId,ipAddress,device,platform,platformVersion,browser,browserVersion, isMobile)

            cursor.execute(postgres_insert_query, record_to_insert)
            cursor.commit()
            
            return { 
                'statusCode': 201, 
                'headers': { 
                    'Content-Type': 'application/json'
                },
                'body': json.dumps('Record inserted successfully')
            }
  
    except (Exception, psycopg2.Error) as error:
        print("Hubo un error: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")



{
    "user_id": 1,
    "ip_address": "192.168.1.0",
    "device": "iphone",
    "platform": "swift",
    "platform_version": "10.0",
    "browser": "safari",
    "browser_version": "12.0",
    "is_mobile": true
}

{
    "user_id": 2,
    "ip_address": "192.168.1.33",
    "device": "Andrdoide",
    "platform": "swift",
    "platform_version": "10.0",
    "browser": "safari",
    "browser_version": "12.0",
    "is_mobile": false
}

{
    "userId": 2,
    "ipAddress": "192.168.1.33",
    "device": "Andrdoide",
    "platform": "swift",
    "platformVersion": "10.0",
    "browser": "safari",
    "browserVersion": "12.0",
    "isMobile": false,
    "createdAt":"2022-10-13 00:00:00.000",
    "updatedAt":"2022-10-13 00:00:00.000"
}



"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,en;q=0.8",
"Cache-Control": "max-age=0",
"CloudFront-Forwarded-Proto": "https",
"CloudFront-Is-Desktop-Viewer": "true",
"CloudFront-Is-Mobile-Viewer": "false",
"CloudFront-Is-SmartTV-Viewer": "false",
"CloudFront-Is-Tablet-Viewer": "false",
"CloudFront-Viewer-Country": "US",
"Host": "1234567890.execute-api.us-east-1.amazonaws.com",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Custom User Agent String",
"Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
"X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
"X-Forwarded-For": "127.0.0.1, 127.0.0.2",
"X-Forwarded-Port": "443",
"X-Forwarded-Proto": "https"
8189

arn:aws:logs:us-east-1:458230157113:log-group:/aws/apigateway/devices:*

aws lambda add-permission --function-name arn:aws:lambda:us-east-1:458230157113:function:apiVectorAzulDevices --source-arn arn:aws:execute-api:us-east-1:458230157113:6euts42pb4/*/POST/devices --principal apigateway.amazonaws.com --statement-id apigateway-access --action lambda:InvokeFunction

arn:aws:lambda:us-east-1:458230157113:function:apiVectorAzulDevices
arn:aws:execute-api:us-east-1:458230157113:6euts42pb4/*/POST/devices

Username = dictionary['username'] 
        Firstname = dictionary['firstname']
        Firstsurname = dictionary['firstsurname']
        Secondsurname = dictionary['secondsurname']
        Email = dictionary['email']
        Lastlogin = dictionary['lastlogin']
        Created = dictionary['created'] 
        Emailverified = dictionary['emailverified']
        
{
"username":"Benji",
"firstname":"mtz",
"firstsurname":"ben",
"secondsurname":"mart",
"email":"benji@gmail.com",
"lastlogin":"ayer",
"created":"hoy",
"emailverified":"true"
}

# userId = dictionary[100]
# ipAddress = dictionary[1]
# device = dictionary[2]
# platform = dictionary[3]
# platformVersion = dictionary[4]
# browser = dictionary[5]
# browserVersion = dictionary[6]
# isMobile = dictionary[7]

"queryStringParameters": {
    "foo": "bar",
}

{
    "httpMethod": "POST",
    "body": {
    "userId": 24,
    "ipAddress": "192.168.1.33",
    "device": "Mozilla",
    "platform": "swift",
    "platformVersion": "10.0",
    "browser": "safari",
    "browserVersion": "12.0",
    "isMobile": false,
    "createdAt":"2022-10-13 00:00:00.000",
    "updatedAt":"2022-10-13 00:00:00.000"
    }
}

{
    "browserUuid": "6ecd8c99-4036-403d-bf84-cf8400f67836",
    "userId": 24,
    "utmSource": "vector.com.mx",
    "utmCampaign": "Campaign 2040",
    "utmTerm": "Beta",
    "utmContent": "Invitacion para adolecentes",
    "utmMedium": "vector.com.mx",
    "referrer": "false",
    "createdAt":"2022-10-13 00:00:00.000",
    "updatedAt":"2022-10-13 00:00:00.000"
}

40e6215d-b5c6-4896-987c-f30f3678f608
6ecd8c99-4036-403d-bf84-cf8400f67836
3f333df6-90a4-4fda-8dd3-9485d27cee36



{
    "user_id": 7,
    "bank":"BBVA",
    "clabe":"123416789123456789"
}

