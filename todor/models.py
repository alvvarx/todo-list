# Importamos instancia de la bbdd creada mediante SQLAlchemy
from todor import db

# Modelo que representa los usuarios en la BBDD
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    # Metodo "toString"
    def __repr__(self):
        return f"<User: {self.username}>"
    
# Modelo que representa las tareas en la BBDD
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # ForeignKey de usuario
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.Text)
    status = db.Column(db.Boolean, default = False)

    # Constructor
    def __init__(self, created_by, title, desc, status = False):
        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.status = status
    
    # Metodo "toString"
    def __repr__(self):
        return f"<Todo: {self.title}>"
    



