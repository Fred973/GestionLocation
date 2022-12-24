from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from soft import app, db
from flask import render_template, session, redirect, request, flash, url_for

from soft.gestion_loc.forms import UserForm
from soft.login.model import Users


@app.route('/gestionLoc/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_GL():
    try:
        user_req = Users.query.get_or_404(current_user.id)
        users_req = Users.query.all()

        return render_template(
            'gestion_loc/dashboard.html',
            user=user_req,
            users=users_req
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/dashboard/register', methods=['GET', 'POST'])
@login_required
def register():
    try:
        form = UserForm()
        if request.method == 'POST':
            user_to_add = Users(
                username=form.username.data,
                category=form.category.data,
                password_hash=generate_password_hash(form.password.data, 'sha256')
            )
            db.session.add(user_to_add)
            db.session.commit()

            flash("L'utilisateur a bien été ajouté", category='success')
            return redirect(url_for('dashboard_GL'))

        return render_template(
            'form_user.html',
            form=form
        )

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/dashboard/edit_user/<int:id_user>', methods=['GET', 'POST'])
@login_required
def edit_user(id_user):
    try:
        form = UserForm()
        user_to_update = Users.query.get_or_404(id_user)
        if request.method == 'POST':
            user_to_update.username = form.username.data
            user_to_update.category = form.category.data
            if form.password.data == '':
                pass
            else:
                user_to_update.password_hash = generate_password_hash(form.password.data, 'sha256')
            db.session.commit()

            flash("L'utilisateur a bien été modifié", category='success')
            return redirect(url_for('dashboard_GL'))


        form.username.data = user_to_update.username
        form.category.data = str(user_to_update.category)

        return render_template(
            'form_user.html',
            form=form
        )

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/dashboard/delete_user/<int:id_user>', methods=['GET', 'POST'])
@login_required
def delete_user(id_user):
    try:
        user_to_delete = Users.query.get_or_404(id_user)
        db.session.delete(user_to_delete)
        db.session.commit()

        flash("L'utilisateur a bien été supprimé", category='success')
        return redirect(request.referrer)

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/dashboard/pwd_update/<int:id_user>', methods=['GET', 'POST'])
@login_required
def pwd_update(id_user):
    try:
        form = UserForm()
        user_to_update = Users.query.get_or_404(id_user)
        if request.method == 'POST':
            user_to_update.password_hash = generate_password_hash(form.password.data, 'sha256')
            db.session.commit()

            flash("Le mot de passe a bien été modifié", category='success')
            return redirect(url_for('dashboard_GL'))

        return render_template(
            'form_pwd.html',
            form=form
        )

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )


@app.route('/gestionLoc/dashboard/username_update/<int:id_user>', methods=['GET', 'POST'])
@login_required
def username_update(id_user):
    try:
        form = UserForm()
        user_to_update = Users.query.get_or_404(id_user)
        if request.method == 'POST':
            user_to_update.username = form.username.data
            db.session.commit()

            flash("Le nom d'utilisateur a bien été modifié", category='success')
            return redirect(url_for('dashboard_GL'))

        return render_template(
            'form_username.html',
            form=form
        )

    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )




