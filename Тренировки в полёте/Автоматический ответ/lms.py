from flask import Flask, render_template, redirect
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
global_form = None


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
  