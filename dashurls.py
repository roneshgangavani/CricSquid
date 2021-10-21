
# from routes.EXTRA.historical import historical_data
from routes.input_user import covid_help
from routes.view_help import view_help
from routes.volunteers import covid_volunteer
# def protect_view(app):
#     for view_func in app.server.view_functions:        
#         if view_func.startswith(app.config.url_base_pathname):
#             app.server.view_functions[view_func] = login_required(
#                 app.server.view_functions[view_func])

# #all commodities
# from routes.dash.all_commodities.all_commodities import all_commodity
# protect_view(all_commodity)

