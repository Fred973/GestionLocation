from soft import db, app
from soft.login.model import Users

with app.app_context():
    db.drop_all()

    db.create_all()

    # fill DB
    user_1 = Users(
    id=1,
    username='fred',
    category=1,
    password_hash='sha256$uvPHv3uhXGtYRt0h$5090871eb4c28b38128af516a3d5c1a4611a81babf273529076e5e1aadc7dc6b'

    )
    user_2 = Users(
    id=2,
    username='jojo',
    category=2,
    password_hash='sha256$uvPHv3uhXGtYRt0h$5090871eb4c28b38128af516a3d5c1a4611a81babf273529076e5e1aadc7dc6b'

    )
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

