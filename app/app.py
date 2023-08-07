from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from config import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/project'

csrf = CSRFProtect()
db = SQLAlchemy(app, engine_options={'pool_pre_ping': True})
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from models.ModelUser import ModelUser
    return ModelUser.get_by_id(db, user_id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = ModelUser.get_by_username(db, username)
        if user is not None and user.check_password(password):
            login_user(user)
            flash("¡Inicio de sesión exitoso!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    data = {
        'title': 'Registro de usuario',
    }

    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']
        email = request.form['email']
        profile_picture = request.files['profile_picture'].read()

        if (username, fullname, password, email, profile_picture):
            return redirect('/')
        else:
            flash("Error al registrar usuario. Inténtelo nuevamente.")

    return render_template('register.html', data=data)


@app.route('/profile')
@login_required
def profile():
    user_data_dict = {
        'username': current_user.username,
        'email': current_user.email,
        'profile_picture': current_user.profile_picture
    }

    return render_template('profile.html', user_data=user_data_dict)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
