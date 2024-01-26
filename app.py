from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

todoservice_url = 'http://localhost:5000'

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)


@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    new_task = Todo(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/todos', methods=['GET'])
def get_todos():
    response = requests.get(f"{todoservice_url}/todos")
    todos = response.json()
    return jsonify(todos)


@app.route('/todos', methods=['POST'])
def add_todo():
    name = request.json.get('name')
    response = requests.post(f"{todoservice_url}/todos", json={'name': name})
    if response.status_code == 201:
        return jsonify(response.json()), 201
    else:
        return jsonify({'error': 'Failed to add task.'}), 500


@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo_status(todo_id):
    response = requests.put(f"{todoservice_url}/todos/{todo_id}")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to update task status.'}), 500


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    response = requests.delete(f"{todoservice_url}/todos/{todo_id}")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to delete task.'}), 500


if __name__ == '__main__':
    app.run(port=5001)
