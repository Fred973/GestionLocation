from flask_login import login_required, current_user
from soft import app
from flask import render_template, session

from soft.login.model import Users


@app.route('/gestionLoc/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_GL():
    try:
        user_req = Users.query.get_or_404(current_user.id)

        return render_template(
            'gestion_loc/dashboard.html',
            user=user_req
        )
    except Exception as e:
        print(e)
        return render_template(
            "error_404.html",
            log=e
        )



