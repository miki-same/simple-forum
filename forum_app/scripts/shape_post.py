from flask import url_for
from forum_app.models import Thread

import time
import re
from decimal import Decimal

#入力された内容とスレッドIDからDBに投げるデータを作成
def shape_post(thread_id, user_name, message, post_id):
  if not user_name:
    user_name='名無しさん' 
  
  #正規表現でURLをハイパーリンクに置き換える
  #直接リンクではなくジャンプページ(別タブ)へのリンクにする
  #TODO:HTMLインジェクション対策
  t=r'(https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)\'\[\]]+)'
  message=re.sub(t,r'<a href="'+url_for('jump_page')+r'?url=\1 " target="_blank" rel="noopener noreferrer">\1</a>',message)

  item={
    "thread_id":thread_id,
    "post_id":post_id,
    "posted_at":Decimal(time.time()),
    "user_name":user_name,
    "message":message
  }

  return item