from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash

from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash

from soft.login.forms import LoginForm
from soft.login.model import Users
from soft.saab.questions.forms import QuestionListForm
from soft.saab.questions.model import QuestionList


@app.route('/SAAB/login', methods=['GET', 'POST'])
def saab_login():
    form = LoginForm()
    if form.validate_on_submit():
        session.permanent = False  # Logout if you close navigator
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                session['user'] = form.username.data
                session['category'] = user.category
                if session['category'] == 3:  # if admin
                    login_user(user)
                    return render_template(
                        "saab/main_menu.html"
                    )
            else:
                flash("Mauvais mot de passe - Essai encore!", category='warning')
                redirect(request.referrer)
        else:
            flash("Cette utilisateur n'existe pas...", category='error')
            redirect(request.referrer)

    return render_template(
        "saab/saab_login.html",
        form=form
    )

@app.route('/SAAB/main_menu')
@login_required
def main_menu():
    return render_template(
        'saab/main_menu.html'
    )

@app.route('/SAAB/orders')
@login_required
def orders():
    return render_template(
        'saab/orders.html'
    )

@app.route('/SAAB/tasks_list_inspection')
@login_required
def tasks_list_inspection():
    return render_template(
        'saab/tasks_list_inspection.html'
    )