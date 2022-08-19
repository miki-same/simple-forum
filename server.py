#起動用ファイル
from forum_app import app


if (__name__=='__main__'):
  #Docker内で稼働するときの設定
  #uwsgiを利用するときは設定不要
  #app.run(host='0.0.0.0')
  #ローカルで稼働するときの設定
  app.run()