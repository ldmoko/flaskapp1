from flask import Flask, request, render_template, url_for, redirect
from flask import make_response, abort, session
# from models import User
# from models.book import Book
from flask_mail import Mail, Message


app = Flask(__name__)
app.debug = True
app.secret_key = 'aaaaaaaaaaaaaaaaa'
# app.config.update({
#     'SECRET_KEY': 'AAAAAAAAAAAAAA',
#     })

@app.route('/')
def hello_world():
    content = '你好！'
    return render_template('main.html', content=content)


# @app.route('/user/')
# def user():
#     user = User(1, 'ldm')
#     return render_template('test.html', user=user)


@app.route('/user/<username>', methods=['GET','PUT'])  # 默认是GET模式
def hello_user(username):
    if username == 'fuck':
        abort(404)
    return '<h1>hello:{}</h1>'.format(username)


# @app.route('/lidm/')  # 在后面加斜杠, 如果网址后面没有也可访问; 如果不在后面加斜杠, 网址后面加斜杠就访问不了 english
# def hello():
#     return 'hello, ldm'


# @app.route('/query_user/<user_id>')
# def query_user(user_id):
#     user = None
#     if int(user_id) == 1:
#         user = User(1, '敏哥！')
#     return render_template('user_id.html', user=user)


# @app.route('/users/')
# def user_list():
#     users = []
#     for i in range(1, 11):
#         user = User(i, '敏哥' + str(i))
#         users.append(user)
#     return render_template('user_list.html', users=users)


@app.route('/one/')
def one_base():
    return render_template('one_base.html')


@app.route('/two/')
def two_base():
    return render_template('two_base.html')
    # return redirect('/one/', code=301) #不写默认是302
    # return redirect(url_for('one_base'))  # 根据终节点找到对应的网址


@app.route('/rq/')
def test_rq():
    data = {}
    data['ip'] = request.remote_addr
    data['environ'] = request.environ
    data['url'] = request.url
    data['name'] = request.args.get('name')
    # return f'你当前的IP地址为：{data["ip"]}'
    return render_template('test_rq.html', data=data)


# @app.route('/resp/')
# def resp():
#     # 创建一个响应对象response
#     resp = make_response()
#     resp.response = render_template('main.html')
#     resp.code = 404
#     resp.headers['content-type'] = 'text/html'  # 'application/json'
#     return resp


# @app.route('/books/')
# def book_list():
#     book1 = Book('Python Flask', 59.00, 'Tom', '人民邮电出版社')
#     books = [
#         Book('Python Flask', 59.00, 'Tom', '人民邮电出版社'),
#         Book('Python Scrapy', 49.00, 'Tom', '人民邮电出版社'),
#         Book('Python 爬虫', 39.00, 'Tom', '人民邮电出版社'),
#         Book('Python Django', 99.00, 'Tom', '人民邮电出版社'),
#         Book('Python Selenium', 59.00, 'Tom', '人民邮电出版社')
#     ]
#     return render_template('book-list.html', book1=book1, books=books)


# @app.route('/help')
# def rq_help():
#     abort(404)


# 推荐
# @app.errorhandler(404)
# def not_found(e):
#     return render_template('404.html'), 404  
# 此处404如果不写，虽然效果也能看到，但是状态码是200
# 对于反爬虫，可以使用这招，返回200,但是界面是404


@app.route('/ip/<num_id>')
def ip(num_id):
    ip = request.remote_addr
    return render_template('ip.html', ip=ip, num_id=num_id)

@app.route('/ua/')
def ua():
    ua = dict(request.headers)
    if not ua['User-Agent'].startswith('Mozilla') or ua['User-Agent'].startswith('Opera'):
        return '非法请求'
    else:
        return '你的浏览器是：' + str(ua['User-Agent'])



@app.route('/reg/')
def reg():
    return render_template('reg.html')


@app.route('/doreg/', methods=['GET', 'POST'])
def doreg():
    name = request.form['username']
    pwd = request.form['pwd']
    age = request.form.get('age', '没输年龄')
    return '你的用户名是：{}, 你的密码是：{},你的年龄是：{}'.format(name, pwd, age)

@app.route('/testua/')
def testua():
    res = dict(request.headers)
    if res.get('anhao'):
        return 'OK'
    else:
        return '失败'


@app.route('/headers/')
def headers():
    data = dict(request.headers)
    return str(data['User-Agent'])  # 字典不会被调用，所以要转成字符
    # import json
    # return json.dumps(data) #此方法也是转成字符

# @app.route('/url')
# def url():
#     with app.test_request_context():
#         print(url_for('/url'))


# SMTP服务器配置
app.config.update(
    MAIL_SERVER='smtp.163.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='ldmoko@163.com',
    MAIL_PASSWORD='LDMOKO'
)


@app.route('/mail/')
def mail():
    mail = Mail(app)

    msg = Message(subject='来自flask的邮件', sender='ldmoko@163.com',
                  recipients=['ldmoko@163.com'])
    # msg.body = '文本 body'
    msg.html = '<b>HTML</b> body'
    # msg.html = render_template('mail.html')
    mail.send(msg)
    return '<h1>邮件发送成功</h1>'


@app.route('/setck/')
def set_mycookie():
    resp = make_response()
    resp.set_cookie('username', 'abc')
    return resp

@app.route('/getck/')
def get_mycookie():
    ck = request.cookies.get('username')
    if ck == 'abc':
        return '成功'
    else:
        return '失败'

@app.route('/remck/')
def remove_cookie():
    resp = make_response()
    resp.set_cookie('username', '', expires=0)
    return resp


@app.route('/login/')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    # 0.0.0.0表示外部也可访问, 否则只能通过localhost访问
    print(app.config)#.get('SECRET_KEY'))
    app.run(host='0.0.0.0', port=80, debug=True)
    # app.run(port=80)

