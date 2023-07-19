from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):
        return redirect(url_for('mypage'))
    else :
        error = 'ユーザ名またはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/mypage', methods=['GET'])
def mypage():
    return render_template('mypage.html')

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
    
    #一覧
@app.route('/booklist')
def Boo_list():
    return render_template('Book_list.html')

@app.route('/hamed')
def home_back():
    return render_template('index.html')

    #Book登録
@app.route('/regi_book')
def register_book():
    return render_template('register_Book.html')

@app.route('/news_Book', methods=['POST'])
def new_Book():
    title = request.form.get('title')
    author = request.form.get('author')
    pages = request.form.get('pages')
    
    db.insert_book(title, author, pages)
    
    book_list = db.select_all_book()
    return render_template('success_Book.html', book=book_list)

if __name__ == '__main__':
    app.run(debug=True)
