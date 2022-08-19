from flask import Flask, request, redirect, url_for, render_template, flash, make_response
from forum_app import app
from decimal import Decimal

from forum_app.models import Thread, Thread_log
from forum_app.models import Post
from forum_app.models import Counter

from forum_app.scripts import shape_post
from forum_app.scripts import move_thread
from forum_app.scripts import random_id
from forum_app.scripts import next_day

import time
import datetime
import random
import re
import json

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

    response=make_response(redirect('/{}'.format(thread_id)))

    #CookieからIDを読み込み
    user_info=request.cookies.get('user_info')
    if user_info != None:
      user_info = json.loads(user_info)
    else:
      #Cookieに情報がない場合の設定
      user_info = {'id':random_id.random_id()}
      expires = next_day.next_day()
      response.set_cookie("user_info", value=json.dumps(user_info), expires=expires)

    if not message:
      flash('本文を入力してください')
      return redirect(url_for('show_thread',thread_id=thread_id))

    item={
      'thread_id':thread_id,
      'user_name':user_name,
      'message':message,
      'post_id':post_id,
      'user_id':user_info['id']
    }
    item=shape_post.shape_post(item)
    #item=shape_post.shape_post(thread_id=thread_id,user_name=user_name,message=message,post_id=post_id, user_id=user_info['id'])

    Post.put_post(item)
    flash('投稿が完了しました')    

    #過去ログに移動
    if post_id>=app.config.get('MAX_THREAD_SIZE'):
      move_thread.move_thread(thread_id=thread_id)
    print(user_info)
    return response

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