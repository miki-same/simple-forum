import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url='http://localhost:8000',
  aws_access_key_id='',
  aws_secret_access_key='',
  region_name='')

counter_table=dynamodb.Table("Counter")

def get_next_id(table_name):
  response=counter_table.get_item(
    Key={
      'table_name':table_name
    }
  )
  next_id=response['Item']['next_id']
  counter_table.update_item(
    Key={
      'table_name':table_name,
    },
    UpdateExpression="add next_id :a",
    ExpressionAttributeValues ={
      ":a": 1
    }
  )

  return next_id