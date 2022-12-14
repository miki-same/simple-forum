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

    response=make_response(redirect('/{}'.format(id)))

    #CookieからIDを読み込み
    user_info=request.cookies.get('user_info')
    if user_info != None:
      user_info = json.loads(user_info)
    else:
      #Cookieに情報がない場合の設定
      user_info = {'id':random_id.random_id()}
      expires = next_day.next_day()
      response.set_cookie("user_info", value=json.dumps(user_info), expires=expires)


    item={
      'thread_id':id,
      'user_name':user_name,
      'message':message,
      'post_id':1,
      'user_id':user_info['id']
    }
    item_post=shape_post.shape_post(item)

    #最初の投稿を作成
    #item_post=shape_post.shape_post(thread_id=id, user_name=user_name,message=message,post_id=1, user_id=user_info['id'])

    Post.put_post(item_post)

    flash('スレッドが作成されました')
    return response