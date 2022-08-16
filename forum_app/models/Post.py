import boto3
from boto3.dynamodb.conditions import Key

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url='http://localhost:8000',
  aws_access_key_id='',
  aws_secret_access_key='',
  region_name='')

post_table=dynamodb.Table("Post")

#1つの投稿の取得
def get_post(ThreadId,PostedAt):
  response=post_table.get_item(
    Key={
      'ThreadId':ThreadId,
      'PostedAt':PostedAt
    }
  )
  return response['Item']

#スレッドに属する全投稿の取得
def get_all_posts_in_thread(ThreadId):
  response=post_table.query(KeyConditionExpression=Key('ThreadId').eq(ThreadId))
  return response['Items']