from flask import Flask


from .config.modules import init_modules
from .config.registered_routes import routes_list
from .config.app_config import(
    database_config,
    cookies_config,
    smtp_config,
    last_seen_config,
    login_manager_config,
    create_database
)


#create flask app
def flask_app():
    app = Flask(__name__, static_folder='templates/static')  
    database_config(app)#database
    cookies_config(app)#cookies or session
    smtp_config(app)#smtp
    init_modules(app) #used modules
    login_manager_config()#login manager
    #last_seen_config(app)
    routes_list(app)#registered route
    create_database(app)#create sqlite.db if none
    return app




            