from flask import Flask, request, redirect, url_for, render_template, flash
from forum_app import app
from decimal import Decimal

from forum_app.models import Thread
from forum_app.models import Post
from forum_app.models import Counter

import time
import datetime
import random

@app.route('/')
def main():
  threads=Thread.get_all_threads()
  #appフォルダ/templatesから自動読み込み
  return render_template('index.html',threads=threads)

@app.route('/new', methods=['GET', 'POST'])
def create_new_thread():
  if request.method=='GET':
    return render_template('new.html')
  elif request.method=='POST':
    title=request.form['title']
    created_at=time.time()
    user_name=request.form['user_name']
    message=request.form['message']
    id=Counter.get_next_id_and_increment('Thread')
    
    item_thread={
      'id':id,
      'title':title,
      'created_at':created_at,
      'number_of_posts':0
    }
    Thread.put_thread(item_thread)
    
    item_post={
      'thread_id':id,
      'posted_at':created_at,
      'user_name':user_name,
      'message':message
    }
    Post.put_post(item_post)

  return redirect('/{}'.format(id))

@app.route('/<int:thread_id>', methods=['GET','POST'])
def show_thread(thread_id):
  if request.method=='GET':
    #スレッドを取得
    thread_response=Thread.get_thread(thread_id)
    #スレッド内の投稿を取得
    thread_posts=Post.get_all_posts_in_thread(thread_id)
    title=thread_response['title']
    number_of_posts=int(thread_response['number_of_posts'])
    created_at=float(thread_response['created_at'])
    created_at_jst=datetime.datetime.fromtimestamp(created_at, datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
    for i, post in enumerate(thread_posts):
      post['post_number']=i+1
      post['thread_id']=int(post['thread_id'])
      post['posted_at']=float(post['posted_at'])
      post['posted_at_jst']=datetime.datetime.fromtimestamp(post['posted_at'],datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
    return render_template('thread.html',thread_id=thread_id,title=title,number_of_posts=number_of_posts,created_at=created_at_jst, thread_posts=thread_posts)

  elif request.method=='POST':
    #TODO:スレッドへの投稿機能を作成
    name=request.form['name']
    message=request.form['message']
    item={
      "thread_id":thread_id,
      "posted_at":time.time(),
      "user_name":name,
      "message":message
    }
    Post.put_post(item)
    flash('投稿が完了しました')
    return redirect('/{}'.format(thread_id))

@app.route('/<int:thread_id>/delete', methods=['POST'])
def delete_thread(thread_id):
  #TODO:スレッドの削除機能を実装
  return redirect('/')

@app.route('/<int:thread_id>/<int:item_id>/delete', methods=['POST'])
def delete_item(thread_id,item_id):
  #TODO:レスの削除機能を実装 
  return redirect('/')

@app.route('/random', methods=['GET'])
def random_page():
  number_of_threads=Counter.get_next_id('Thread')
  rand=random.randrange(number_of_threads)
  return redirect('/{}'.format(rand))


'''
@app.errorhandler(404)
def not_found(error):
  return '404 not found'
'''