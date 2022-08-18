from concurrent.futures import thread
from flask import Flask, request, redirect, url_for, render_template, flash
from forum_app import app
from decimal import Decimal

from forum_app.models import Thread, Thread_log
from forum_app.models import Post
from forum_app.models import Counter

from forum_app.scripts import shape_post
from forum_app.scripts import move_thread

import time
import datetime
import random
import re

@app.route('/')
def main():
  threads=Thread.get_all_threads()
  params=request.args
  sort_param=int(params.get("sort")) if params.get("sort")!=None else None
  if sort_param==1 or sort_param==None:
    threads.sort(key=lambda x:x['created_at'],reverse=True)
  elif sort_param==2:
    threads.sort(key=lambda x:x['number_of_posts'],reverse=True)
  #appフォルダ/templatesから自動読み込み

  return render_template('index.html',threads=threads)

@app.route('/new', methods=['GET', 'POST'])
def create_new_thread():
  if request.method=='GET':
    return render_template('new.html')

  elif request.method=='POST':
    #スレッドを作成
    id=Counter.get_next_id_and_increment('Thread')
    title=request.form['title']
    created_at=time.time()

    user_name=request.form['user_name']
    message=request.form['message']

    #タイトル・本文が未入力の場合新規作成ページにリダイレクトされるようにする
    errflg=False
    if not title:
      flash('タイトルを入力してください')
      errflg=True
    if not message:
      flash('本文を入力してください')
      errflg=True
    
    if errflg:
      return redirect(url_for('create_new_thread'))

    item_thread={
      'id':id,
      'title':title,
      'created_at':created_at,
      'number_of_posts':0
    }
    Thread.put_thread(item_thread)

    #最初の投稿を作成
    item_post=shape_post.shape_post(thread_id=id, user_name=user_name,message=message,post_id=1)

    Post.put_post(item_post)

  flash('スレッドが作成されました')
  return redirect('/{}'.format(id))

@app.route('/<int:thread_id>', methods=['GET','POST'])
def show_thread(thread_id):
  if request.method=='GET':
    #スレッドを取得
    thread_response=Thread.get_thread(thread_id)
    can_post=True

    #現行スレにないとき過去ログを探す
    if thread_response==None:
      thread_response=Thread_log.get_thread(thread_id)
      #過去ログにある時Falseになるフラッグ
      can_post=False

    if thread_response==None:
      flash('存在しないスレッドです')
      return redirect(url_for('main'))

    #スレッド内の投稿を取得
    thread_posts=Post.get_all_posts_in_thread(thread_id)
    title=thread_response['title']
    number_of_posts=int(thread_response['number_of_posts'])
    created_at=float(thread_response['created_at'])
    created_at_jst=datetime.datetime.fromtimestamp(created_at, datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

    for post in thread_posts:
      post['thread_id']=int(post['thread_id'])
      post['posted_at']=float(post['posted_at'])
      post['posted_at_jst']=datetime.datetime.fromtimestamp(post['posted_at'],datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
    return render_template('thread.html',thread_id=thread_id,title=title,number_of_posts=number_of_posts,created_at=created_at_jst, thread_posts=thread_posts, can_post=can_post)

  elif request.method=='POST':
    thread_response=Thread.get_thread(thread_id)

    #現行スレではなくなっている場合、または現行スレで投稿上限に達している場合
    if thread_response==None or (thread_response and thread_response['number_of_posts']>=app.config.get('MAX_THREAD_SIZE')):
      flash('投稿上限に到達しました')
      if thread_response!=None:
        move_thread.move_thread(thread_id=thread_id)

      return redirect(url_for('show_thread',thread_id=thread_id))

    post_id=thread_response['number_of_posts']+1

    user_name=request.form['name']
    message=request.form['message']

    if not message:
      flash('本文を入力してください')
      return redirect(url_for('show_thread',thread_id=thread_id))

    item=shape_post.shape_post(thread_id=thread_id,user_name=user_name,message=message,post_id=post_id)

    Post.put_post(item)
    flash('投稿が完了しました')

    #過去ログに移動
    if post_id>=app.config.get('MAX_THREAD_SIZE'):
      move_thread.move_thread(thread_id=thread_id)

    return redirect('/{}'.format(thread_id))

@app.route('/<int:thread_id>/delete', methods=['POST'])
def delete_thread(thread_id):
  #TODO:スレッドの削除機能を実装
  return redirect('/')

@app.route('/<int:thread_id>/<int:post_id>', methods=['GET'])
def show_post(thread_id,post_id):
  post_response=Post.get_post(thread_id,post_id)
  thread_response=Thread.get_thread(thread_id)
  can_post=True

  #過去ログの場合
  if thread_response==None:
    thread_response=Thread_log.get_thread(thread_id)
    can_post=False

  if post_response!=None:
    post=post_response
    title=thread_response['title']
    number_of_posts=int(thread_response['number_of_posts'])
    
    created_at=float(thread_response['created_at'])
    created_at_jst=datetime.datetime.fromtimestamp(created_at, datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

    post['thread_id']=int(post['thread_id'])
    post['posted_at']=float(post['posted_at'])
    post['posted_at_jst']=datetime.datetime.fromtimestamp(post['posted_at'],datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('thread.html',thread_id=thread_id,title=title,number_of_posts=number_of_posts,created_at=created_at_jst, thread_posts=[post], can_post=can_post)
  
  else:
    flash('存在しないレス番号です')
    return redirect(url_for('show_thread',thread_id=thread_id))


@app.route('/<int:thread_id>/<int:item_id>/delete', methods=['POST'])
def delete_item(thread_id,item_id):
  #TODO:レスの削除機能を実装 
  return redirect('/')

@app.route('/random', methods=['GET'])
def random_page():
  number_of_threads=Counter.get_next_id('Thread')
  rand=random.randrange(number_of_threads)
  return redirect('/{}'.format(rand))

@app.route('/jump', methods=['GET'])
def jump_page():
  if request.args.get('url')==None:
    flash('無効なURLです。')
    return redirect('/')
  print(request.args.get('url'))
  return render_template('jump.html',url=request.args.get('url'))

'''
@app.errorhandler(404)
def not_found(error):
  return '404 not found'
'''