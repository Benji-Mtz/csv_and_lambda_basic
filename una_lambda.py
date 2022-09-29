import json
import boto3
import os
import csv
import codecs
import sys
#import time

csv.register_dialect('pipe', delimiter='|', quoting=csv.QUOTE_NONE)
counter = 0

s3 = boto3.resource('s3')
dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
                                
tableName = os.environ['nombre_tabla']

def borraTabla(table_name):
    print('Borrando tabla '+table_name)
    table = dynamodb.Table(table_name)
    table.delete()
    table.wait_until_not_exists()


def createTable(table_name):
    existing_tables = dynamodb_client.list_tables()['TableNames']
    
    if table_name not in existing_tables:
        print('Creando tabla ' + table_name)
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'Emisora',
                    'KeyType': 'HASH' # Partition key
                },
                {
                    'AttributeName': 'ID',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions= [
                {
                    'AttributeName': 'Emisora',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 100
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name,WaiterConfig={
            'Delay': 1,
            'MaxAttempts': 30
        })
    else:
        print(f'La tabla: "{ table_name }" ya existe, no fue necesario crearla.')

                                
def lambda_handler(event, context):
    print("Inicio de ejecución de carga de listas de recomedación")                             
   
    key = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']
    #obj = s3.Object(bucket, key).get()['Body']
    
    # try:
    #     print("Borrar")
    #     #borraTabla(tableName)
       
    # except Exception as e:
    #     print(e)    
    #     print("Hubo un error al eliminar la tabla "+tableName)

    try:
        print("Crear")
        createTable(tableName)

    except Exception as e:
        print(e)    
        print("Hubo un error al crear la tabla "+tableName)

                                      
    try:
        print("Obj")
        obj = s3.Object(bucket, key).get()['Body']
    except:
        print("El objeto S3 no pudo ser abierto. Revisa que exista el objeto o la variable de ambiente")
    try:
        table = dynamodb.Table(tableName)
    except:
        print("Error al abrir la tabla de Dynamo")
                                
    batch_size_per_page = 50
    table = []
    batch = []
    item_keys = {}
    items_count = 0
    rows_on_file = 0
                                
    for row in csv.DictReader(codecs.getreader('utf-8')(obj), dialect='pipe'):
        if len(batch) >= batch_size_per_page:
            write_to_dynamo(batch, item_keys)
            #time.sleep(2)
            batch.clear()
    
        if items_count == 0:
            for i in row:
                item_keys[i[1:-1]]=''
            items_count += 0
        batch.append(row)
        rows_on_file += 1
        print(rows_on_file)
        print(f'lenght batch {len(batch)}')
                                
    if batch:
        write_to_dynamo(batch, item_keys)
   
    print("Fin de ejecución de carga de listas de valmer")                             
    return {
        'statusCode': 200,
        'body': json.dumps('Tabla de DynamoDB lista!')
    }
                                
                                    
def write_to_dynamo(rows, item_keys_table):
    try:
        table = dynamodb.Table(tableName)
    except:
        print("Error al abrir la tabla de DynamoDb")                        
    try:  
        with table.batch_writer() as batch:
            value_clean = ''
            global counter
            for i in range(len(rows)):
                item_keys_aux = {}  
                counter += 1
                for item in item_keys_table:
                    if '"' in rows[i][f'"{item}"']:
                        value_clean = rows[i][f'"{item}"'][1:-1]
                    if '"' not in rows[i][f'"{item}"']:
                        value_clean = rows[i][f'"{item}"']
                    item_keys_aux['ID'] = str(counter)
                    item_keys_aux[item] = value_clean
                # table.append(item_keys_aux)
                batch.put_item(
                    Item=item_keys_aux
                )
    except Exception as e:
        print(e) 
        print("Error al escribir")