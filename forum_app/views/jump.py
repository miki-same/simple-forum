from flask import Flask, request, redirect, url_for, render_template, flash
from forum_app import app

@app.route('/jump', methods=['GET'])
def jump_page():
  if request.args.get('url')==None:
    flash('無効なURLです。')
    return redirect('/')
  print(request.args.get('url'))
  return render_template('jump.html',url=request.args.get('url'))