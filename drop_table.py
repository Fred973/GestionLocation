from soft import db, app


with app.app_context():
    db.drop_all()
