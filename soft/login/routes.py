from flask_login import login_user, login_required, logout_user, current_user
from soft import app, login_manager
from soft.login.forms import LoginForm
from flask import render_template, redirect, url_for, flash, session, request
from soft.login.model import Users, check_password_hash


@app.route('/')
def index():
    return render_template(
        "index.html"
    )


@app.route('/normal')
def normal():
    user_req = Users.query.get_or_404(current_user.id)
    return render_template(
        "normal.html",
        user=user_req
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


@app.route('/login<int:id_choice>', methods=['GET', 'POST'])
def login(id_choice):
        form = LoginForm()
        if form.validate_on_submit():
            session.permanent = True  # Logout if you close navigator
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                # Check the hash
                if check_password_hash(user.password_hash, form.password.data):
                    session['user'] = form.username.data
                    session['category'] = user.category
                    session['id_choice'] = id_choice
                    if session['category'] == 1:
                        login_user(user)
                        flash("Vous êtes connecté", category='success')
                        if id_choice == 0:
                            return redirect(url_for('dashboard_GL'))
                        elif id_choice == 1:
                            return redirect(url_for('dashboard_CCB'))
                    elif session['category'] == 2 and id_choice == 1:
                        flash("Vous n'avez pas les droits pour vous connecter ici", category='warning')
                        return redirect(url_for('index'))
                    elif session['category'] == 2 and session['category'] == 1:
                        login_user(user)
                        flash("Vous êtes connecté", category='success')
                        return redirect(url_for('dashboard_GL'))
                    elif session['category'] == 0:
                        login_user(user)
                        flash("Vous êtes connecté", category='success')
                        return redirect(url_for('normal'))

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


# Create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
        session.pop("user", None)
        session.clear()
        flash("Vous êtes déconnecté", category='info')
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )