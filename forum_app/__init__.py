
from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)
app.config.from_object('forum_app.config')

@app.route('/')
def main():
  #appフォルダ/templatesから自動読み込み
  return render_template('index.html')

@app.route('/<int:thread_id>', methods=['GET','POST'])
def thread(thread_id):
  if request.method=='GET':
    #TODO:スレッド表示機能を作成

    #ダミーのスレッド内容
    responses=[{
    'name':'tarou',
    'item':'こんにちは'
    },
    {'name':'jirou',
    'item':'こんばんは'
    },
    ]
    return 'スレッド番号{}'.format(thread_id)
  elif request.method=='POST':
    #TODO:スレッドへの投稿機能を作成
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

if (__name__=='__main__'):
  app.run()