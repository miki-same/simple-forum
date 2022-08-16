import boto3

dynamodb=boto3.resource(
  'dynamodb',
  endpoint_url='http://localhost:8000',
  aws_access_key_id='',
  aws_secret_access_key='',
  region_name='')

thread_table=dynamodb.Table("Thread")

def get_item(id):
  response=thread_table.get_item(
    Key={
      'id':id
    }
  )
  return response['Item']

def post_item(item):
  thread_table.put_item(item)
  return 


def get_all_threads():
  response=thread_table.scan()

  return response['Items']