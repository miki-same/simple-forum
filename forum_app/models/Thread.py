import boto3
from decimal import Decimal
from forum_app import app

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url=app.config.get('DYNAMODB_ENDPOINT_URL'),
  aws_access_key_id=app.config.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=app.config.get('AWS_SECRET_ACCESS_KEY'),
  region_name=app.config.get('DYNAMODB_REGION')
  )

thread_table=dynamodb.Table(app.config.get('DB_THREAD'))

#スレッドが存在する場合Itemを返す 存在しない場合Noneを返す
def get_thread(id):
  response=thread_table.get_item(
    Key={
      'id':id
    }
  )
  return response.get('Item')

def put_thread(item):
  item['created_at']=Decimal(item['created_at'])
  thread_table.put_item(Item=item)
  return

def delete_thread(id):
  thread_table.delete_item(
    Key={
      'id':id
    }
  )


def get_all_threads():
  response=thread_table.scan()

  return response.get('Items')