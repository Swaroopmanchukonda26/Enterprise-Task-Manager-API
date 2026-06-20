from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Define the Task Relational Schema ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    # Read operation: Fetch active tasks from database matrix
    tasks = Task.query.all()
    return f"<h1>Enterprise Task Manager API</h1><p>Active items in database: {len(tasks)}</p>"

@app.route('/add', methods=['POST'])
def add():
    # Create operation: Insert a new task structure record
    task_title = request.form.get('title')
    if task_title:
        new_task = Task(title=task_title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Build database schema tables automatically
    app.run(debug=True)
