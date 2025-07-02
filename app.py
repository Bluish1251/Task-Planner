from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

# Gets our SQLite database ready & setup (file should exist but if it doesn't, it will be created)
def setup_database():
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute(''' create table if not exists tasks ''')
    connection.commit()
    connection.close()

setup_database()

# Sets up the route to serve the static index.html file
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Once all tha task is gathered, it's returned as a JSON object in the database
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description FROM tasks')
    rows = cursor.fetchall()
    tasks = []
    for row in rows:
        task = {
            'id': row[0],
            'title': row[1],
            'description': row[2]
        }
        tasks.append(task)
    connection.close()
    return jsonify(tasks)

# Adding task onto the database
@app.route('/tasks', methods=['POST'])
def add_new_task():
    data = request.get_json()
    title = data['title']
    description = ''
    if 'description' in data:
        description = data['description']

    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    connection.commit()
    connection.close()
    return jsonify({'status': 'task added'})

# Deletes the task from it's ID in the database
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    connection.commit()
    connection.close()
    return jsonify({'status': 'task deleted'})

if __name__ == '__main__':
    app.run(debug=True)
