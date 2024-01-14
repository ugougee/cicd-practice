
from flask import Flask, request, render_template, redirect, url_for
import pymysql
import os
app = Flask(__name__)


username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
db = os.environ.get('MYSQL_DATABASE')

# Database configuration
db_config = {
    'host': f'{host}:3306',  # The name of your MySQL service in Kubernetes
    'user': username,
    'password': password,
    'db': db 
}

# Initialize database connection
def get_db_connection():
    return pymysql.connect(**db_config)
# Ensure the database and table exist
def initialize_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

initialize_db()
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title) VALUES (%s)', (title,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')