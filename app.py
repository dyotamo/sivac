from flask import Flask, render_template, redirect, flash, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import SearchForm, LoginForm, UploadForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "make-this-key-powerfull"

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"

login_manager = LoginManager(app)


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    owner = db.Column(db.String(120), unique=False, nullable=False)
    issue_date = db.Column(db.DateTime(), unique=False, nullable=False)
    institution = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<Certificate %d>" % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return "<Institution %d>" % self.institution


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        code = form.code.data
        issue_date = form.issue_date.data
        institution = form.institution.data

        certificate = Certificate.query.filter_by(
            code=code, issue_date=issue_date, institution=institution).first()

        if certificate is None:
            flash("Invalid certificate.", "danger")
        else:
            flash("Valid certificate.", "success")
        return redirect(url_for("index"))
    return render_template("index.html", form=form)


@app.route("/portal", methods=["GET", "POST"])
@login_required
def portal():
    form = UploadForm()

    if form.validate_on_submit():
        from seed import import_csv

        print(dir(form.csv.data))
        item_count = import_csv(form.csv.data)
        flash("{} lines sucessfully loaded".format(item_count), "success")
        return redirect(url_for('index'))

    certificates = Certificate.query.filter_by(
        institution=current_user.institution)
    return render_template("portal.html", certificates=certificates, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        institution = form.institution.data
        password = form.password.data

        user = User.query.filter_by(
            institution=institution, password=password).first()

        if user is None:
            flash("Invalid credentials.", "danger")
        else:
            flash("Successful logged in as {}.".format(
                user.institution), "success")
            login_user(user)
        return redirect(url_for("portal"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Successful logged out.", "success")
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify("404 Not Found.")


if __name__ == "__main__":
    app.run(debug=True)
