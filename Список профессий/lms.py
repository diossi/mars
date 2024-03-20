from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
list_prof = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='mars one')


@app.route('/training/engineers')
def training_engineers():
    return render_template('training.html', title='mars one', prof='engineers')


@app.route('/training/scientists')
def training_scientists():
    return render_template('training.html', title='mars one', prof='scientists')


@app.route('/list_prof/<list>')
def list_prof_def(list):
    return render_template('list_prof.html', list=list, list_prof=list_prof)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
  