# Archivo principal para crear app y la configuración
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Instancia de la bbdd
db = SQLAlchemy()

# Función para crear la app
def create_app():
    app = Flask(__name__)

    # Configuración del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    )

    db.init_app(app)

    # Registramos Blueprint
    from . import todo, auth
    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        db.create_all()
    
    return app
