import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from forum_app import app

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url=app.config.get('DYNAMODB_ENDPOINT_URL'),
  aws_access_key_id=app.config.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=app.config.get('AWS_SECRET_ACCESS_KEY'),
  region_name=app.config.get('DYNAMODB_REGION')
  )
counter_table=dynamodb.Table("Counter")

def get_next_id(table_name):
  response=counter_table.get_item(
    Key={
      'table_name':table_name
    }
  )
  next_id=response['Item']['next_id']

  return next_id

def get_next_id_and_increment(table_name):
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