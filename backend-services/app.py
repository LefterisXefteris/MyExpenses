import os
from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='host.docker.internal',
        database='Transactions',
        user='lefterisgilmaz',
        password='admin'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return str(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 