from flask import Flask, request, redirect, url_for, render_template, flash
from forum_app import app
from forum_app.models import Counter

import random

@app.route('/random', methods=['GET'])
def random_page():
  number_of_threads=Counter.get_next_id('Thread')
  rand=random.randrange(number_of_threads)
  return redirect('/{}'.format(rand))