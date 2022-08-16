import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url='http://localhost:8000',
  aws_access_key_id='',
  aws_secret_access_key='',
  region_name='')

post_table=dynamodb.Table("Post")
thread_table=dynamodb.Table("Thread")
#1つの投稿の取得
def get_post(thread_id,posted_at):
  response=post_table.get_item(
    Key={
      'thread_id':thread_id,
      'posted_at':posted_at
    }
  )
  return response['Item']

def put_post(item):
  item['posted_at']=Decimal(item['posted_at'])
  post_table.put_item(Item=item)
  thread_table.update_item(
    Key={
      'id':item['thread_id'],
    },
    UpdateExpression="add number_of_posts :a",
    ExpressionAttributeValues ={
      ":a": 1
    }
  )
  return

#スレッドに属する全投稿の取得
def get_all_posts_in_thread(thread_id):
  response=post_table.query(KeyConditionExpression=Key('thread_id').eq(thread_id))
  return response['Items']