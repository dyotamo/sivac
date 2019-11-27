from datetime import datetime
from sivac import application, login_manager
from sqlalchemy import text
from flask import Flask, render_template, redirect, flash, jsonify, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import ValidateForm, LoginForm, UploadForm, PasswordChangeForm
from models import db, Certificate, User


@application.route("/", methods=["GET", "POST"])
def index():
    """ Presentes a certificate validation form and validates certificates """
    form = ValidateForm()
    error = None
    if form.validate_on_submit():
        code = form.code.data
        issue_date = form.issue_date.data
        institution = form.institution.data

        certificate = Certificate.query.filter_by(code=code, issue_date=datetime(
            issue_date.year, issue_date.month, issue_date.day), institution=institution).first()

        if certificate is None:
            error = "Certificado inválido."
        else:
            flash("Certificado com o código {} é válido, do titular {}, emitido em {}.".format(
                certificate.code, certificate.owner, certificate.issue_date.strftime("%d/%m/%Y")), "success")
            return redirect(url_for("index"))
    return render_template("index.html", form=form, error=error)


@application.route("/portal", methods=["GET", "POST"])
@login_required
def portal():
    """ Show all certificates that belongs to certain institution,
    and also makes possible to upload a .csv file containg new certificates """
    form = UploadForm()
    if form.validate_on_submit():
        from tools.file import save_csv, import_csv

        path = save_csv(form)
        with open(path, "r") as f:
            import_csv(f)

        flash("Ficheiro carregado com sucesso.", "success")
        return redirect(url_for("portal"))
    return render_template("portal.html", page=Certificate.query.order_by(text("id desc")).filter_by(
        institution=current_user.institution).paginate(per_page=9), form=form)


@application.route("/delete/<int:id>", methods=["POST"])
@login_required
def remove(id):
    """ Remove a certificate """
    certificate = Certificate.query.filter_by(id=id).first_or_404()
    db.session.delete(certificate)
    db.session.commit()

    flash("Certificado de {} removido com sucesso.".format(
        certificate.owner), "success")
    return redirect(url_for("portal"))


@application.route("/login", methods=["GET", "POST"])
def login():
    """ Login view """
    form = LoginForm()
    if form.validate_on_submit():
        institution = form.institution.data
        password = form.password.data

        user = User.query.filter_by(institution=institution).first()
        if user is None:
            flash("Credenciais inválidas.", "danger")
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Entrou como {}.".format(
                    user.institution), "success")
                return redirect(url_for("portal"))
            else:
                flash("Credenciais inválidas.", "danger")
    return render_template("login.html", form=form)


@application.route("/password", methods=["GET", "POST"])
@login_required
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
                flash("Password alterado com sucesso.", "success")
                return redirect(url_for("portal"))
            else:
                error = "Confirmação de password falhou."
        else:
            error = "Password corrente errado."
    return render_template("password.html", form=form, error=error)


@application.route("/logout", methods=["GET"])
@login_required
def logout():
    """ Get out here """
    logout_user()
    flash("Saiu com sucesso.", "success")
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
    """ Current logged in user """
    return User.query.get(user_id)


# HTTP Errors views
@application.errorhandler(500)
def internal_server_error(e):
    import traceback
    from tools.mail import send_mail

    send_mail(traceback.format_exc())
    return jsonify("500 Internal Server Error, dyotamo has been reported.")


@application.errorhandler(404)
def page_not_found(e):
    return jsonify("404 Not Found.")


@application.errorhandler(405)
def page_not_found(e):
    return jsonify("405 Method Not Allowed.")