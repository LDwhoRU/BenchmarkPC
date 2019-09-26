from bench import app
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
if __name__ == "__main__":
    app.config['SECRET_KEY'] = '13c144f006b7411aa39365a5d7d42da1'
    csrf = CsrfProtect(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.run()
    