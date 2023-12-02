from flask import Flask, render_template, redirect, jsonify, request, url_for, flash, send_from_directory, send_file
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import secrets
import subprocess

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///rclone_helper.db"
app.config["SECRET_KEY"] = secrets.token_hex()
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

class Comandi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(128), nullable=False)
    origine = db.Column(db.String(128), nullable=False)
    destinazione = db.Column(db.String(128), nullable=False)
    descrizione = db.Column(db.String(128), nullable=True)

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    comandi = db.Column(db.JSON, nullable=False)
    note = db.Column(db.String(128), nullable=True)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/comandi")
@login_required
def comandi():
    return render_template("comandi.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if len(User.query.all()) == 0:
        return render_template("welcome.html")
    if request.method == "POST":
        utente = User.query.filter_by(username=request.form["username"]).first()
        if utente:
            if check_password_hash(utente.password, request.form["passwd"]):
                login_user(utente)
                return redirect(url_for("index"))
            else:
                flash("Username o Password errati!", "warning")
        else:
            flash("Utente inesistente!", "warning")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        if request.form["id_form"] == "nuovo_utente":
            utente = User.query.filter_by(username=request.form["username"]).first()
            if utente is None:
                password = generate_password_hash(request.form["passwd"])
                utente = User(username=request.form["username"], password=password)
                db.session.add(utente)
                db.session.commit()
                flash("Utente inserito con successo!", "success")
            else:
                flash("Esiste già l'utente "+request.form["username!"], "warning")
    return render_template("admin.html", utenti=User.query.all())

@app.route("/welcome", methods=["POST"])
def welcome():
    if len(User.query.all()) > 0:
        return redirect(url_for("login"))
    if request.form["passwd"] == request.form["conferma_passwd"]:
        password = generate_password_hash(request.form["passwd"])
        utente = User(username=request.form["username"], password=password)
        db.session.add(utente)
        db.session.commit()
        flash("Utente creato con successo!", "success")
    else:
        flash("Le password non coincidono!", "warning")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
