#register routes or blue_prints here

def routes_list(app):
    

    #public---------------------------------------------------------
    from website.routes.public.home import home
    app.register_blueprint(home, url_prefix='/')
    
    from website.routes.public.about import about
    app.register_blueprint(about, url_prefix='/public')
    
    #auth---------------------------------------------------------
    from website.routes.auth.login import login
    app.register_blueprint(login, url_prefix='/auth')
    
    from website.routes.auth.signup import signup
    app.register_blueprint(signup, url_prefix='/auth')
    
    from website.routes.auth.verify import verify
    app.register_blueprint(verify, url_prefix='/auth')