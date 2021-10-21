from flask_login import LoginManager
from models.user import User

login_manger = LoginManager()


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(user_id)
