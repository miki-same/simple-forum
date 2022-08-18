from flask import Flask, request, redirect, url_for, render_template, flash
from forum_app import app
from decimal import Decimal

from forum_app.models import Thread
from forum_app.models import Post
from forum_app.models import Counter
from forum_app.models import Thread_log

import time
import datetime
import random
import re

#スレッドを過去ログに移動
def move_thread(thread_id):
  thread_response=Thread.get_thread(thread_id)
  if thread_response==None:
    return False

  Thread.delete_thread(thread_id)
  Thread_log.put_thread(item=thread_response)

  return