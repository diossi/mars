from flask import Flask, redirect, render_template, request, abort, make_response, jsonify
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from forms.departments import DepartmentsForm
from data import db_session, jobs_api
from data.jobs import Jobs
from data.users import User
from data.departments import Departments
from flask_restful import Api, abort
import jobs_resources
import users_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.collaborators = form.collaborators.data
        jobs.work_size = form.work_size.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление новости', 
                           form=form, current_user=current_user)


@app.route('/departments_add',  methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = Departments()
        departments.title = form.title.data
        departments.chief = form.chief.data
        departments.members = form.members.data
        departments.email = form.email.data
        current_user.departments.append(departments)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('departments_add_edit.html', title='Добавление', 
                           form=form, current_user=current_user)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))
                                          ).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job 
            form.collaborators.data = jobs.collaborators
            form.work_size.data = jobs.work_size
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))
                                          ).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.collaborators = form.collaborators.data
            jobs.work_size = form.work_size.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/departments_add_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departments = db_sess.query(Departments).filter(Departments.id == id,
                                          ((Departments.user == current_user) | (current_user.id == 1))
                                          ).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief 
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments: Jobs | None = db_sess.query(Departments).filter(Departments.id == id,
                                          ((Departments.user == current_user) | (current_user.id == 1))
                                          ).first()
        if departments:
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('departments_add_edit.html',
                           title='Редактирование',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments).filter(Departments.id == id,
                                          ((Departments.user == current_user) | (current_user.id == 1))
                                      ).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs, title='Главная страница', current_user=current_user)


@app.route("/departments")
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments)
    return render_template("departments.html", departments=departments, title='Departments', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", current_user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", current_user=current_user)
        jobs = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        jobs.set_password(form.password.data)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs') 
    api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')
    api.add_resource(users_resources.UserListResource, '/api/v2/users') 
    api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')
    app.register_blueprint(jobs_api.blueprint)
    app.run()
