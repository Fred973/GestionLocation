from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from soft import app, db
from flask import render_template, session, redirect, request, url_for, flash

from soft.login.forms import LoginForm
from soft.login.model import Users
from soft.saab.forms import SAABLoginForm
from soft.saab.questions.forms import QuestionsListForm
from soft.saab.questions.model import QuestionsList


@app.route('/SAAB/login', methods=['GET', 'POST'])
def saab_login():
    form = SAABLoginForm()
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
                    return redirect(url_for('main_menu'))
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


# Create logout page
@app.route('/SAAB/logout', methods=['GET', 'POST'])
@login_required
def saab_logout():
    try:
        logout_user()
        session.pop("user", None)
        session.clear()
        flash("Vous êtes déconnecté", category='info')
        return redirect(url_for('saab_login'))
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )



@app.route('/SAAB/main_menu')
@login_required
def main_menu():
    return render_template(
        'saab/main_menu.html'
    )