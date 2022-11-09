from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config
from app.models.ModelUser import ModelUser
from app.models.entities.User import User

app=Flask(__name__)

db= MySQL(app)
login_manager_app= LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# redirige login
@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return  redirect(url_for("admin"))
            else:
                flash("Invalid Password")
                return render_template('login.html')
        else:
            flash("User not found ...")
        return render_template('login.html')
    else:
        return render_template('login.html')
    #Dentro de las comillas ruta del login o lo que se vaya usara de front
    
@app.route('/index')
def cancel():
    return render_template("home.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    return render_template("administrator.html")

def status401(error):
    return redirect(url_for('login'))

def status404(error):
    return '<h1> Página no encontrada</h1>', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status401)
    app.register_error_handler(404, status404)
    app.run()