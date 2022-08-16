
from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)
app.config.from_object('forum_app.config')

from forum_app.views import entries


if (__name__=='__main__'):
  app.run()