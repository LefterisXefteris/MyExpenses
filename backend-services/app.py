import io
import os
from flask import Flask, jsonify, request, send_file
import psycopg2
from datetime import datetime, timedelta


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
    return jsonify(data)


@app.route('/transactions')
def get_visual_transactions():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT money in FROM transactions LIMIT 50;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return "No transactions found", 404

        amounts = [row[0] for row in data]

        plt.figure(figsize=(10, 6))
        plt.bar(range(len(amounts)), amounts)
        plt.title('Transaction Amounts')
        plt.xlabel('Transaction Number')
        plt.ylabel('Amount')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return send_file(buf, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error in get_visual_transactions: {e}")
        return f"An error occurred: {str(e)}", 500


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        
        return "File uploaded successfully!"
    return render_template('upload_form.html') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 