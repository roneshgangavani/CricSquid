from db.db import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    inserted_date = db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=1)
    is_admin = db.Column(db.Boolean, nullable=False, default=0)
    is_block = db.Column(db.Boolean, nullable=False, default=0)
    expiry_date = db.Column(db.Date, nullable=False)
    is_cpo_bmd = db.Column(db.Boolean, nullable=False, default=0)
    is_cpo_mcx = db.Column(db.Boolean, nullable=False, default=0)
    is_sbo_cbot = db.Column(db.Boolean, nullable=False, default=0)
    is_yield_arima = db.Column(db.Boolean, nullable=False, default=0)
    is_spread_trading = db.Column(db.Boolean, nullable=False, default=0)
