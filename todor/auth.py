from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
# Al importar los modelos ya se han realizado las migraciones a las BBDD
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from todor import db
import functools

# Para organizar las rutas de la aplicación auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Vista para registrar usuarios en la BBDD
@bp.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Creamos el usuario con los datos del formulario (contraseña encriptada)
        user = User(username, generate_password_hash(password))

        # Comprobamos si el usuario ya existe en la base de datos
        user_exists = User.query.filter_by(username = username).first()

        # Creamos variable que contiene mensaje si se crea usuario o ya existe
        msg = None

        if user_exists == None:
            db.session.add(user)
            db.session.commit()

            msg = "Usuario creado correctamente"

            flash(msg, "success")
            
            return redirect(url_for('auth.login'))
        else:
            msg = f"El usuario {username} ya está en la base de datos"

            flash(msg, "error")
        
    return render_template('auth/register.html')

# Vista para iniciar sesion
@bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Creamos variable que contiene mensaje si se crea usuario o ya existe
        msg = None

        user = User.query.filter_by(username = username).first()

        # Validar datos (NO ES LA FORMA MAS OPTIMA)
        if user == None:
            msg = "El usuario no existe en la base de datos"
        elif not check_password_hash(user.password, password):
            msg = "Contraseña incorrecta"

        # Iniciar sesión 
        if msg is None:
            # Primero limpiamos sesion por si hubiera alguna iniciada
            session.clear()
            # Guardamos el id de usuario en el campo 'user_id' de la sesion
            session['user_id'] = user.id
            
            return redirect(url_for('todo.index'))

        flash(msg)

    return render_template('auth/login.html')

# Vista para cerrar sesión
@bp.route('/logout')
def logout():
    # Limpiamos la sesión
    session.clear()
    return redirect(url_for('index'))

# Vista para mantener la sesion activa durante navegacion en la web
@bp.before_app_request
def load_logger_in_user():
    user_id = session.get('user_id') 

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

# Vista para requerir autenticación en las urls
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user == None:
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)
        
    return wrapped_view