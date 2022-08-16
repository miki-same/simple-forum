from tokenize import Number
from flask import Flask, request, redirect, url_for, render_template
from forum_app import app

from forum_app.models import Thread
from forum_app.models import Post

@app.route('/')
def main():
  #ダミーのスレッド情報
  threads=[
    {
      'name':'Flask総合スレ',
      'number_of_responses':150,
      'thread_id':1
    },
    {
      'name':'Webアプリ相談スレ',
      'number_of_responses':70,
      'thread_id':2
    },
  ]
  #appフォルダ/templatesから自動読み込み
  return render_template('index.html',threads=threads)

@app.route('/<int:thread_id>', methods=['GET','POST'])
def show_thread(thread_id):
  if request.method=='GET':
    #TODO:スレッド表示機能を作成

    thread_response=Thread.get_item(thread_id)
    thread_posts=Post.get_all_posts_in_thread(thread_id)
    ThreadName=thread_response['ThreadName']
    NumberOfPosts=int(thread_response['NumberOfPosts'])
    CreatedAt=int(thread_response['CreatedAt'])
    ThreadId=thread_id
    for post in thread_posts:
      post['ThreadId']=int(post['ThreadId'])
      post['PostedAt']=int(post['PostedAt'])
    return render_template('thread.html',ThreadId=ThreadId,ThreadName=ThreadName,NumberOfPosts=NumberOfPosts,CreatedAt=CreatedAt, thread_posts=thread_posts)
    '''
    #ダミーのスレッド内容
    responses=[{
    'name':'tarou',
    'item':'こんにちは',
    },
    {'name':'jirou',
    'item':'こんばんは',
    },
    ]
    return 'スレッド番号{}'.format(thread_id)
    '''
  elif request.method=='POST':
    #TODO:スレッドへの投稿機能を作成
    print(request.form['message'])
    return redirect('/{}'.format(thread_id))

@app.route('/<int:thread_id>/delete', methods=['POST'])
def delete_thread(thread_id):
  #TODO:スレッドの削除機能を実装
  return redirect('/')

@app.route('/<int:thread_id>/<int:item_id>/delete', methods=['POST'])
def delete_item(thread_id,item_id):
  #TODO:レスの削除機能を実装 
  return redirect('/')


'''
@app.errorhandler(404)
def not_found(error):
  return '404 not found'
'''