from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object("config.flask_config.DevelopmentConfig")
Bootstrap(app)

