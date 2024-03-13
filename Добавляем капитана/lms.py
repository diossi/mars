from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import Flask, render_template
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.db")


db_sess = db_session.create_session()
user = User()

user.surname = "Scott"
user.name = "Ridley"
user.age = "22"
user.position = "captain"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "scott_chief@mars.org"

db_sess.add(user)

user.surname = "Scott2"
user.name = "Ridley2"
user.age = "22"
user.position = "captain"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "scott_chief2@mars.org"

db_sess.add(user)

user.surname = "Scott3"
user.name = "Ridley3"
user.age = "23"
user.position = "captain"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "scott_chief3@mars.org"

db_sess.add(user)

user.surname = "Scott4"
user.name = "Ridley4"
user.age = "24"
user.position = "captain"
user.speciality = "research engineer"
user.address = "module_1"
user.email = "scott_chief4@mars.org"

db_sess.add(user)
db_sess.commit()

user = db_sess.query(User).first()
print(user.name)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        jobs = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        jobs.set_password(form.password.data)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')