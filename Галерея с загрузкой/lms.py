from flask import Flask, render_template, redirect
from loginform import LoginForm, PhotoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
global_form = None
list_members = ['1', '2', 'asdasd', 'zxc', 'qwe']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='mars one')


@app.route('/training/<prof>')
def training_engineers(prof):
    return render_template('training.html', title='mars one', prof=prof)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global global_form

    form = LoginForm()
    if form.validate_on_submit():
        global_form = form
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='mars one', form=global_form)


@app.route('/distribution')
def distribution():
    return render_template('distribution.html', title='mars one', list_members=list_members)


@app.route('/table/<sex>/<age>')
def cabin_table(sex, age):
    return render_template('cabin_table.html', title='mars one', sex=sex, age=int(age))


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    form = PhotoForm()
    if form.validate_on_submit():
        return render_template('galery.html', title='Галерея', form=form, flag=True)
    return render_template('galery.html', title='Галерея', form=form, flag=False)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
  