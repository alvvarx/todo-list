from flask import Blueprint, render_template, redirect, url_for, request, g
from todor.auth import login_required
from .models import Todo, User
from todor import db

# Para organizar las rutas de la aplicación 'todo'
bp = Blueprint('todo', __name__, url_prefix='/todo')

# Vista para listar las tareas del usuario logueado
@bp.route('/list')
@login_required
def index():
    tareas = Todo.query.all()
    return render_template('todo/index.html', tareas = tareas)

# Vista para crear tareas
@bp.route('/create', methods = ["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']

        tarea = Todo(g.user.id, title, description)

        db.session.add(tarea)
        db.session.commit()

        return redirect(url_for('todo.index'))
        
    return render_template('todo/create.html')

# Vista para obtener una tarea por id
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    
    return todo

# Vista para actualizar una tarea
@bp.route('/update/<int:id>', methods = ["GET", "POST"])
@login_required
def update(id):

    tarea = get_todo(id)

    if request.method == "POST":
        tarea.title = request.form['title']
        tarea.desc = request.form['desc']  
        tarea.status = True if request.form.get('status') == 'on' else False

        db.session.commit()

        return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo = tarea)

# Vista para eliminar una tarea
@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    tarea = get_todo(id)

    db.session.delete(tarea)
    db.session.commit()

    return redirect(url_for('todo.index'))

