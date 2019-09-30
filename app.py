from bench import app
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
if __name__ == "__main__":
    csrf = CsrfProtect(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.run()
    