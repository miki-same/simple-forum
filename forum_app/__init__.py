
from flask import Flask, request, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect

#CSRF対策
csrf=CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

config={
  'default':'forum_app.config.DevelopmentConfig'
}
config_name='default'
app.config.from_object(config[config_name])

#from forum_app.views import entries
from forum_app.views import index
from forum_app.views import thread
from forum_app.views import random
from forum_app.views import jump

if (__name__=='__main__'):
  app.run()