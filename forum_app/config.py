import os

class DevelopmentConfig(object):
  DEBUG = True
  SECRET_KEY='secret_key'
  AWS_ACCESS_KEY='AWS_ACCESS_KEY'
  AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY'
  DYNAMODB_ENDPOINT_URL='http://localhost:8000'
  DYNAMODB_REGION=''
  MAX_THREAD_SIZE=20
  DB_THREAD="Thread"
  DB_THREAD_LOG="Thread_log"
  DB_POST="Post"
  DB_COUNTER="Counter"

class ProductionConfig(object):
  DEBUG = False
  SECRET_KEY=os.environ.get('SIMPLE_FORUM_SECRET_KEY')
  AWS_ACCESS_KEY=os.environ.get('SIMPLE_FORUM_AWS_ACCESS_KEY')
  AWS_SECRET_ACCESS_KEY=os.environ.get('SIMPLE_FORUM_AWS_SECRET_ACCESS_KEY')
  DYNAMODB_ENDPOINT_URL='None'
  DYNAMODB_REGION='ap-northeast-1'
  MAX_THREAD_SIZE=100
  DB_THREAD="SimpleForumThread"
  DB_THREAD_LOG="SimpleForumThreadLog"
  DB_POST="SimpleForumPost"
  DB_COUNTER="SimpleForumCounter"