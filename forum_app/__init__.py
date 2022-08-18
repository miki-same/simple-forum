
from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)

config={
  'default':'forum_app.config.DevelopmentConfig'
}
config_name='default'
app.config.from_object(config[config_name])

from forum_app.views import entries


if (__name__=='__main__'):
  app.run()