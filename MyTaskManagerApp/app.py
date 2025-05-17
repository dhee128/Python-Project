import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('taskmanager.db')
    conn.row_factory = sqlite3.Row  # This makes the result behave like a dictionary
    conn.execute('PRAGMA busy_timeout = 3000')  # Set timeout to 3000 ms (3 seconds)
    return conn

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    conn = get_db_connection()

    if search_query:
        tasks = conn.execute('SELECT * FROM tasks WHERE content LIKE ?', ('%' + search_query + '%',)).fetchall()
    else:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()

    total = conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    completed = conn.execute('SELECT COUNT(*) FROM tasks WHERE done = 1').fetchone()[0]
    conn.close()

    # Convert due_date string to datetime object
    now = datetime.now()
    updated_tasks = []
    for task in tasks:
        # Convert sqlite3.Row to a dictionary
        task_dict = dict(task)
        # Add due_date_obj field
        task_dict['due_date_obj'] = datetime.strptime(task_dict['due_date'], '%Y-%m-%d')
        updated_tasks.append(task_dict)
    
    return render_template('home.html', tasks=updated_tasks, total=total, completed=completed, now=now)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    due_date = request.form['due_date']
    priority = request.form.get('priority', 'Medium')  # Default to 'Medium' if not provided
    category = request.form['category']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (content, due_date, priority, category) VALUES (?, ?, ?, ?)',
                 (content, due_date, priority, category))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/done/<int:task_id>')
def done(task_id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST', 'GET'])
def delete(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
