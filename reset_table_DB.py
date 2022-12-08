from soft import db, app
from soft.login.model import Users

with app.app_context():
    db.drop_all()

    db.create_all()

    user = Users(
    id=1,
    username='fred',
    password_hash='sha256$uvPHv3uhXGtYRt0h$5090871eb4c28b38128af516a3d5c1a4611a81babf273529076e5e1aadc7dc6b'

    )
    db.session.add(user)
    db.session.commit()

