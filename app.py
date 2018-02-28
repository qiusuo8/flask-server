#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash, get_flashed_messages
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'
LOCOLIZABLE_FOLDER = 'localizable_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'png', 'jpeg', 'gif', 'xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

base_dir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
	return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/error/<message>')
def show_error(message):
    return 'Error: %s' % message

@app.route('/success/<message>')
def show_success(message):
    return 'Success: %s' % message

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('show_error', message='No file part'))
		file = request.files['file']
		if file.filename == '':
			print('No selected file')
			directory = os.getcwd()
			return redirect(url_for('show_error', message='No selected file'))
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print('origin file name: %s secure file name: %s' % (file.filename, filename) )
			time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
			save_name = time_str + '_' + filename
			file_path = create_dir_if_need(base_dir, save_name, app.config['UPLOAD_FOLDER'], filename)
			print('file_path: %s' % file_path)
			file.save(file_path)
			return redirect(url_for('show_success', message='Upload successfully!'))

	return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<midpath>/<filename>')
def download_file(filename, midpath):
	upload_dir = os.path.join(base_dir, app.config['UPLOAD_FOLDER'])
	file_dir = os.path.join(upload_dir, midpath)
	print('file_dir: %s' % file_dir)
	return send_from_directory(file_dir, filename, as_attachment=True)

def create_dir_if_need(base, file, *dirs):
	retDir = base
	for d in dirs:
		retDir = os.path.join(retDir, d)
		if not os.path.exists(retDir):
			os.makedirs(retDir)
	if file != '':
		retDir = os.path.join(retDir, file)
	return retDir