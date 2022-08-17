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
def get_post(thread_id,post_id):
  response=post_table.get_item(
    Key={
      'thread_id':thread_id,
      'post_id':post_id
    }
  )
  return response.get('Item')

def put_post(item):
  #floatをDecimalに変換
  item['posted_at']=Decimal(item['posted_at'])

  post_table.put_item(Item=item)

  #スレッドの投稿数を更新
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