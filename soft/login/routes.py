from flask_login import login_user, login_required, logout_user
from soft import app, login_manager
from soft.login.forms import LoginForm
from flask import render_template, redirect, url_for, flash, session, request
from soft.login.model import Users, check_password_hash


@app.route('/')
def index():
    return render_template(
        "index.html"
    )


@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.query.get(int(user_id))
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            session.permanent = True  # Logout if you close navigator
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                # Check the hash
                if check_password_hash(user.password_hash, form.password.data):
                    session['user'] = form.username.data
                    login_user(user)
                    flash("Vous êtes connecté", category='success')
                    return redirect(url_for('dashboard'))
                else:
                    flash("Mauvais mot de passe - Essai encore!", category='warning')
                    redirect(request.referrer)
            else:
                flash("Cette utilisateur n'existe pas...", category='error')
                redirect(request.referrer)

        return render_template(
            'login.html',
            form=form
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


# Create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        session.pop("user", None)
        logout_user()
        flash("Vous êtes déconnecté", category='info')
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )