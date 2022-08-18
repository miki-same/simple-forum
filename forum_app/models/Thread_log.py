import boto3
from decimal import Decimal

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url='http://localhost:8000',
  aws_access_key_id='',
  aws_secret_access_key='',
  region_name='')

thread_log_table=dynamodb.Table("Thread_log")

def get_thread(id):
  response=thread_log_table.get_item(
    Key={
      'id':id
    }
  )
  return response.get('Item')

def put_thread(item):
  item['created_at']=Decimal(item['created_at'])
  thread_log_table.put_item(Item=item)
  return

def delete_thread(id):
  thread_log_table.delete_item(
    Key={
      'id':id
    }
  )

def get_all_threads():
  response=thread_log_table.scan()

  return response.get('Items')