from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)


@app.route('/todos', methods=['GET'])
def get_todos():
    todo_list = Todo.query.all()
    todos = []
    for todo in todo_list:
        todos.append({'task_id': todo.task_id, 'name': todo.name, 'done': todo.done})
    return
