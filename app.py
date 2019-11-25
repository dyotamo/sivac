import os
import os.path
import tempfile

from datetime import datetime
from flask import Flask, render_template, redirect, flash, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import SearchForm, LoginForm, UploadForm, PasswordChangeForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "make-this-key-powerfull"

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL") or "sqlite:///dev.db"

login_manager = LoginManager(app)


class Certificate(db.Model):
    """ Certificate model """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    owner = db.Column(db.String(120), unique=False, nullable=False)
    issue_date = db.Column(db.DateTime(), unique=False, nullable=False)
    institution = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<Certificate %s>" % self.code


class User(db.Model, UserMixin):
    """ User model """
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return "<Institution %s>" % self.institution


@app.route("/", methods=["GET", "POST"])
def index():
    """ Presentes a certificate validation form and validates certificates """
    form = SearchForm()
    error = None
    if form.validate_on_submit():
        code = form.code.data
        issue_date = form.issue_date.data
        institution = form.institution.data

        certificate = Certificate.query.filter_by(code=code, issue_date=datetime(
            issue_date.year, issue_date.month, issue_date.day), institution=institution).first()

        if certificate is None:
            error = "Invalid certificate."
        else:
            flash("Certificate with code {} is valid, belongs to {}, issued on {}.".format(
                certificate.code, certificate.owner, certificate.issue_date.strftime('%d-%m-%Y')), "success")
            return redirect(url_for("index"))
    return render_template("index.html", form=form, error=error)


@app.route("/portal", methods=["GET", "POST"])
@login_required
def portal():
    """ Show all certificates that belongs to certain institution,
    and also makes possible to upload a .csv file containg new certificates """
    form = UploadForm()
    if form.validate_on_submit():
        from seed import import_csv

        # Here, we save the file in the /tmp directory and then retrieve it for reading
        path = _save_csv(form)
        f = open(path, "r")
        loaded_count, ignored_count = import_csv(f)
        f.close()

        flash("{} line(s) sucessfully loaded, {} line(s) ignored.".format(
            loaded_count, ignored_count), "success")

        return redirect(url_for("portal"))

    return render_template("portal.html", certificates=Certificate.query.filter_by
                           (institution=current_user.institution), form=form)


@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def remove(id):
    """ Remove a certificate """
    certificate = Certificate.query.filter_by(id=id).first_or_404()
    db.session.delete(certificate)
    db.session.commit()

    flash("{}'s certificated removed successfully.".format(
        certificate.owner), "success")
    return redirect(url_for("portal"))


def _save_csv(form):
    """ An utility function to save a file in the /tmp directory,
    returning its path for further processing """
    csv = form.csv.data
    path = os.path.join(tempfile.gettempdir(),
                        secure_filename(csv.filename))
    csv.save(path)
    return path


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login view """
    form = LoginForm()
    if form.validate_on_submit():
        institution = form.institution.data
        password = form.password.data

        user = User.query.filter_by(institution=institution).first()

        if user is None:
            flash("Invalid credentials.", "danger")
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Successful logged in as {}.".format(
                    user.institution), "success")
                return redirect(url_for("portal"))
            else:
                flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)


@app.route("/password", methods=["GET", "POST"])
def password():
    """ Change password view """
    error = None
    form = PasswordChangeForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if check_password_hash(current_user.password, current_password):
            if new_password == confirm_new_password:
                current_user.password = generate_password_hash(new_password)
                db.session.add(current_user)
                db.session.commit()
                flash("Password changed successfully", "success")
                return redirect(url_for("portal"))
            else:
                error = "Password confirmation failed"
        else:
            error = "Current password failed"
    return render_template("password.html", form=form, error=error)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """ Get out here """
    logout_user()
    flash("Successful logged out.", "success")
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
    """ Current logged in user """
    return User.query.get(user_id)


# HTTP Errors views
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify("500 Internal Server Error.")


@app.errorhandler(404)
def page_not_found(e):
    return jsonify("404 Not Found.")


@app.errorhandler(405)
def page_not_found(e):
    return jsonify("405 Method Not Allowed.")


@app.errorhandler(401)
def unauthorized(e):
    flash("Login first", "warning")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
