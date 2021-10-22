from routes.auth import index,match1,todays
from application import app
from flask import Flask, current_app

app.add_url_rule("/", "index", index)
app.add_url_rule("/match1", "match1_playings", match1)
app.add_url_rule("/todays", "todays_match_playings", todays)
# app.add_url_rule("/covid/ask_help/", "Asking_help", covid_ask_help)
# app.add_url_rule('/covid/view_available_help/','_available_help',covid_view_help)
# app.add_url_rule('/covid/volunteer_regi/','volunteers_covid',covid_volunterr_help)
# app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
# app.add_url_rule("/register", "register", register, methods=["GET", "POST"])
# app.add_url_rule("/logout", "logout", logout)


from security.security import login_manger

login_manger.init_app(app)
import dashurls

if __name__ == "__main__":
    app.run()
