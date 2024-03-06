from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
  