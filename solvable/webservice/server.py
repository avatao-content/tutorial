from flask import Flask, render_template, request, redirect, url_for, make_response, session, send_from_directory
from pathlib import Path
import uuid
import os
import json
from os.path import join
from comment_handler import add_new_comment, get_all_comments
from user_handler import check_login_credentials, add_new_user, set_nickname, get_nickname
from functools import wraps

app = Flask(__name__)

MY_URL = None
MY_PORT = 8888

def is_redirect(response):
    return response.status_code in range(300, 400)

def get_my_url():
    global MY_URL
    try:
        for key, value in json.loads(os.environ['AVATAO_PROXY_SERVICES'].replace("'",'"')).items():
            if value == str(MY_PORT) + '/tcp':
                uuid = key
        host = '.'.join(request.headers.get('X-Forwarded-Host', '.').split('.')[1:])
        MY_URL = 'https://' + uuid + '.' + host
    except Exception:
        MY_URL = 'http://localhost:' + str(MY_PORT)
    MY_URL += '/webservice'
    return MY_URL

@app.after_request
def after_request(response):
    if is_redirect(response):
        response.location = get_my_url() + response.location
    return response


UPLOAD_FOLDER = '/home/user/webservice/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = str(uuid.uuid1().hex)

SEARCH_HISTORY = '/home/user/webservice/search-history.txt'

def append_to_search_results(name, movie):
    filename = Path(SEARCH_HISTORY)
    filename.touch(exist_ok=True)
    with open(SEARCH_HISTORY, 'a') as file:
        file.write(name +'--->'+ movie + '\n')

def test_append_to_search_results(movie):
    filename = Path(SEARCH_HISTORY)
    filename.touch(exist_ok=True)
    with open(SEARCH_HISTORY, 'a') as file:
        file.write('test' + '--->'+ movie + '\n')

def get_search_history():
    filename = Path(SEARCH_HISTORY)
    filename.touch(exist_ok=True)
    with open(SEARCH_HISTORY, 'r') as file:
        searches = [line.split('--->') for line in file.readlines()]
    return reversed(searches)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login', alert = "You need to be logged in first!" ))
    return wrap

def get_comments():
    comments = get_all_comments()
    return comments

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == "POST":
        new_nickname = request.form['nickname']
        set_nickname(session['username'], new_nickname)
        session.pop('nickname', None)
        session['nickname'] = new_nickname
        msg = "Success! Nickname changed."
        return render_template('settings.html', nickname = new_nickname, message = msg)
    return render_template('settings.html', nickname = session['nickname'], message = None)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username = session['username'], nickname = session['nickname'])

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        result = []
        movie_name = request.form['moviename']
        username = session['username']
        append_to_search_results(username, movie_name)
        with open('/home/user/webservice/movies.txt', 'r') as movies:
            content = movies.readlines()
        for row in content:
            if movie_name.lower() in row.lower():
                result.append(row)
        if len(result) > 0:
            formatted_results = []
            for line in result:
                formatted_results.append([ line[0:4], line[4:] ])
            return render_template('search.html', results = formatted_results, no_result = False)
        results = [ "No result found for " + movie_name ]
        return render_template('search.html', results = results, no_result = True)
    return render_template('search.html')

@app.route('/search-history')
def search_history():
    data = get_search_history()
    if not data:
        data = ["The search history is empty."]
        return render_template('search_results.html', history=data, empty=True)
    temp = []
    for row in data:
        temp.append( (row[0], row[1]))
    return render_template('search_results.html', history=temp, empty=False)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('nickname', None)
    session.clear()
    return redirect(url_for('index'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if check_login_credentials(username, password):
            session['logged_in'] = True
            session['username'] = username
            session['nickname'] = get_nickname(username)
            return redirect(url_for('index'))
        return render_template('login.html', alert = "Wrong user credentials!")
    alert = request.args.get('alert')
    return render_template('login.html', alert = alert)

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['passwordconfirm']
        if password == password_confirm:
            success = add_new_user(username, password)
            if success:
                payload = {'username': username, 'password': password}
                return redirect(url_for('login', data = payload), code = 307)
            return render_template('register.html', alert="User already exists!")
        return render_template('register.html', alert="Passwords doesn't mach!")
    return render_template('register.html')

@app.route('/add_comment', methods=["POST"])
def add_comment():
    to_insert=[request.form['name'], request.form['comment']]
    if 'file' not in request.files:
        to_insert.append(None)
        session['messages'] = "nope"
    else:
        file = request.files['file']
        if file.filename == "":
            session['messages'] = "nope"
            to_insert.append(None)
        elif file and 'image' in file.content_type:
            to_insert.append(file.filename)
            try:
                file.save(join(UPLOAD_FOLDER, file.filename))
                session['messages'] = "SUCCESS"
            except Exception as e:
                session['messages'] = "Error: " + str(e)
        else:
            to_insert.append(None)
            session['messages'] = "Error: file extension not allowed! Please try again with an image."
    add_new_comment(to_insert)
    return redirect(url_for('guestbook'))

@app.route('/guestbook')
def guestbook():
    try:
        msg=session['messages']
    except:
        msg="nope"
    r = make_response(render_template('guestbook.html', comments = get_comments(), msg = msg))
    return r

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

@app.route('/uploads/<string:filename>')
def uploads(filename):
    response = make_response( send_from_directory(app.config['UPLOAD_FOLDER'], filename) )
    response.headers.set('Content-Security-Policy', "default-src 'none';")
    response.headers.set('X-Content-Type-Options', 'nosniff')
    return response

@app.route('/show-upload/<string:filename>')
def show_upload(filename):
    filepath = "/webservice/uploads/" + filename
    return render_template("file.html", file=filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11111, debug=True)
