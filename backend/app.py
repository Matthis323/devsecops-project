
import os
import logging
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration par variables d'environnement
DB_HOST     = os.environ.get('DB_HOST', 'localhost')
DB_PORT     = os.environ.get('DB_PORT', '5432')
DB_NAME     = os.environ.get('DB_NAME', 'devsecops')
DB_USER     = os.environ.get('DB_USER', 'admin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password123') 

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    logger.debug(f'[APP2] Connexion DB: host={DB_HOST} user={DB_USER}')
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW()
        )''')
        conn.commit()
        cur.close()
        conn.close()
        logger.info('[APP2] Table users creee/verifiee')
    except Exception as e:
        logger.error(f'[APP2] Erreur init DB: {e}')

@app.route('/api/users', methods=['GET'])
def get_users():
    logger.info('[APP2] GET /api/users')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, email, created_at FROM users ORDER BY id')
        rows = cur.fetchall()
        cur.close(); conn.close()
        users = [{'id': r[0], 'name': r[1], 'email': r[2], 'created_at': str(r[3])} for r in rows]
        logger.debug(f'[APP2] {len(users)} utilisateurs retournes')
        return jsonify({'users': users, 'count': len(users)})
    except Exception as e:
        logger.error(f'[APP2] Erreur DB: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name  = data.get('name', '')
    email = data.get('email', '')
    logger.info(f'[APP2] POST /api/users name={name} email={email}')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # RISQUE: requete non paramétrisee → injection SQL possible
        query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}') RETURNING id"
        cur.execute(query)
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'message': 'Utilisateur cree', 'id': user_id}), 201
    except Exception as e:
        logger.error(f'[APP2] Erreur: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close(); conn.close()
        return jsonify({'status': 'ok', 'db': 'connected', 'host': DB_HOST})
    except Exception as e:
        return jsonify({'status': 'degraded', 'db': 'error', 'detail': str(e)}), 500

if __name__ == '__main__':
    init_db()
    logger.info(f'[APP2] Demarrage Backend — DB={DB_HOST}:{DB_PORT}/{DB_NAME}')
    app.run(host='0.0.0.0', port=5001, debug=True)
